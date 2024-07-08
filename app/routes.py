import requests
from config import settings

requests.packages.urllib3.disable_warnings()

class ZertoGet():
    def __init__(self, site=None):

        self.site = site
        self.sgu_zvm_base_url = settings.sgu_zerto_base_url
        self.boi_zvm_base_url = settings.boi_zerto_base_url
        self.fb_zbm_base_url = settings.fb_zerto_base_url
        self.user_name = settings.username
        self.password = settings.password
        self.sgu_auth_url = f'https://{self.sgu_zvm_base_url}/v1/session/add'
        self.boi_auth_url = f'https://{self.boi_zvm_base_url}/v1/session/add'
        self.fb_auth_url = f'https://{self.fb_zbm_base_url}/v1/session/add'


        try:
            if self.site == "SGU":
                self.sgu_response = requests.post(self.sgu_auth_url, json={'authenticationMethod': 0, 'login': self.user_name, 'password': self.password},timeout=10, verify=False)
        except:
            print("Failed to connect to SGU ZVM, attempting direct connection with IP address.")
            self.sgu_response = requests.post(f'https://{settings.sgu_ip}:9669/v1/session/add', json={'authenticationMethod': 0, 'login': self.user_name, 'password': self.password},timeout=10, verify=False)
        
        try:
            if self.site == "BOI":
                self.boi_response = requests.post(self.boi_auth_url, json={'authenticationMethod': 0, 'login': self.user_name, 'password': self.password},timeout=10, verify=False)
        except:
            print("Failed to connect to BOI ZVM, attempting direct connection with IP address.")
            self.boi_response = requests.post(f'https://{settings.boi_ip}:9669/v1/session/add', json={'authenticationMethod': 0, 'login': self.user_name, 'password': self.password},timeout=10, verify=False)   
        
        try:
            if self.site == "FB":
                self.fb_response = requests.post(self.fb_auth_url, json={'authenticationMethod': 0, 'login': self.user_name, 'password': self.password},timeout=10, verify=False)
        except:
            print("Failed to connect to FB ZVM, attempting direct connection with IP address.")
            self.fb_response = requests.post(f'https://{settings.fb_ip}:9669/v1/session/add', json={'authenticationMethod': 0, 'login': self.user_name, 'password': self.password},timeout=10, verify=False)
        
        
        

    def login(self):
        if self.site == "SGU":
            if self.sgu_response.status_code == 200:
                print('Login successful to SGU ZVM')
                sgu_auth_token = self.sgu_response.headers['x-zerto-session']
                #print(sgu_auth_token)
                return sgu_auth_token
            else:
                print(f'Response Code: {self.sgu_response.status_code} | Login failed at SGU ZVM')
        if self.site == "BOI":
            if self.boi_response.status_code == 200:
                print('Login successful to BOI ZVM')
                boi_auth_token = self.boi_response.headers['x-zerto-session']
                return boi_auth_token
            else:
                print('Login failed at BOI ZVM')
        if self.site == "FB":
            if self.fb_response.status_code == 200:
                print('Login successful to FB ZVM')
                fb_auth_token = self.fb_response.headers['x-zerto-session']
                return fb_auth_token
            else:
                print('Login failed at FB ZVM')

    def get_all_vpg_names(self, auth_token):
        if self.site == "SGU":
            #auth_token = self.sgu_response.json()['auth_token']
            url = self.sgu_zvm_base_url
        if self.site == 'BOI':
            #auth_token = self.boi_response.json()['auth_token']
            url = self.boi_zvm_base_url
        if self.site == 'FB':
            #auth_token = self.fb_response.json()['auth_token']
            url = self.fb_zbm_base_url

        headers = {
            'Content-Type': 'application/json', 
            'x-zerto-session': auth_token
            }
        
        response = requests.get(f'https://{url}/v1/vpgs', headers=headers, verify=False)
        vpg_list = []
        for vpg in response.json():
            vpg_list.append(vpg['VpgIdentifier'])
        #print("Total VPGs:", len(vpg_list))

        return vpg_list

        

    def get_peer_all_sites(self, auth_token):

        if self.site == "SGU":
            url = self.sgu_zvm_base_url
        if self.site == 'BOI':
            url = self.boi_zvm_base_url
        if self.site == 'FB':
            url = self.fb_zbm_base_url

        headers = {
            'Content-Type': 'application/json',
            'x-zerto-session': auth_token
        }
        response = requests.get(f'https://{url}/v1/peersites', headers=headers, verify=False)
        self.site_list = []
        for site in response.json():
            
            self.site_list.append(site['PeerSiteName'])
        print("Total Peer Sites:", len(self.site_list))
        return self.site_list
    

    def get_vpg_statuses(self, auth_token):
        if self.site == "SGU":
            url = self.sgu_zvm_base_url
        if self.site == 'BOI':
            url = self.boi_zvm_base_url
        if self.site == 'FB':
            url = self.fb_zbm_base_url

        headers = {
            'Content-Type': 'application/json',
            'x-zerto-session': auth_token
        }
        response = requests.get(f'https://{url}/v1/vpgs/statuses', headers=headers, verify=False)

        return response.json()

    def get_single_vpg_info(self, auth_token, vpg):
        if self.site == "SGU":
            url = self.sgu_zvm_base_url
        if self.site == 'BOI':
            url = self.boi_zvm_base_url
        if self.site == 'FB':
            url = self.fb_zbm_base_url

        headers = {
            'Content-Type': 'application/json',
            'x-zerto-session': auth_token
        }
        response = requests.get(f'https://{url}/v1/vpgs/{vpg}', headers=headers, verify=False)

        return response.json()
    
    def close_session(self, auth_token):
        if self.site == "SGU":
            url = self.sgu_zvm_base_url
        if self.site == 'BOI':
            url = self.boi_zvm_base_url
        if self.site == 'FB':
            url = self.fb_zbm_base_url

        headers = {
            'Content-Type': 'application/json',
            'x-zerto-session': auth_token
        }
        response = requests.delete(f'https://{url}/v1/session', headers=headers, verify=False)
        if response.status_code == 200:
            print('Session closed successfully')
        else:
            print('Session failed to close')




