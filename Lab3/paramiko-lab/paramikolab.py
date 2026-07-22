"""
	Get running-config from router 0 with Paramiko,
	And backup to local repository
"""

import paramiko
import time
from pathlib import Path
from collections.abc import Sequence

# Backup file directory
BACKUP_DIR = Path(__file__).parent / "backup"

# Username, Password to SSH to router
USERNAME = "admin"
PASSWORD = "cisco"

# Router IP (Sort ascending from R0 - R2)
ROUTERS_IP = [ 
	"172.31.14.1",
	"172.31.14.4",
	"172.31.14.5" 
]
# Switch IP
SWITCHES_IP = [ 
	"172.31.14.2",
	"172.31.14.3"
]

def get_running_config(
		device_ip: Sequence[str],
		device_type: str
	) -> None:
	"""Get device running config from switch or router"""

	device_type = device_type.lower()
	device_type_uppercase: str = device_type.upper()
	alias: str = "SW" if device_type == "switch" else "R"
	backup_path = BACKUP_DIR / device_type
	backup_path.mkdir(parents=True, exist_ok=True)

	for index, device in enumerate(device_ip, start=1):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=device, username=USERNAME, password=PASSWORD, look_for_keys=False)

		print(f"Connecting to {device_type_uppercase} IP: {device}, please wait...")

		try:
			with client.invoke_shell() as ssh:
				print(f"Connected to {device_type_uppercase} IP: {device}")

				# Make output of Cisco IOS fully visible
				ssh.send("terminal length 0\n")
				time.sleep(1)
				# Show device running config
				ssh.send("show running-config\n")
				time.sleep(3)
				config = ssh.recv(65536).decode("utf-8")

				# Save running config as file
				with open(backup_path / f"{alias}{index}_{device}", "w", encoding="utf-8") as file:
					print("Saving running config to local repository...")
					file.write(config)
		finally:
			client.close()

		print(f"Done for {device_type_uppercase} IP: {device}")

def main() -> None:
	"""Main Function"""
	# Switch running config backup
	get_running_config(SWITCHES_IP, "switch")

	# Router running config backup
	get_running_config(ROUTERS_IP, "router")

if __name__ == "__main__":
	main()
