"""
        Config network device like previous netmiko lab \
        But using template engine (Jinja2) for render config from template
        No AI using. Human write
"""

from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import yaml

# Essential directory
TEMPLATE_DIR: str = Path(__file__).parent / "templates"
DATA_DIR: str = Path(__file__).parent / "data"
CONFIG_DIR: str = Path(__file__).parent / "config"
# Network Device config template
SW_TEMPLATE_FILE: str = "switch.j2"
ROUTER_TEMPLATE_FILE: str = "router.j2"
# Template env
ENV: Environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True
)

# Network device credential
USERNAME = "admin"
PASSWORD = "cisco"
SSH_CONFIG = "config_ssh"
DEVICES: dict = {
        "switch1": "172.31.14.3",
        "router1": "172.31.14.4",
        "router2": "172.31.14.5"
}

def load_env_template(
                template_file: str
        ) -> Template:
        """
                Load template jinja2 from env
                @params:
                        first: network device template file
        """
        return ENV.get_template(template_file)

def load_yaml_data(
                path: str
        ) -> dict:
        """
                Load yaml config data file
                @params:
                        first: yaml file data path
        """
        with open(path) as f:
                return yaml.safe_load(f)

def write_render_template(
                path: str,
                template: Template,
                data: dict
        ) -> None:
        """
                Write render config template file to machine with utf-8 encoding
        """
        with open(path, 'w', encoding="utf-8") as f:
                f.write(template.render(data))

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

def config_device(
                device_data: dict,
                device_name: str,
                config_file_path: str
        ) -> None:
        """
                Config network device using netmiko
        """
        print(f"Connecting to {device_name}...")
        net_connect = ConnectHandler(**device_data)

        print(f"Applying config on {device_name} from {config_file_path}...")

        config = net_connect.send_config_from_file(
                                config_file=config_file_path,
                                read_timeout=90
        )
        print(config)

        print(f"Saving config on {device_name}...")
        net_connect.save_config()
        net_connect.disconnect()
        print(f"Successfully finished {device_name}!\n")

def main() -> None:
        """
                Main Function
                Get jinja2 template to config file
                And using Netmiko to config device
        """
        for device, ip in DEVICES.items():
                template: Template = load_env_template(
                        ROUTER_TEMPLATE_FILE if "router" in device.lower() 
                        else SW_TEMPLATE_FILE
                )
                device_data: dict = load_yaml_data(f"{DATA_DIR}/{device}.yaml")
                write_render_template(CONFIG_DIR/ f"{device}.config", template, device_data)

                # Config device with Netmiko
                config_file_path = f"{CONFIG_DIR}/{device}.config"
                # config_device(devices_model(ip), device, config_file_path)

if __name__ == "__main__":
        main()
