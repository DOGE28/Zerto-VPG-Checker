# Zerto VPG Checker

This project is designed to alert the cloud team when a percentage of a Zerto site's VPGs are down. If this happens, it is generally an indicator of bigger issues that needs more immediate attention.

# Installation

Begin by making a directory called 'Zerto-Alerts' and entering it.

```
cd
mkdir Zerto-Alerts
cd Zerto-Alerts
```

Then run the following to download the monitor and make the installation script executable.

```
curl -LO https://github.com/DOGE28/Zerto-VPG-Checker/archive/refs/heads/main.zip
unzip main.zip
rm main.zip
cd Zerto-VPG-Checker-main
chmod +x install.sh
```

If you haven't run into any errors, you can then run:

```
./install.sh
```

This will install all dependencies and file directories needed. You will need to input the variables in the .env file.
You will also need to uncomment out the sites you want to monitor. You can find these in lines 160-190 in the alerts.py file. Just take out the '#' in front of the lines to uncomment.