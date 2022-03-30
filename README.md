# mod_3_practical

## Topics to cover:
- python
- api calls
- yaml/json
- ansible

## Build device configuration files with Ansible

- Clone the exam repo to your machine and go to that directory
- Create a new branch from the development branch
- Install ansible
- Using ansible-galaxy, install the netcommon collection
- Configure the ansible config file to allow inventory scripts to be used as inventory sources
- Finish the 'inventory.py' dynamic inventory file

    - Use API calls to Nautobot to pull necessary information

    - The resulting inventory should include:
        - A hostvars section containing every device from the 'orko' site in Nautobot.
            - Each device should have the ansible_host variable and device_type variable
        - A group of devices that have a device_role of 'router' in Nautobot. Name the group 'routers'.
        - A group of devices that have a device_role of 'switch' in Nautobot. Name the group 'switches'.
        - A group of devices that have a platform of 'red' in Nautobot. Name the group 'red_devices'.
        - A group of devices that have a platform of 'yellow' in Nautobot.  Name the group 'yellow_devices'.

    - Print the inventory to STDOUT in JSON format

- Create a folder to store files for group variables

    - Create a JSON file for the 'red_devices' group 
        - Define a variable called 'dns_servers' and set it to this list of IPs: 10.10.20.98, 10.10.20.99

    - Create a JSON file for the 'yellow_devices' group
        - Define a variable called 'dns_servers' and set it to this list of IPs: 10.10.30.98, 10.10.30.99

    - Create a JSON file for the 'routers' group
        - Define a variable called 'management_interface' and set it to 'Loopback0'

    - Create JSON file for the 'switches' group
        - Define a variable called 'management_interface' and set it to 'Vlan1000'

- In base.j2, fill in the empty variable call after 'hostname' on the first line using an ansible special variable

- Finish the 'physical_interfaces.j2' template to generate the configuration for all physical interfaces
    - Loop through the 'interfaces' variable defined in the 'all.json' group_vars file
    - Configure each interface's IP address and subnet mask
        - Use the appropriate data from the 'interfaces' variable

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

