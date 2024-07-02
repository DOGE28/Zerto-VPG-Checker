import requests

# Disable IPv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False

# Disable warnings for insecure requests (not recommended for production)
requests.packages.urllib3.disable_warnings()

# Zerto server details
zerto_base_url = 'https://sgu-zvm.tonaquint.local:9669/v1'  # Replace with your Zerto server URL
username = 'tonaquint\\prtgvcenter-bot'
password = 'QEW471BcYYsD'

# Function to authenticate and get token
def authenticate(base_url, user, pwd):
    auth_url = f'{base_url}/session/add'
    print("Attempting to authenticate!")

    response = requests.post(auth_url, json={"authenticationMethod": 0,"login": user, "password": pwd}, timeout=90, verify=False)

    if response.status_code == 200:
        print("Authentication successful!")
        return response.headers['x-zerto-session']
    else:
        print(f'Failed to authenticate: {response.status_code} - {response.text}')
        return None

# Function to make authenticated GET requests
def zerto_get(base_url, token, endpoint):
    headers = {
        'Content-Type': 'application/json',
        'x-zerto-session': token
    }
    url = f'{base_url}/{endpoint}'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code} - {response.text} for endpoint: {endpoint}')
        return None

# Authenticate and get token
auth_token = authenticate(zerto_base_url, username, password)
if auth_token:
    # Example: Get Zerto Virtual Protection Groups (VPGs)
    endpoint = 'vpgs'  # Replace with the correct endpoint
    vpgs = zerto_get(zerto_base_url, auth_token, endpoint)
    if vpgs:
        print(vpgs)
    else:
        print(f'Failed to retrieve data from endpoint: {endpoint}')
