#!/usr/bin/env python3

import requests
import json

query_id = 'a5290bd3-c1c4-41b5-9ec3-2954d1134359'
nautobot_token = '99959315b2c64f730610cc44085840b4ff5d75be'
devices_url = 'https://192.168.128.15/api/dcim/devices?site=orko_mod_3_practical'


headers = {
    'Application': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Token {nautobot_token}'
}

devices = requests.get(devices_url, headers=headers, verify=False).json()['results']

hostvars = {
    '_meta': {
        'hostvars': {
            device['name']: {
                'ansible_host': device['primary_ip4']['address'],
                'device_type': device['device_type']['model']
            }
            for device in devices
        }
    }
}

groups = {
    'red_devices': {
        'hosts': [device['name'] for device in devices if device['platform']['name'] == 'orko_red']
    },
    'yellow_devices': {
        'hosts': [device['name'] for device in devices if device['platform']['name'] == 'orko_yellow']
    },
    'routers': {
        'hosts': [device['name'] for device in devices if device['device_role']['name'] == 'orko_router']
    },
    'switches': {
        'hosts': [device['name'] for device in devices if device['device_role']['name'] == 'orko_switch']
    }
}

inventory = {}
inventory.update(hostvars)
inventory.update(groups)

print(json.dumps(inventory))