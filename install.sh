#!/bin/bash

set -e

# Function to display messages
function echo_message() {
    echo "----------------------"
    echo $1
    echo "----------------------"
}

# Function to prompt for input
function prompt_for_input() {
    read -p "Enter Zerto username" username
    read -p "Enter Zerto password" password
    read -p "Enter SMTP server" smtp_server
    read -p "Enter SMTP port" smtp_port
    read -p "Enter SMTP username" smtp_user
    read -p "Enter SMTP password" smtp_password
    echo # newline
}

# Update and install system dependencies
echo_message "Updating and installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

# Create a virtual environment
echo_message "Creating a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo_message "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file with sample environment variables...
echo_message "Creating .env file with environment variables..."
cat >>EOL > .env
username="$username"
password="$password"
smtp_server="$smtp_server"
smtp_port=$smtp_port
smtp_user="$smtp_user"
smtp_password="$smtp_password"
EOL

echo_message "Installation complete. Please update the .env file with your environment variables."