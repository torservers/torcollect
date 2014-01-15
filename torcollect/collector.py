#-*- coding: utf-8 -*-

##########################################################
# © 2011 Daniel 'grindhold' Brendle with torservers.net
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

import paramiko
import tempfile
import re

import torcollect.server
import torcollect.database
import torcollect.heartbeat

LOGPATH = "/var/lib/torcollect/"
NOTICEPATH = "/var/log/torcollect/"
NUMBERMATCH = re.compile("^\d*")
PATHSTRIP = re.compile("^[^ ]* ")


# TODO: See how to extract IPs of the bridges to log them
# TODO: Actually log individual Bridge-IPs

class ExitReason:
    OK = 0
    INVALID_CONFIG = 1


def collect():
    servers = torcollect.server.Server.get_server_list(full=True)

    country_data = {}
    transports_data = {}
    traffic_data = {}
    for server in servers:
        # Establish SSH connection
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if server.get_login_type() == torcollect.server.LoginType.PASSWORD:
            ssh_connection.connect(server.get_ip(), server.get_port(),
                                   server.get_username(),
                                   server.get_password())
        else:
            keyfile = tempfile.NamedTemporaryFile("w")
            keyfile.write(server.get_keyfile())
            keyfile.flush()
            ssh_connection.connect(server.get_ip(),
                                   port=server.get_port(),
                                   username=server.get_username(),
                                   password=server.get_password(),
                                   key_filename=keyfile.name)

        # Acquire information
        #  - Acquire country-related information
        con_stdin, con_stdout, con_stderr = ssh_connection.exec_command(
            'grep -r bridge-ips %s 2> /dev/null' % LOGPATH)
        country_data[server] = con_stdout.read().split("\n")
        #  - Acquire transport-related information
        con_stdin, con_stdout, con_stderr = ssh_connection.exec_command(
            'grep -r bridge-ip-transports %s 2> /dev/null' % LOGPATH)
        transports_data[server] = con_stdout.read().split("\n")
        #  - Acquire traffic-related information
        # Grep every Heartbeat-line from the notices-files that are from yesterday
        # and the day before yesterday.
        # The day before yesterday is necessary because we need a reference point
        # to calculate the difference from todays traffic to get the traffic that
        # has been transported.
        command = 'TC_ONEDAYAGO="$(date --date="1 day ago" +"%%b %%d")" ; \
                   TC_TWODAYAGO="$(date --date="2 days ago" +"%%b %%d")" ; \
                   grep Heartbeat %snotices* 2> /dev/null | grep -P "$TC_ONEDAYAGO|$TC_TWODAYAGO"'  
        con_stdin, con_stdout, con_stderr = ssh_connection.exec_command(
            command % LOGPATH)
        traffic_data[server] = con_stdout.read().split("\n")
        traffic_data[server].remove('')
        if server.get_login_type() == torcollect.server.LoginType.PUBLICKEY:
            keyfile.close()
        ssh_connection.close()

    # Declare SQL stmnts

    # insert bridge statement
    ib_stmnt = "DO\
                $BODY$\
                BEGIN\
                IF NOT EXISTS (SELECT BRG_ID FROM Bridge WHERE \
                       BRG_NR = %(brg_nr)d AND BRG_SRV_ID = %(brg_srv_id)d)\
                THEN \
                    INSERT INTO Bridge (BRG_NR, BRG_IP, BRG_SRV_ID) \
                    VALUES (%(brg_nr)d, %(brg_ip)s, %(brg_srv_id)d); \
                END IF;\
                END;\
                $BODY$;"

    # get bridge id statement
    sb_stmnt = "SELECT BRG_ID FROM Bridge WHERE BRG_NR = %(brg_nr)d\
                AND BRG_SRV_ID = %(brg_srv_id)d ;"

    # create report statement
    cr_stmnt = "DO\
                $BODY$\
                BEGIN\
                IF NOT EXISTS (SELECT REP_ID FROM Report WHERE \
                    REP_DATE = DATE 'today' AND REP_BRG_ID = %(brg_id)d) \
                THEN \
                    INSERT INTO Report (REP_BRG_ID , REP_DATE, REP_PORT ) \
                    VALUES (%(brg_id)d, DATE 'today', %(port)d); \
                END IF;\
                END;\
                $BODY$;"

    # get report id statement
    sr_stmnt = "SELECT REP_ID FROM Report WHERE REP_DATE = DATE 'today' \
                AND REP_BRG_ID = %(brg_id)d;"

    # create countryreport statement
    ccr_stmnt = "INSERT INTO CountryReport (CRP_REP_ID, CRP_CCO_ID, \
                        CRP_USERS ) \
                 VALUES ( %(rep_id)d, COALESCE(\
                         (SELECT CCO_ID FROM CountryCode WHERE \
                                       CCO_SHORT = %(cco_short)s) \
                          , -1), \
                          %(users)d);"

    # create transport statement
    ct_stmnt = "DO\
                $BODY$\
                BEGIN \
                IF NOT EXISTS (SELECT TRA_ID FROM Transport \
                    WHERE TRA_NAME = %(name)s) \
                THEN \
                    INSERT INTO Transport (TRA_NAME) VALUES (%(name)s);\
                END IF;\
                END;\
                $BODY$;"

    # create transportreport statement
    ctr_stmnt = "INSERT INTO TransportReport (TRP_REP_ID, TRP_TRA_ID, \
                        TRP_USERS) \
                 VAlUES ( %(rep_id)d, (SELECT TRA_ID FROM TRANSPORT \
                        WHERE TRA_NAME = %(tra_name)s), %(users)d);"

    # update traffic statement
    utr_stmnt = "UPDATE Report SET REP_TRAFFIC_SENT = %(rep_traffic_sent)d, \
                        REP_TRAFFIC_RECEIVED = %(rep_traffic_received)d \
                 WHERE REP_ID = %(rep_id)d;"

    db = torcollect.database.Database()
    cur = db.cursor()

    # parse loglines and create the database entries for the country-statistics
    for server, data in country_data.items():
        for line in data:
            stripped = line.replace(LOGPATH, "")
            numbermatch = NUMBERMATCH.match(stripped)
            if numbermatch and numbermatch.group(0) != '':
                bridge_number = int(numbermatch.group(0))
            else:
                continue

            cur.execute(ib_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id(),
                                   'brg_ip': "0.0.0.0"})
            cur.execute(sb_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id()})
            bridge_id = cur.fetchone()[0]
            cur.execute(cr_stmnt, {'brg_id': bridge_id,
                                   'port': 22})
            cur.execute(sr_stmnt, {'brg_id': bridge_id})
            report_id = cur.fetchone()[0]
            infoline = PATHSTRIP.sub('', stripped)
            if infoline == '':
                continue
            for stats in infoline.split(","):
                country, users = stats.split("=")
                cur.execute(ccr_stmnt, {'rep_id': report_id,
                                        'cco_short': country.upper(),
                                        'users': int(users)})
    db.commit()
    
    # parse loglines and create the database entries for the bridge-user statistics
    for server, data in transports_data.items():
        for line in data:
            stripped = line.replace(LOGPATH, "")
            numbermatch = NUMBERMATCH.match(stripped)
            if numbermatch and numbermatch.group(0) != '':
                bridge_number = int(numbermatch.group(0))
            else:
                continue

            cur.execute(ib_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id(),
                                   'brg_ip': "0.0.0.0"})
            cur.execute(sb_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id()})
            bridge_id = cur.fetchone()[0]
            cur.execute(cr_stmnt, {'brg_id': bridge_id,
                                   'port': 22})
            cur.execute(sr_stmnt, {'brg_id': bridge_id})
            report_id = cur.fetchone()[0]
            infoline = PATHSTRIP.sub('', stripped)
            if infoline == '':
                continue
            for stats in infoline.split(","):
                transport, users = stats.split("=")
                cur.execute(ct_stmnt, {'name': transport})
                cur.execute(ctr_stmnt, {'rep_id': report_id,
                                        'tra_name': transport,
                                        'users': int(users)})
    db.commit()

    # preparing traffic-related data
    for server, data in traffic_data.items():
        heartbeat_data = {}
        for line in data:
            heartbeat = torcollect.heartbeat.Heartbeat.parse(line)
            if not heartbeat_data.has_key(heartbeat.bridge_nr):
                heartbeat_data[heartbeat.bridge_nr] = []
            heartbeat_data[heartbeat.bridge_nr].append(heartbeat)
        traffic_data[server] = heartbeat_data

    for server, per_bridge_data in traffic_data.items():
        for bridge_number, data in per_bridge_data.items():
            sent, received = _get_sent_received(data)
            cur.execute(ib_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id(),
                                   'brg_ip': "0.0.0.0"})
            cur.execute(sb_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id()})
            bridge_id = cur.fetchone()[0]
            cur.execute(cr_stmnt, {'brg_id': bridge_id,
                                   'port': 22})
            cur.execute(sr_stmnt, {'brg_id': bridge_id})
            report_id = cur.fetchone()[0]

            cur.execute(utr_stmnt, {'rep_id': report_id,
                                    'rep_traffic_sent': sent,
                                    'rep_traffic_received': received})
    db.commit()


def _get_sent_received(data):
    # Determine the reference point, which is the with the dataset
    # with the highest "hours" and the lowest "day" in the timestamp
    reference_heartbeat = None
    newest_heartbeat = None
    for heartbeat in data:
        if reference_heartbeat is None and newest_heartbeat is None:
            # initially set reference heartbeat and newest heartbeat
            reference_heartbeat = heartbeat
            newest_heartbeat = heartbeat
            continue
        if heartbeat.timestamp < reference_heartbeat.timestamp or \
           (heartbeat.timestamp.day == reference_heartbeat.timestamp.day and \
            heartbeat.timestamp.hour > reference_heartbeat.timestamp.hour):
            # set reference hartbeat
            reference_heartbeat = heartbeat

        if heartbeat.timestamp > newest_heartbeat.timestamp:
            newest_heartbeat = heartbeat
    sent = newest_heartbeat.sent - reference_heartbeat.sent
    received = newest_heartbeat.received - reference_heartbeat.received
    return sent, received
