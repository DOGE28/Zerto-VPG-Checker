# Zerto ZVM Health Checker

This is designed to be installed onto the Linux machine that runs your ZVM. Please do not attempt to install this on Windows or a different Linux machine as it will not work!

## How It Works

This is a Python script ran as a systemd service that checks the status of your ZVM every 10 minutes. If there is a problem for three consecutive checks (30 minutes), a problem is reported and emailed. If there is a problem that persists through the three consecutive checks, the chances of it being a false positive are next to none.

We suggest keeping this at the default of 10 minutes to avoid bogging down the ZVM with API calls. 

## Keycloak

We will need to create a Client inside of Keycloak that we will use to authenticate against the ZVM API.

1. Log in to Keycloak at h<span>ttps:</span>//ZVM-IP/auth as your admin user that came preconfigured with the ZVM and go to the "zerto" Realm in the top left

![alt text](resources/image.png)

2. Go to "Client" and create a new client
    - Client ID: zerto-api
        - Next
    - Turn on "Client authentication" and "Authroization", check the "Standard flow", "Implicit flow", and "Direct access grants" boxes
    - Save (No other changes need to be made)

3. Go to the newly made zerto-api client, go to the "Credentials" tab and copy the "Client Secret" for later use.

## Installation


Begin by making a directory called 'Zerto-Alerts' and entering it.

```
cd && mkdir Zerto-Alerts && cd Zerto-Alerts
```

Then run the following to download the files and make the installation and run scripts executable.

```
curl -LO https://github.com/DOGE28/Zerto-VPG-Checker-Linux/archive/refs/heads/Client.zip
unzip main.zip
rm main.zipc
cd Zerto-VPG-Checker-Linux-Client
chmod +x install.sh
chmod +x run.sh
```

> [!Note]
> You may need to download unzip if the above script does not work. ```sudo apt install unzip```


Please have the following before continuing:

* Keycloak zerto-api client secret
* SMTP server IP/FQDN
* SMTP port 
* Email address to send alerts
* Email address(s) to receive alerts
* VPG threshold percent (default: 90)
    - If percent of VPGs **UP** is less than this, report a problem
* Run interval in minutes (default: 10)

Next, run the following to begin the installation

```
./install.sh
```

This will install all needed dependencies, create a `.env` file with the prompted information, and create a system service that will run on startup.
If you ever need to change the information you initially provided in the installtion script, you can change them in the created `.env` file. 


## Systemd Commands

The install script will get everything ready for the monitor to run continuously, even after restart. But the service still needs to be started initially right after you've finished getting environment variables and setting which sites you want to monitor.

The below command will start the zerto-alerts service:

```
sudo systemctl start zerto-alerts
```

This command will check the status of the service and include important information from the most recent run of the monitor:

```
sudo sustemctl status zerto-alerts
```

Finally, to verify that the script is currently running, use the command:
```
sudo systemdctl status zerto-alerts.service
```
It should show the service as active and you will see the print statements of the script in the output.