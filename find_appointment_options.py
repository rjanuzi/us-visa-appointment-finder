import asyncio

from time import sleep
from datetime import date
import json

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

RUN_FOREVER = True
SLEEP_TIME = 60 * 60 * 2  # 2 Hours
MONTHS_RANGE = 12
OUTPUT_DAYS_LIMIT = 10
CONFIG_FILE = "config.json"

LOGIN_PAGE = "https://ais.usvisa-info.com/pt-br/niv/users/sign_in"
APPOINTMENT_PAGE = "https://ais.usvisa-info.com/pt-br/niv/schedule/53185389/appointment"

EMAIL_ELEMENT_ID = "user_email"
PASSWORD_ELEMENT_ID = "user_password"
POLICY_CHECK_ELEMENT_CLASS_NAME = "icheckbox"
LOGIN_BTN_NAME = "commit"
LOCATION_SELECT_ID = "appointments_consulate_appointment_facility_id"
APPOINTMENT_DATE_ID = "appointments_consulate_appointment_date"
CALENDAR_DIV_ID = "ui-datepicker-div"
CALENDAR_FIRST_DIV_CALSS_NAME = "ui-datepicker-group-first"


async def main() -> None:
    while True:
        # Use the last configs for each check
        configs = json.load(open(CONFIG_FILE, "r"))

        with webdriver.Chrome() as driver:
            # Login
            driver.get(LOGIN_PAGE)

            sleep(5)

            email_elem = driver.find_element(By.ID, EMAIL_ELEMENT_ID)
            password_elem = driver.find_element(By.ID, PASSWORD_ELEMENT_ID)
            check_policy_elem = driver.find_element(
                By.CLASS_NAME, POLICY_CHECK_ELEMENT_CLASS_NAME
            )
            login_btn = driver.find_element(By.NAME, LOGIN_BTN_NAME)

            email_elem.send_keys(configs["email"])
            password_elem.send_keys(configs["password"])
            check_policy_elem.click()  # Check policy
            login_btn.click()  # Login

            sleep(2)

            # Check Apointments
            driver.get(APPOINTMENT_PAGE)

            # Select Location
            location_elem = Select(driver.find_element(By.ID, LOCATION_SELECT_ID))
            location_elem.select_by_visible_text(configs["location"])

            sleep(2)

            # Open Dates
            appointment_date_elem = driver.find_element(By.ID, APPOINTMENT_DATE_ID)
            appointment_date_elem.click()

            # Navigate Until Find next time
            calendar_div_elem = driver.find_element(By.ID, CALENDAR_DIV_ID)

            # Iterate over the months listing the options
            days_options = []

            # Available dates are links
            for _ in range(MONTHS_RANGE):
                # Calendar is a table of days (tds) and the available days has links inside the td
                tmp_days_tds = (
                    calendar_div_elem.find_element(
                        By.CLASS_NAME, CALENDAR_FIRST_DIV_CALSS_NAME
                    )
                    .find_element(By.TAG_NAME, "tbody")
                    .find_elements(By.TAG_NAME, "td")
                )

                for tmp_table_data in tmp_days_tds:
                    try:
                        tmp_year = int(tmp_table_data.get_attribute("data-year"))
                        tmp_month = int(tmp_table_data.get_attribute("data-month")) + 1
                        day_link = tmp_table_data.find_element(By.TAG_NAME, "a")
                        days_options.append(
                            {
                                "year": tmp_year,
                                "month": tmp_month,
                                "day": int(day_link.text),
                            }
                        )

                        if len(days_options) >= OUTPUT_DAYS_LIMIT:
                            break
                    except NoSuchElementException:
                        pass  # Just Ignore
                    except TypeError:
                        pass  # Just Ignore

                if len(days_options) >= OUTPUT_DAYS_LIMIT:
                    break

                calendar_div_elem.find_element(
                    By.CLASS_NAME, "ui-datepicker-next"
                ).click()

        # Dump all options
        with open("available_options.json", "w") as f:
            json.dump(days_options, f)

        output = f"Nearest available days at {configs['location']}:\n"
        for idx in range(min(OUTPUT_DAYS_LIMIT, len(days_options))):
            tmp_option = days_options[idx]
            tmp_date = date(
                year=tmp_option["year"],
                month=tmp_option["month"],
                day=tmp_option["day"],
            )
            output += f"\n\t{tmp_date.strftime('%d/%b/%Y')}"

        print(output)

        # Send options by telegram
        telegram_bot_token = configs.get("telegram-bot-token", False)
        telegram_chat_id = configs.get("telegram-chat-id", False)

        if telegram_bot_token and telegram_chat_id:
            telegram_chat_id = int(telegram_chat_id)
            from telegram import Bot

            bot = Bot(token=telegram_bot_token)

            await bot.send_message(chat_id=telegram_chat_id, text=output)

        if RUN_FOREVER:
            print(f"Sleeping for {int(SLEEP_TIME/60)} minutes and checking again")
            sleep(SLEEP_TIME)
        else:
            break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
