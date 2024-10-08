#!/bin/bash

echo "Sending Test Email..."
cd /home/zadmin/Zerto-Alerts/Zerto-VPG-Checker-Linux-Client/

source ./venv/bin/activate

cd appv2/

python3 -u alerts.py --test