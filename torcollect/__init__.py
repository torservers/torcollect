#!/usr/bin/python
#-*- coding: utf-8 -*-

#######################################
# Torcollect
# Released under BSD License
# By Daniel 'grindhold' Brendle
#######################################

#######################################
#
# This script should be called on a
# regular basis (24h) to collect
# data from the servers running bridges
#
#######################################

import sys
import torcollect.server

HELPTEXT = """
Collect statistics about TOR-Relays

%s <action> <parameters>

actions:

 collect        --  collect data ( to be called every 24h )

 server         --  edit information about servers
 › add           -  add a new server
   --name <name>
   --address <address>
   --port <port>
   --user <username>
   --password <password>
  [--keyfile <path>]
 › -d <address>  -  remove a server
 > list          -  list existing servers

 organization   --  edit information about organizations
 > add           -  add a new organization
   --name <name>
 > -d <name>     -  remove an organization
 > list          -  list existing organizations
 > assign-bridge <bridge_identifier>:<address>
                 -  assign a bridge to an organization

 bridge         --  show information about bridges
 > list          -  list collected bridges
 
 help           --  show this help message
"""

ACTIONS = ["collect",
           "server",
           "organization",
           "bridge",
           "help"]

def helptext():
    print HELPTEXT
    sys.exit(0)

def run(argv):
    action = argv[1]
    subaction = argv[2]
    parameters = argv[3:]
    if action not in ACTIONS:
        helptext()
    elif action == "collect":
        pass #do collectings
    elif action == "server":
        if subaction == "add":
            address = None
            name = None
            port = 22
            user = None
            password = None
            keyfile_path = None
            keyfile_content = None
            if "--address" not in parameters:
                helptext()
            else:
                address = parameters[parameters.index("--address")+1]
            if "--name" not in parameters:
                helptext()
            else:
                name = parameters[parameters.index("--name")+1]
            if "--port" in parameters:
                port = parameters[parameters.index("--port")+1]
            if "--user" not in parameters:
                helptext()
            else:
                user = parameters[parameters.index("--user")+1]
            if "--password" not in parameters:
                helptext()
            else:
                password = parameters[parameters.index("--password")+1]
            if "--keyfile" in parameters:
                keyfile_path = parameters[parameters.index("--keyfile")+1]
                keyfile_content = open(keyfile_path,"r").read()

            # Verify input
            server = torcollect.server.Server.create(address,name,port,password,keyfile_content)
            server.store()

        elif subaction == "-d":
            if parameters[0] is not None:
                torcollect.server.Server.load(parameters[0])
            else:
                helptext()
        elif subaction == "list":
            server_list = torcollect.server.Server.get_server_list()
            for server in server_list:
                print "Name: %s :: %s"%(server.get_name(),server.get_ip())
        else:
            helptext()
    elif action == "organization":
        pass #do of organizations editings
    elif action == "bridge":
        pass #do bridge listings
    elif action == "help":
        helptext()

