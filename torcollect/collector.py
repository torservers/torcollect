import paramiko
import tempfile
import re

import torcollect.server
import torcollect.database

LOGPATH = "/var/lib/tor"
NUMBERMATCH = re.compile("^\d*")
PATHSTRIP = re.compile("^[^ ]* ")

class ExitReason:
    OK = 0
    INVALID_CONFIG = 1


def collect():
    servers = torcollect.server.Server.get_server_list(full=True)

    received_data = {}
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
            ssh_connection.connect(server.get_ip(), server.get_port(),
                                   server.get_username(), 
                                   server.get_password(),
                                   key_filename=keyfile.name)

        # Acquire information
        con_stdin, con_stdout, con_stderr = ssh_connection.exec_command(
            'grep -r bridge-ips /var/lib/tor 2> /dev/null')
        received_data[server] = con_stdout.read().split("\n")
        if server.get_login_type() == torcollect.server.LoginType.PUBLICKEY:
            keyfile.close()
        ssh_connection.close()

    # Declare SQL stmnts
    
    # insert bridge statement
    ib_stmnt = "IF \
                    (SELECT COUNT(BRG_ID) FROM Bridge \
                    WHERE BRG_NR = %(brg_nr)d \
                      AND BRG_SRV_ID = %(nrg_srv_id)d) = 0\
                 THEN \
                    INSERT INTO Bridge (BRG_NR, BRG_IP, BRG_SRV_ID) \
                    VALUES (%(brg_nr)d, %(brg_ip)s, %(brg_srv_id)d) \
                    RETURNING BRG_ID\
                 ELSE \
                    SELECT BRG_ID FROM Bridge \
                    WHERE BRG_NR = %(brg_nr)d \
                      AND BRG_SRV_ID = %(brg_srv_id)d;"
    
    # create report statement
    cr_stmnt = "INSERT INTO Report (REP_BRG_ID , REP_DATE, REP_PORT ) \
                VALUES (%(brg_id)d, DATE 'today', %(port)d) \
                RETURING REP_ID;"

    # create countryreport statement
    ccr_stmnt = "INSERT INTO CountryReport (CRP_REP_ID, CRP_CCO_ID, \
                        CRP_USERS ) \
                 VALUES ( %(rep_id)d, (SELECT CCO_ID FROM CountryCode WHERE \
                                       CCO_SHORT = %(cco_short)s), \
                          %(users)d);"

    db = torcollect.database.Database()
    cur = db.cursor()

    for server, data in received_data.items():
        for line in data:
            stripped = line.replace(LOGPATH,"")
            numbermatch = NUMBERMATCH.match(stripped)
            if numbermatch:
                bridge_number = int(numbermatch.group(0))
            else:
                continue

            cur.execute(ib_stmnt, {'brg_nr': bridge_number,
                                   'brg_srv_id': server.get_id(),
                                   'brg_ip': "0.0.0.0"})
            bridge_id = cur.fetchone()[0]
            cur.execute(cr_stmnt, {'brg_id': bridge_id,
                                   'port': 22})
            report_id = cur.fetchone()[0]

            infoline = PATHSTRIP.sub('',stripped)
            for stats in infoline.split(","):
                country, users = stats.split("=")
                print ccr_stmnt%{'rep_id': report_id,
                                 'cco_short': country,
                                 'useres': users}
                # cur.execute(ccr_stmnt, {'rep_id': report_id,
                #                         'cco_short': country,
                #                         'useres': users})

