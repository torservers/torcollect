#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2013/2014 Daniel 'grindhold' Brendle with torservers.net
#
# This file is part of torcollect
#
# torcollect is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later
# version.
#
# torcollect is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with torcollect.
# If not, see http://www.gnu.org/licenses/.
###########################################################


import sys
import os
import datetime
import torcollect.server
import torcollect.collector
import torcollect.web
import torcollect.organization

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
 > -d <id>       -  remove an organization
 > list          -  list existing organizations
 > assign-bridge -  assign a bridge to an organization
   --bridge <bridge_id>
   --organization <organization_id>

 bridge         --  show information about bridges
 > list          -  list collected bridges

 help           --  show this help message
""" % sys.argv[0]

ACTIONS = ["collect",
           "server",
           "organization",
           "bridge",
           "generate",
           "help"]


def helptext():
    print HELPTEXT
    sys.exit(0)


def server_add(parameters):
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
        address = parameters[parameters.index("--address") + 1]
    if "--name" not in parameters:
        helptext()
    else:
        name = parameters[parameters.index("--name") + 1]
    if "--port" in parameters:
        port = parameters[parameters.index("--port") + 1]
    if "--user" not in parameters:
        helptext()
    else:
        user = parameters[parameters.index("--user") + 1]
    if "--password" not in parameters:
        helptext()
    else:
        password = parameters[parameters.index("--password") + 1]
    if "--keyfile" in parameters:
        keyfile_path = parameters[parameters.index("--keyfile") + 1]
        keyfile_content = open(os.path.expanduser(keyfile_path), "r").read()
    # Verify input
    server = torcollect.server.Server.create(address, name, port, user,
                                            password, keyfile_content)
    server.store()

def server_delete(parameters):
    if parameters[0] is not None:
        server = torcollect.server.Server.load(parameters[0])
        server.delete()
    else:
        helptext()

def server_list():
    server_list = torcollect.server.Server.get_server_list()
    for server in server_list:
        print "Name: %s :: %s" % (server.get_name(), server.get_ip())

def organization_add(parameters):
    if "--name" not in parameters:
        helptext()
    else:
        name = ""
        try:
            name = parameters[parameters.index("--name") + 1]
        except IndexError:
            helptext()
        o = torcollect.organization.Organization()
        o.set_name(name)
        o.store()
        print "Created Organization: %s"%name
        

def organization_delete(parameters):
    if len(parameters) > 0 and parameters[0] is not None:
        o = torcollect.organization.Organization.load(int(parameters[0]))
        o.delete()
        print "Deleted organization %s"%o.get_name()
    else:
        helptext()    

def organization_list():
    orglist = torcollect.organization.Organization.list()
    for org in orglist:
        print "Organization %(name)s (ID: %(id)d)"%org

def organization_assign(parameters):
    if len(parameters) == 4:
        try:
            brg_id = int(parameters[parameters.index("--bridge") + 1])
        except IndexError:
            helptext()
        try:
            org_id = int(parameters[parameters.index("--organization") + 1])
        except IndexError:
            helptext()
        o = torcollect.organization.Organization.load(org_id)
        o.disclose_bridge(brg_id)
    else:
        helptext()


def run(argv):
    try:
        action = argv[1]
    except IndexError:
        helptext()
    try:
        subaction = argv[2]
        parameters = argv[3:]
    except IndexError:
        pass
    if action not in ACTIONS:
        helptext()
    elif action == "collect":
        torcollect.collector.collect()
    elif action == "server":
        if subaction == "add":
            server_add(parameters)
        elif subaction == "-d":
            server_delete(parameters)
        elif subaction == "list":
            server_list()
        else:
            helptext()
    elif action == "organization":
        if subaction == "add":
            organization_add(parameters)
        elif subaction == "-d":
            organization_delete(parameters)
        elif subaction == "list":
            organization_list()
        elif subaction == "assign-bridge":
            organization_assign(parameters)
    elif action == "bridge":
        pass  # do bridge listings
    elif action == "generate":
        torcollect.web.generate_main_page()
        torcollect.web.generate_report_for_day(datetime.date.today())
    elif action == "help":
        helptext()
