#!/usr/bin/python

import datetime
import torcollect.database
import StringIO
import json

from torcollect.paths import REPORTPAGE, REPORTS

main_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Torservers.net :: Statistics</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css" type="text/css">
    <link rel="stylesheet" href="bootstrap/css/bootstrap-theme.min.css" type="text/css">
    <link rel="stylesheet" href="torcollect.css" type="text/css">
    <script type="text/javascript">
        var graphdata = %(graphdata)s;
    </script>
</head>
<body onLoad="">
    <div class="row tc_heading">
    <div class="col-md-12"><h1>Torservers.net Statistics</h1></div>
    </div>
    <div class="row tc_chart">
        <div class="col-md-12 nopad" id="graphspace">
            <svg width="1024" height="100" class="tc_graph" id="tc_graph">
                <defs>
                    <linearGradient id="grad1" x1="0%%" y1="0%%" x2="0%%" y2="100%%">
                    <stop offset="0%%" style="stop-color:rgb(160,255,0);stop-opacity:1" />
                    <stop offset="100%%" style="stop-color:rgb(128,255,0);stop-opacity:0.25" />
                    </linearGradient>
                </defs>
            </svg>
        </div>
    </div>
    <div class="row tc_table" id="reportcontent">
        <div class="col-md-12">Please select a day to see detailed statistics</div>
    </div>

    <script type="text/javascript" src="datascript.js"></script>
</body>
</html>
"""

report_header = """
<h2>Statistics of Bridge usage at %(date)s</h2>
"""

country_line = """
<tr>
    <td><img src="flags/%(code)s.png" alt="%(code)s"></td>
    <td> %(name)s </td>
    <td> %(users)d </td>
</tr>
"""

country_table = """
<div class="col-md-4">
<h4>Country Statistics</h4>
<table class="table">
%(content)s
</table>
</div>
"""

transport_line = """
<tr>
    <td><img src="transport.png" alt="Pluggable Transport"></td>
    <td> %(transport)s </td>
    <td> %(users)d </td>
</tr>
"""

transport_table = """
<div class="col-md-4">
<h4>Pluggable Transports Statistics</h4>
<table class="table">
%(content)s
</table>
</div>
"""

bridge_line = """
<tr>
    <td><img src="bridge.png" alt="Bridge"></td>
    <td> Bridge </td>
    <td> %(users)d </td>
</tr>
"""

bridge_table = """
<div class="col-md-4">
<h4>Users by Bridge</h4>
<table class="table">
%(content)s
</table>
</div>
"""


def escape(plain):
    html = plain.replace("<", "&lt;")
    return html.replace(">", "&gt;")


def generate_main_page():
    graphdata = []
    db = torcollect.database.Database()
    stmnt = "SELECT SUM(CRP_USERS), REP_DATE \
            FROM Report INNER JOIN CountryReport \
                ON (REP_ID = CRP_REP_ID) \
            GROUP BY (REP_DATE) \
            ORDER BY REP_DATE ASC LIMIT 365;"
    cur = db.cursor()
    cur.execute(stmnt)
    count = 0
    for dataset in cur.fetchall():
        graphdata.append({'d': dataset[1], 'u': dataset[0]})
    page = main_page % {'graphdata': json.dumps(graphdata)}
    mainpage = open(REPORTPAGE, "w")
    mainpage.write(page)
    mainpage.close()


def generate_countryreport(date):
    db = torcollect.database.Database()
    stmnt = "SELECT CCO_SHORT, CCO_LONG, SUM(CRP_USERS) AS USAGE\
            FROM CountryReport INNER JOIN CountryCode \
                ON (CCO_ID = CRP_CCO_ID) \
            INNER JOIN Report \
                ON (REP_ID = CRP_REP_ID) \
            WHERE REP_DATE = %(date)s \
            GROUP BY CCO_SHORT, CCO_LONG \
            ORDER BY USAGE DESC;"
    cur = db.cursor()
    cur.execute(stmnt, {'date': date.isoformat()})
    country_lines = StringIO.StringIO()
    for dataset in cur.fetchall():
        line = country_line % {'code': dataset[0].lower(),
                               'name': dataset[1],
                               'users': dataset[2]}
        country_lines.write(line)
    return country_table % {'date': date.isoformat(),
                            'content': country_lines.getvalue()}


def generate_transportreport(date):
    db = torcollect.database.Database()
    stmnt = "SELECT TRA_NAME, SUM(TRP_USERS) AS USAGE\
             FROM TransportReport INNER JOIN Transport \
                 ON (TRA_ID = TRP_TRA_ID) \
             INNER JOIN Report \
                 ON (REP_ID = TRP_REP_ID) \
             WHERE REP_DATE = %(date)s \
             GROUP BY TRA_NAME \
             ORDER BY USAGE DESC;"
    cur = db.cursor()
    cur.execute(stmnt, {'date': date.isoformat()})
    transport_lines = StringIO.StringIO()
    for dataset in cur.fetchall():
        line = transport_line % {'transport': escape(dataset[0]),
                                 'users': dataset[1]}
        transport_lines.write(line)
    return transport_table % {'date': date.isoformat(),
                              'content': transport_lines.getvalue()}


def generate_bridgereport(date):
    db = torcollect.database.Database()
    stmnt = "SELECT REP_BRG_ID, SUM(CRP_USERS) AS USAGE \
             FROM CountryReport INNER JOIN Report \
                ON (REP_ID = CRP_REP_ID) \
             WHERE REP_DATE = %(date)s \
             GROUP BY REP_BRG_ID \
             ORDER BY USAGE DESC;"
    cur = db.cursor()
    cur.execute(stmnt, {'date': date.isoformat()})
    bridge_lines = StringIO.StringIO()
    for dataset in cur.fetchall():
        line = bridge_line % {'users': dataset[1]}
        bridge_lines.write(line)
    return bridge_table % {'date': date.isoformat(),
                           'content': bridge_lines.getvalue()}


def generate_report_for_day(date):
    content = report_header%{'date': date.isoformat()}
    content += generate_countryreport(date)
    content += generate_bridgereport(date)
    content += generate_transportreport(date)
    reportfile = open("%s%s%s" % (REPORTS, date.isoformat(), ".html"), "w")
    reportfile.write(content)
    reportfile.close()

