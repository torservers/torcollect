import pgdb
import paramiko
import json
import os
import sys

CONFIG = os.path.join("/","etc","torcollect","torcollect.conf")

class ExitReason:
    OK = 0
    INVALID_CONFIG = 1

try:
    configfile = open(CONFIG,"r")
    configuration = json.loads(configfile.read())
except ValueError:
    print("Could not parse config. Must be proper JSON")
    sys.exit(ExitReason.INVALID_CONFIG)

connection = pgdb.connect("localhost")

retrieved_data = {}
for server in configuration['servers']:
    # Establish SSH connection
    ssh_connection = paramiko.SSHClient()
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connection.connect(server['ip'], server['port'], 
                           server['user'], server['pw'])

    # Acquire information
    con_stdin, con_stdout, con_stderr = ssh_connection.exec_command(
                                                        'grep -r "bridge-ips"')
    received_data[server['ip']] = con_stdout.read()

for ip, data in retrieved_data.items():
    pass


