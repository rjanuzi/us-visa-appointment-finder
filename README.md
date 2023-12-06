# US VISA Appointment Finder
![Python 3.11.0](https://img.shields.io/badge/Python-3.11.0-green.svg?style=plastic)
![Selenium 4.16.0](https://img.shields.io/badge/Selenium-4.16.0-green.svg?style=plastic)

This is a simple automation to check available days to schedule the USA Visa Appointment in USA Embassy in Brazil.

## The Problem

In Brazil it is often sometimes hard to find an available time slot to schedule the US VISA's meeting in the near-term. One "non-written rule" is that the person should be check the appointments site every day and look for some cancelation.

## The Solution

This project is a basic RPA (Robotic Process Automation) which access the Embassy site, execute the logon in the user account and send the next schedule options by telegram (and in the console).

## How to Use

To use this project it is really simple, you just need to:

1. Have Python (3.11 or latter) installed
2. Install the dependencies (Selenium and Telegram Bot).
3. Have an account at the Embassy [Site](https://ais.usvisa-info.com/pt-br/niv/users/sign_in)
4. (Optional) Have an [Telegram Bot created](https://core.telegram.org/bots/tutorial)
5. Configure your data into config-template.json file
6. Rename config-template.json to config.json
7. Run the find_appointment_options.py

### Installing Dependecies

```bash
pip install -r requirements.txt
```

The above command will install the following dependecies:

- [Selenium](https://selenium-python.readthedocs.io/) for Web Scripting
- [Python Telegram Bot](https://python-telegram-bot.org/) for telegram messaging (optional)


### Running the Code

```bash
python find_appointment_options.py
```

The above command will start the program. The script will run "forever" (just close it when you want to) and will check for appointment options every 2 hours.

The main steps executed are:

1. Open the Chrome Browser (ensure that you have it installed)
2. Loging into the Embassy Site with the configured email and password (config.json)
3. Select the configured location (config.json).
4. Check along the next 12 months for all the options and stops when find 10 options.
5. Print the first 10 options in the terminal.
6. Send the first 10 options in the telegram chat configured (optional in config.json).