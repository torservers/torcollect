import paramiko
import tempfile
import re

import torcollect.server
import torcollect.database

LOGPATH = "/var/lib/torcollect/"
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

    db = torcollect.database.Database()
    cur = db.cursor()

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
