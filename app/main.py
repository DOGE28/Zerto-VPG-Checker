import routes
import time
import argparse

parser = argparse.ArgumentParser(description="Get the percentage of VPGs down for each site")
parser.add_argument("-s", "--site", help="Site to get VPG status for, if not specified, default is SGU")


start = time.time()
print("Initializing Zerto Object")

if parser.parse_args().site:
    zerto = routes.ZertoGet(site=parser.parse_args().site)
else:
    zerto = routes.ZertoGet(site="SGU")

print("Starting Authentication Process")

auth_token = zerto.login()


print("Getting Response from Zerto Server")

# Get SourceSite for each VPG
#Dict of single site and VPG status format: {site_name: {vpgs_up: up, vpgs_down: down}}
#List of all sites and their VPG statuses.
#The status of each VPG is either "up" or "down" and is determined by the "Status" key in the response.

def get_site_vpg_status(auth_token):
    site_vpg_status = {}
    vpgs = zerto.get_all_vpg_names(auth_token)
    sites = zerto.get_peer_all_sites(auth_token)
    count = 1
    for site in sites:
        #print(count, site)
        #count += 1
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
    if zerto.site == 'FB' or 'BOI':
        pass
    else:
        dumb = site_vpg_status['3form']["vpgs_up"]
        site_vpg_status['3form']["vpgs_up"] = dumb + 1

    return site_vpg_status

def get_percent_down(site_vpg_status):
    site_list = []
    for key, value in site_vpg_status.items():
        sites_down = {}
        total_vpgs = value['vpgs_up'] + value['vpgs_down']
        
        if total_vpgs == 0:
            #print(key, ": 0%")
            continue
        
        percent_down = (value['vpgs_down'] / total_vpgs) * 100
        sites_down[key] = f'{percent_down}% Down'
        site_list.append(sites_down)
        
        #print(key, "|", "Total VPGs:", total_vpgs, "|", f'{round(percent_down)}', "%", "down")
        #print(total_vpgs)
    print(site_list)
    return site_list


get_percent_down(get_site_vpg_status(auth_token))
zerto.close_session(auth_token)

end = time.time()
print("Time taken:", end-start)