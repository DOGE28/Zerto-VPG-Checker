echo "Checking if an instance is already running..."

PID=$(pgrep -f "alerts.py")

if [ -n "$PID" ]; then
    echo "An instance is already running. Exiting..."
    kill -9 $PID
    echo "Process $PID has been killed"
    echo "Proceeding..."
else
    echo "No instance is running. Proceeding..."
fi



cd /home/zadmin/Zerto-Alerts/Zerto-VPG-Checker-Linux-Client/

source ./venv/bin/activate

cd appv2/

python3 alerts.py