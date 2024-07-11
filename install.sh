#!/bin/bash

set -e

# Function to display messages
function echo_message() {
    echo
    echo "----------------------"
    echo $1
    echo "----------------------"
    echo
}

# Function to prompt for input
function prompt_for_input() {
    read -p "Enter Zerto username, format username@domain: " username
    read -s -p "Enter Zerto password: " password
    read -p "Enter SMTP server: " smtp_server
    read -p "Enter SMTP port: " smtp_port
    read -p "Enter SMTP username: " smtp_user
    read -s -p "Enter SMTP password: " smtp_password
    echo # newline
}

# Function to prompt for cronjob creation
function prompt_for_cronjob() {
    while true; do
        read -p "Do you want to set up a cron job for each location? (y/n)" yn
        case $yn in
            [Yy]* ) echo ; break;;
            [Nn]* ) echo ; break;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

function prompt_for_cronjob_interval() {
    while true; do
        read -p "Enter the interval in minutes for the cron job: " interval
        if [[ $interval =~ ^[0-9]+$ ]]; then
            break
        else
            echo "Please enter a valid number."
        fi
    done

}

sgu_path=$"./app/sgu.py"
boi_path=$"./app/boi.py"
fb_path=$"./app/fb.py"

# Update and install system dependencies
echo_message "Updating and installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

echo "System dependencies have been updated and installed."

# Create a virtual environment
echo_message "Creating a virtual environment..."
python3 -m venv venv
source ./venv/bin/activate
echo "Virtual environment has been created and activated."

# Install Python dependencies
echo_message "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo
echo "Python dependencies have been installed."

# Create .env file with sample environment variables...
echo_message "Creating .env file with environment variables..."
prompt_for_input

cat <<EOL > .env
username="$username"
password="$password"
smtp_server="$smtp_server"
smtp_port=$smtp_port
smtp_user="$smtp_user"
smtp_password="$smtp_password"
sgu_zerto_base_url="sgu-zvm.tonaquint.local:9669"
boi_zerto_base_url="boi-zvm.tonaquint.local:9669"
fb_zerto_base_url="sgu-fb-zvm.tonaquint.local:9669"
sgu_ip="172.16.100.19"
boi_ip="172.17.6.20"
fb_ip="172.16.93.6"
EOL
echo
echo "Environment variables have been written to .env file. You may edit this file to change the environment variables if needed."
echo

prompt_for_cronjob
# Deciding whether to set up a cron job"
if [ "$yn" = "yes" || "$yn" = "y" || "$yn" = "Y" ]; then
    prompt_for_cronjob_interval
    echo_message "Setting up the cron job to run every $interval minutes..."
    # Get current user
    current_user=$(whoami)
    #(Re)write the cron jobs to ensure they run every 15 minutes
    crontab -l | grep -v "$sgu_path" | crontab -
    (crontab -l 2>/dev/null; echo "*/$interval * * * * cd $(pwd) && ./bin/python $sgu_path") | crontab -
    (crontab -l 2>/dev/null; echo "*/$interval * * * * cd $(pwd) && ./bin/python $boi_path") | crontab -
    (crontab -l 2>/dev/null; echo "*/$interval * * * * cd $(pwd) && ./bin/python $fb_path") | crontab -
    echo "Cron job has been set up to run every $interval minutes."
else
    echo_message "Skipping cron job setup..."
fi

source ./venv/bin/activate

echo_message "Installation complete. Please check the .env file that was created to ensure the environment variables are correct before running. \n Also check the cronjobs to ensure they are set up correctly."