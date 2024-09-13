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

# Update and install system dependencies

echo_message "Updating and installing system dependencies"
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

echo "System dependencies have been updated and installed successfully"

# Create a virtual environment and activate it

echo_message "Creating a virtual environment..."

python3 -m venv venv
source ./venv/bin/activate

echo "Virtual environment has been created and activated successfully"

# Install the required Python packages

echo_message "Installing the required Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
echo
echo "Python dependencies have been installed successfully"

# Create .env file

echo_message "Creating .env file..."

cat <<EOL > .env
keycloak_client_id=
sgu_prod_zvm_url=
sgu_prod_secret=
boi_prod_zvm_url=
boi_prod_secret=
fb_prod_zvm_url=
fb_prod_secret=
sgu_inf_zvm_url=
sgu_inf_secret=
boi_inf_zvm_url=
boi_inf_secret=
okc_inf_zvm_url=
okc_inf_secret=
EOL

echo
echo ".env file has been created successfully. Please fill in the required values."
echo

# Setup Cronjobs

echo_message "Would you like to set up a cronjob for this script to run every 15 minues? (y/n)"
read -r response

if [ "$response" == "y" ]; then
    echo_message "Setting up cronjob..."
    cronjob="*/15 * * * * $(pwd)/venv/bin/python $(pwd)/alerts.py"
    (crontab -l; echo "$cronjob") | crontab -
    echo "Cronjob has been set up successfully"
fi

echo_message "Installation has been completed successfully."