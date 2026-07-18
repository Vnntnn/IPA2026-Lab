"""
    	Get running-config from router 0 with Paramiko,
		And backup to local repository
"""

import paramiko
import time
from pathlib import Path

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

def main() -> None:
	"""Main Function"""
	# Switch running config backup
	for INDEX, SWITCH in enumerate(SWITCHES_IP):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=SWITCH, username=USERNAME, password=PASSWORD, look_for_keys=False)

		print("=" * 60)
		print("Connecting to Switch IP: ", SWITCH, ", Please waiting...")
		print("=" * 60)

		with client.invoke_shell() as ssh:
			print("=" * 60)
			print("Connected to Switch IP: ", SWITCH)
			print("=" * 60)

			# Make output of Cisco IOS not pressing any button to show more
			ssh.send("terminal length 0\n")
			time.sleep(1)
			# Show device running config
			ssh.send("show running-config\n")
			time.sleep(3)
			config = ssh.recv(65536).decode("utf-8")
			# Save running config as file
			(BACKUP_DIR / "switch").mkdir(parents=True, exist_ok=True)
			with open(BACKUP_DIR / "switch" / f"SW{INDEX + 1}_{SWITCH}", "w") as file:
				print("Saving running config to local repository...")
				file.write(config)

			print("Done for Switch IP: ", SWITCH)

	# Router running config backup
	for INDEX, ROUTER in enumerate(ROUTERS_IP):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=ROUTER, username=USERNAME, password=PASSWORD, look_for_keys=False)

		print("=" * 60)
		print("Connecting to Router IP: ", ROUTER, ", Please waiting...")
		print("=" * 60)

		with client.invoke_shell() as ssh:
			print("=" * 60)
			print("Connected to Router IP: ", ROUTER)
			print("=" * 60)

			# Make output of Cisco IOS not pressing any button to show more
			ssh.send("terminal length 0\n")
			time.sleep(1)
			# Show device running config
			ssh.send("show running-config\n")
			time.sleep(3)
			config = ssh.recv(65536).decode("utf-8")
			# Save running config as file
			(BACKUP_DIR / "router").mkdir(parents=True, exist_ok=True)
			with open(BACKUP_DIR / "router" / f"R{INDEX + 1}_{ROUTER}", "w") as file:
				print("Saving running config to local repository...")
				file.write(config)

			print("Done for Router IP: ", ROUTER)

if __name__ == "__main__":
	main()
