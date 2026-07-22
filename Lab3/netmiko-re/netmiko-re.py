"""
        Checking and display all the active interfaces on r1, r2
        and their uptime using REGEX.
"""

from netmiko import ConnectHandler
import re

# Network device credential
USERNAME = "admin"
PASSWORD = "cisco"
SSH_CONFIG = "config_ssh"
DEVICES: dict = {
        "router1": "172.31.14.4",
        "router2": "172.31.14.5"
}

def devices_model(
                ip: int | str
        ) -> dict:
        """
                Create device model to extract connection
        """
        return {
                'device_type': 'cisco_ios',
                'ip': str(ip),
                'username': USERNAME,
                'password': PASSWORD,
                'ssh_config_file': SSH_CONFIG,
                'conn_timeout': 30,
                'fast_cli': False
        }

def get_device_status(
                device_data: dict,
                device_name: str,
        ) -> None:
        """
                Get network device status (Active interface, Uptime)
        """
        print(f"Connecting to {device_name}...")
        net_connect = ConnectHandler(**device_data)

        status = net_connect.send_command('show ip interface brief | include up')
        format_status = status.split('\n')
        if format_status:
                print(f"Active {len(format_status)} interface(s):\n", end="")
                for index, line in enumerate(format_status):
                        name = line.strip().split()[0]
                        print(f"\t{index + 1}.{name} is up.")
        else:
                print("No any interface(s) is up.")

        uptime = net_connect.send_command(f"show version | include uptime")
        print(f"Device {device_name} Uptime: {re.search(" \d+ \w+", uptime)}")

        net_connect.disconnect()
        print(f"Successfully finished status report in {device_name}!\n")

def main() -> None:
        """
                Main function
        """
        for device, ip in DEVICES.items():
                get_device_status(devices_model(ip), device)

if __name__ == "__main__":
        main()
