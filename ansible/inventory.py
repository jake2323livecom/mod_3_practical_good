#!/usr/bin/env python3

import requests
import json

query_id = 'a5290bd3-c1c4-41b5-9ec3-2954d1134359'
nautobot_token = '99959315b2c64f730610cc44085840b4ff5d75be'
api_url = f'https://192.168.128.15/api/extras/graphql-queries/{query_id}/run/'

headers = {
    'Application': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Token {nautobot_token}'
}

result = requests.post(api_url, headers=headers, verify=False).json()

devices = result['data']['devices']
tenant_groups = result['data']['tenant_groups']
tenants = result['data']['tenants']
device_roles = result['data']['device_roles']
platforms = result['data']['platforms']

final_devices = {
    '_meta': {
        'hostvars': {
            device['name']: {
                'ansible_host': device['primary_ip4']['host'],
                'device_type': device['device_type']['model'],
            }
            for device in devices
        }
    }

}


final_device_roles = {
    role['name']: {
        'hosts': [device['name'] for device in role['devices']]
    }
    for role in device_roles
}

final_platforms = {
    platform['name']: {
        'hosts': [device['name'] for device in platform['devices']]
    }
    for platform in platforms
}

custom_groups = {
    'all_routers': {
        'children': [role for role in final_device_roles.keys() if 'router' in role]
    },
    'all_switches': {
        'children': [role for role in final_device_roles.keys() if 'switch' in role]
    }
}

# Create empty inventory and add the hostvars
final_inventory = {}
final_inventory.update(final_devices)

# Combine all groups into a single groups dictionary
groups = {}
groups.update(final_device_roles)
groups.update(final_platforms)
groups.update(custom_groups)

# Add the master groups dictionary to the inventory
final_inventory.update(groups)

# Print the inventory to STDOUT
print(json.dumps(final_inventory))