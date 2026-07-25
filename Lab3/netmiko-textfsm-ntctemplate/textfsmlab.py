"""
    Auto-generate interface descriptions for R1, R2 and S1 from CDP.

    `show cdp neighbors` is parsed with textfsm / ntc-templates to learn which
    Cisco device sits on each local interface, then each interface is described:

      * Cisco <-> Cisco link  -> "Connect to <remote-intf> of <remote-device>"
      * Link to a PC          -> "Connect to PC"        (no CDP neighbor)
      * DHCP client uplink    -> "Connect to WAN"       (R2 g0/3)

    The description logic is pure (unit-tested in test_textfsm.py); main()
    pushes it to the live devices over SSH with netmiko.

    NOTE: named textfsmlab.py, not textfsm.py -- a module called textfsm.py
    would shadow the textfsm library that ntc-templates imports.
"""

import re

from ntc_templates.parse import parse_output
from netmiko import ConnectHandler


# --- description logic (pure, testable) --------------------------------------

def short_interface(name: str) -> str:
    """"GigabitEthernet0/1" / "Gig 0/1" / "g0/1" -> "G0/1"."""
    m = re.match(r"\s*([A-Za-z])[A-Za-z]*\s*(\d.*)", name.strip())
    return f"{m.group(1).upper()}{m.group(2)}" if m else name.strip()


def parse_cdp_neighbors(cdp_output: str) -> list[dict]:
    """Parse `show cdp neighbors` with ntc-templates (cisco_ios textfsm)."""
    return parse_output(
        platform="cisco_ios", command="show cdp neighbors", data=cdp_output
    )


def cdp_descriptions(cdp_output: str) -> dict[str, str]:
    """Map short local interface -> "Connect to <remote-intf> of <device>"."""
    descriptions = {}
    for entry in parse_cdp_neighbors(cdp_output):
        local = short_interface(entry["local_interface"])
        remote = short_interface(entry["neighbor_interface"])
        device = entry["neighbor_name"].split(".")[0]  # strip any domain
        descriptions[local] = f"Connect to {remote} of {device}"
    return descriptions


def interface_descriptions(
    cdp_output: str,
    interfaces: list[str],
    wan_interfaces=(),
) -> dict[str, str]:
    """Description for every interface, applying the three topology rules."""
    cdp = cdp_descriptions(cdp_output)
    wan = {short_interface(w) for w in wan_interfaces}
    result = {}
    for intf in interfaces:
        key = short_interface(intf)
        if key in cdp:
            result[key] = cdp[key]
        elif key in wan:
            result[key] = "Connect to WAN"
        else:
            result[key] = "Connect to PC"
    return result


# --- live device configuration (control/data plane over SSH) -----------------

USERNAME = "admin"
PASSWORD = "cisco"
SSH_CONFIG = "config_ssh"

# ip, interfaces to describe, and which of them is the DHCP/WAN uplink.
# Interfaces come from the netmiko-jinja2 lab topology data.
DEVICES = {
    "S1": {"ip": "172.31.14.3", "interfaces": ["g0/1", "g0/2"], "wan": []},
    "R1": {"ip": "172.31.14.4", "interfaces": ["g0/1", "g0/2"], "wan": []},
    "R2": {"ip": "172.31.14.5", "interfaces": ["g0/1", "g0/2", "g0/3"], "wan": ["g0/3"]},
}


def devices_model(ip: str) -> dict:
    """netmiko connection dict (same pattern as the netmiko-jinja2 lab)."""
    return {
        "device_type": "cisco_ios",
        "ip": str(ip),
        "username": USERNAME,
        "password": PASSWORD,
        "ssh_config_file": SSH_CONFIG,
        "conn_timeout": 30,
        "fast_cli": False,
    }


def config_lines(descriptions: dict[str, str]) -> list[str]:
    """Turn a description map into interface config lines."""
    lines = []
    for intf, desc in descriptions.items():
        lines.append(f"interface {intf}")
        lines.append(f" description {desc}")
    return lines


def config_device(device_name: str, device: dict) -> None:
    """Read CDP off a live device and push generated descriptions."""
    print(f"Connecting to {device_name}...")
    net_connect = ConnectHandler(**devices_model(device["ip"]))

    cdp_output = net_connect.send_command("show cdp neighbors")
    descriptions = interface_descriptions(
        cdp_output, device["interfaces"], wan_interfaces=device["wan"]
    )

    print(f"Applying descriptions on {device_name}:")
    for intf, desc in descriptions.items():
        print(f"    {intf}: {desc}")

    net_connect.send_config_set(config_lines(descriptions), read_timeout=90)
    net_connect.save_config()
    net_connect.disconnect()
    print(f"Successfully finished {device_name}!\n")


def main() -> None:
    for device_name, device in DEVICES.items():
        config_device(device_name, device)


if __name__ == "__main__":
    main()
