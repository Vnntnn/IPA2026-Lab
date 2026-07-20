"""
        Using Netmiko to config network devices
        - Config VLAN 101 for control/data plan on S1
        - Config OSPF on R1, R2 for control/data plan \
          All Interfaces (include loopback) are in Area 0 \
          except interface that connecting to NAT
        - Advertise default route to the NAT cloud on R2 into OSPF at R2
        - Config PAT on R2
        - Allow Telnet/SSH to R1-2 and S1 only from Management Plan IP Addresses \
          and the LAB306 Network
"""

from netmiko import ConnectHandler

# S1, R1, R2
NETWORK_DEVICES = [
        "172.31.14.3",
        "172.31.14.4",
        "172.31.14.5"
]

# SSH Username, Password with Hard Code
USERNAME = "admin"
PASSWORD = "cisco"

router1: dict = {
        'device_type': 'cisco_ios',
        'ip': NETWORK_DEVICES[1],
        'username': USERNAME,
        'password': PASSWORD
}

router2: dict = {
        'device_type': 'cisco_ios',
        'ip': NETWORK_DEVICES[2],
        'username': USERNAME,
        'password': PASSWORD
}

switch1: dict = {
        'device_type': 'cisco_ios',
        'ip': NETWORK_DEVICES[0],
        'username': USERNAME,
        'password': PASSWORD
}

def main() -> None:
        """
                Main: Running preset config from file and write memory to network device
        """
        for dev in switch1, router1, router2:
                net_connect = ConnectHandler(**dev)
                net_connect.send_config_from_file(config_file = f"config/{dev["ip"]}.config")
                net_connect.save_config()

if __name__ == "__main__":
        main()
