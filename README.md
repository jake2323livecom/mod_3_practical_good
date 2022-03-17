# mod_3_practical

## Topics to cover:
- python
- api calls
- yaml/json
- ansible

## Build device configuration files with Ansible :D

- clone the exam repo to your machine and go to that directory
- create a new branch from the development branch
- install ansible
- create hosts.ini file for inventory
    - create group called 'routers'
        - define 4 hosts:
            - router_1 with primary ip address of 1.1.1.1
            - router_2 with primary ip address of 2.2.2.2
            - router_3 with primary ip address of 3.3.3.3
            - router_4 with primary ip address of 4.4.4.4
    - create group called 'switches'
        - define 4 hosts
            - switch_1 with primary ip of 172.16.1.1
            - switch_2 with primary ip of 172.16.1.2
            - switch_3 with primary ip of 172.16.1.3
            - switch_4 with primary ip of 172.16.1.4
    - define group 'all'
        - make routers and switches child groups of 'all'

- create a folder to store files for group variables
    - create a json file for the group all
        - define a variable called 'dns_servers' and set it to this list of IPs: 8.8.8.8, 8.8.4.4
    - create json file for routers
        - define a variable called management_interface and set it to Loopback0
        - define a variable called device_type and set it equal to 'router'
    - create json file for switches
        - define a variable called management_interface and set it to Vlan1000
        - define a variable called device_type and set it equal to 'switch'

- In base.j2, fill in the empty variable call after 'hostname' on the first line

- create template to generate interface configurations
    - using a for loop, create four physical interfaces
        - resulting interface numbers should be 0/0, 0/1, 0/2, 0/3
        - set the interface type to 'Ge' if the device_type is 'router' else 'Fe'.
        - For a router, the output would be Ge0/0, Ge0/1, Ge0/2, Ge0/3
        - for a switch, the output would be Fe0/0, Fe0/1, Fe0/2, Fe0/3
        - for the sake of simplicity, set the ip address of each interface to 5.5.5.5 255.255.255.0

- create template to generate the configuration for dns servers
    - using a for loop, create a line that contains the IP address of each server in the dns_servers variable
    - make sure to keep it to one line
    - example:
        - ip name-server 8.8.8.8 8.8.4.4

- finish the template to generate the management interface configuration
    - fill in the empty variable calls with the appropriate variables
    - the management interface's IP address should be the primary IP address of the host
    - the subnet mask should be 255.255.255.255 if the device_type is router, otherwise it should be 255.255.255.0

- import the dns_servers.j2, physical_interfaces.j2, and management_interface.j2 templates into the base template
- finish the playbook called build.yml
    - configure the playbook so that localhost is responsible for carrying it out
    - set start_time variable
    - create a directory to store device config files using the start_time variable in the name
    - generate device config files and store in the directory you created
        - store in .cfg file
        - put the device hostname in the name of it's config file
        - set the playbook to continue if the task fails
    - use scp to send configs to a remote server
        - set the playbook to continue if the task fails
    - delete the original directory
- Run the playbook
    - pass in an extra variable called syslog_server and set the value equal to 10.10.10.10
- Commit the changes to your branch

