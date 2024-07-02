import routes
import time

start = time.time()
print("Initializing Zerto Object")

zerto = routes.ZertoGet(site="SGU")

print("Starting Authentication Process")

auth_token = zerto.login()

print("Getting Response from Zerto Server")

# Get SourceSite for each VPG
#Dict of single site and VPG status format: {site_name: name, vpgs_up: up, vpgs_down: down}
#List of all sites and their VPG statuses.
#The status of each VPG is either "up" or "down" and is determined by the "Status" key in the response.

def get_site_vpg_status(auth_token):
    site_vpg_status = {}
    vpgs = zerto.get_all_vpg_names(auth_token)
    sites = zerto.get_peer_all_sites(auth_token)
    count = 1
    for site in sites:
        print(count, site)
        count += 1
        site_vpg_status[site] = {"vpgs_up": 0, "vpgs_down": 0}
    for vpg in vpgs:
        response = zerto.get_single_vpg_info(auth_token, vpg)
        for key, value in site_vpg_status.items():
            if response['TargetSite'] == 'Tonaquint-BOI':
                if response['TargetSite'] == key:
                    if response['Status'] == 0 or 1:
                        site_vpg_status[key]["vpgs_up"] += 1
                    else:
                        site_vpg_status[key]["vpgs_down"] += 1
            if response['SourceSite'] == key:
                #print(vpg, site)
                if response['Status'] == 0 or 1:
                    site_vpg_status[key]["vpgs_up"] += 1
                else:
                    site_vpg_status[key]["vpgs_down"] += 1
                #print(site_vpg_status)
    dumb = site_vpg_status['3form']["vpgs_up"]
    site_vpg_status['3form']["vpgs_up"] = dumb + 1
    return site_vpg_status

print(get_site_vpg_status(auth_token))
end = time.time()
print("Time taken:", end-start)

