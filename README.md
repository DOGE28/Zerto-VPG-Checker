# Zerto VPG Checker

This repo is designed to alert the cloud team when a percentage of a Zerto site's VPGs are down.

# Installation

CD into the directory you want to install the script in, then run:
```
curl -LO https://github.com/DOGE28/Zerto-VPG-Checker/archive/refs/heads/main.zip
unzip main.zip -d Zerto-VPG-Checker
rm main.zip
cd Zerto-VPG-Checker
chmod +x install.sh
```
If you haven't run into any errors, you can then run:
```
./install.sh
```
This script will download any neccesary dependencies, create a python virtual environment, and start creating environment variables.
It will create a .env file and prompt for the following environment variables:

* username = Zerto username for interacting with ZVM API
* password = Zerto password
* smtp_server = SMTP server used to send emails
* smtp_port = SMTP port, usually 587
* smtp_user = SMTP email address that sends the alert
* smtp_password = Password associated with smtp_user


 You will be asked if you want to create a `crontab` job to be run every 15 minutes. A job is created for each of the main ZVM locations, SGU, BOI, and FB. If you'd rather create these on your own, say no to the prompt.