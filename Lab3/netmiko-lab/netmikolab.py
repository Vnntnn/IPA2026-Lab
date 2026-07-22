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

USERNAME = "admin"
PASSWORD = "cisco"
SSH_CONFIG = "config_ssh"

def devices_model(ip: int) -> dict:
        """Create device model to extract connection"""
        return {
                'device_type': 'cisco_ios',
                'ip': str(ip),
                'username': USERNAME,
                'password': PASSWORD,
                'ssh_config_file': SSH_CONFIG,
                'conn_timeout': 30,
                'fast_cli': False
        }

def main() -> None:
        """
        Main: Running preset config from file and write memory to network device
        """
        for dev in NETWORK_DEVICES:
                print(f"Connecting to {dev}...")
                net_connect = ConnectHandler(**devices_model(dev))

                config_file_path = f"config/{dev}.config"
                print(f"Applying config on {dev} from {config_file_path}...")

                config = net_connect.send_config_from_file(
                        config_file=config_file_path,
                        read_timeout=90
                )
                print(config)

                print(f"Saving config on {dev}...")
                net_connect.save_config()
                net_connect.disconnect()
                print(f"Successfully finished {dev}!\n")

if __name__ == "__main__":
        main()
