# Zerto VPG Checker

This project is designed to alert the cloud team when a percentage of a Zerto site's VPGs are down. If this happens, it is generally an indicator of bigger issues that needs more immediate attention.

# Installation

First, you'll want to CD into the directory you want to use. Below is a great start, otherwise create your own folder:
```
mkdir Zerto-Alerts
cd Zerto-Alerts
```
Next, download and unzip the script files:
```
curl -LO https://github.com/DOGE28/Zerto-VPG-Checker/archive/refs/heads/main.zip
unzip main.zip
rm main.zip # This is just for cleanup
cd Zerto-VPG-Checker-main
chmod +x install.sh # Makes the install script executable
```
If you haven't run into any errors, you can then run:
```
./install.sh
```
This script will download any neccesary dependencies, create a python virtual environment, and will create a .env file and prompt for the following environment variables:

* username = Zerto username for interacting with ZVM API
* password = Zerto password
* smtp_server = SMTP server used to send emails
* smtp_port = SMTP port, usually 587
* smtp_user = SMTP email address that sends the alert
* smtp_password = Password associated with smtp_user


 You will be asked if you want to create a `crontab` job to be run every 15 minutes. A job is created for each of the main ZVM locations, SGU, BOI, and FB. Each site will be ran in parallel. If you'd rather create these on your own, say no to the prompt.

