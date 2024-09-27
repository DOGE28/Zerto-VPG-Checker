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

echo_message "Creating systemd service..."

# Create a systemd service
cat <<EOL > /etc/systemd/system/zerto-alerts.service
[Unit]
Description=Zerto Alerts Service
After=network.target

[Service]
User=$USER
WorkingDirectory=/home/automate/Zerto-Alerts/Zerto-VPG-Checker-main
ExecStart=/bin/bash /home/automate/Zerto-Alerts/Zerto-VPG-Checker-main/run.sh
Restart=always
RestartSec=5

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOL

echo "Systemd service has been created successfully"
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Zerto Alerts service has been created successfully and is ready to be started"

# Display the next steps

echo_message "Next steps:"

echo "1. Fill in the required values in the .env file"
echo "2. Adjust the alerts.py file by uncommenting the desired location (Check lines 160-190)"
echo "3. Run the application using the command: sudo systemctl start zerto-alerts.service"

echo_message "The Zerto Alerts service has been successfully installed and configured"