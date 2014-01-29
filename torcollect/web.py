#-*- coding: utf-8 -*-

##########################################################
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

import datetime
import torcollect.database
import StringIO
import json
import re
import pygal
from pygal.style import Style

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
        <div class="col-md-12 nopad" id="graphspace" style="display:none;">
            <svg width="1024" height="100" class="tc_graph" id="tc_graph">
                <defs>
                    <linearGradient id="grad1" x1="0%%" y1="0%%" x2="0%%" y2="100%%">
                    <stop offset="0%%" style="stop-color:rgb(160,255,0);stop-opacity:1" />
                    <stop offset="100%%" style="stop-color:rgb(128,255,0);stop-opacity:0.25" />
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <div>
            %(usage_graph)s
        </div>
    </div>
    <div class="row tc_table" id="reportcontent">
        <div class="col-md-12">Please select a day to see detailed statistics</div>
    </div>

    <script type="text/javascript" src="statistics.js"></script>
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
<tr>
    <td colspan="3" style="border-top:none;">%(sparkline)s</td>
</tr>
"""

country_table = """
<div class="col-md-4">
<h4>Country Statistics</h4>
%(worldmap)s
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
<tr>
    <td colspan="3" style="border-top:none;">%(sparkline)s</td>
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

RE_XML_COMMENT = re.compile(r"<!--.*?-->")

class TorcollectStyle(Style):
    def __init__(self):
        Style.__init__(self)
        self.background = 'transparent'
        self.plot_background = 'transparent'
        self.colors = ('#aaff00', '#550055')
        self.foreground_dark = '#010101'

def clean_graph(xml):
    xml = re.sub(RE_XML_COMMENT, "", xml)
    return xml.replace ("<?xml version='1.0' encoding='utf-8'?>","",1)

def escape(plain):
    html = plain.replace("<", "&lt;")
    return html.replace(">", "&gt;")

def generate_main_graph(data):
    chart = pygal.Line(width=900, height=100, fill=True, spacing=20,
                       margin=10, style=TorcollectStyle())
    chart.add('Users', data)
    return clean_graph(chart.render())

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
    pygal_graph = []
    for dataset in cur.fetchall():
        graphdata.append({'d': dataset[1], 'u': dataset[0]})
        pygal_graph.append(dataset[0])
    page = main_page % {'graphdata': json.dumps(graphdata),
                        'usage_graph': generate_main_graph(pygal_graph)}
    mainpage = open(REPORTPAGE, "w")
    mainpage.write(page)
    mainpage.close()

def generate_worldmap(data):
    wm = pygal.Worldmap(width=300, height=200, show_legend=False, margin=0, style=TorcollectStyle())
    wm.add('Tor Usage', data)
    return clean_graph(wm.render())

def generate_country_sparkline(data):
    chart = pygal.StackedLine(fill=True, show_x_labels=False, 
                              show_y_labels=False, margin=0, style=TorcollectStyle())
    chart.add('', data)
    return clean_graph(chart.render_sparkline(interpolate="cubic"))

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
    stmnt_history = "SELECT CCO_SHORT, SUM(CRP_USERS) AS USAGE\
            FROM CountryReport INNER JOIN CountryCode \
                ON (CCO_ID = CRP_CCO_ID) \
            INNER JOIN Report \
                ON (REP_ID = CRP_REP_ID) \
            WHERE REP_DATE > DATE %(date)s-7 \
            GROUP BY CCO_SHORT, CCO_LONG, REP_DATE \
            ORDER BY CCO_SHORT, REP_DATE ASC;"
    cur = db.cursor()

    cur.execute(stmnt_history, {'date': date.isoformat()})
    country_history = {}
    for dataset in cur.fetchall():
        ccode = dataset[0].lower()
        if not country_history.has_key(ccode):
            country_history[ccode] = []
        country_history[ccode].append(dataset[1])

    cur.execute(stmnt, {'date': date.isoformat()})
    country_lines = StringIO.StringIO()
    
    worldmap_data = {}

    for dataset in cur.fetchall():
        ccode = dataset[0].lower()
        line = country_line % {'code': ccode,
                               'name': dataset[1],
                               'users': dataset[2],
                               'sparkline': generate_country_sparkline(country_history[ccode])}
        worldmap_data[dataset[0].lower()] = dataset[2]
        country_lines.write(line)

    return country_table % {'date': date.isoformat(),
                            'content': country_lines.getvalue(),
                            'worldmap': generate_worldmap(worldmap_data)}


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

def generate_bridge_sparkline(data):
    style = Style()
    style.background = 'transparent'
    style.plot_background = 'transparent'
    chart = pygal.StackedLine(fill=True, show_x_labels=False, show_y_labels=False,
                               margin=0, style=TorcollectStyle())
    chart.add('', data['sent'])
    chart.add('', data['received'])
    return clean_graph(chart.render_sparkline(interpolate="cubic"))

def generate_bridgereport(date):
    db = torcollect.database.Database()
    stmnt_usage = "SELECT REP_BRG_ID, SUM(CRP_USERS) AS USAGE \
             FROM CountryReport LEFT JOIN Report \
                ON (REP_ID = CRP_REP_ID) \
             WHERE REP_DATE = %(date)s \
             GROUP BY REP_BRG_ID \
             ORDER BY USAGE DESC;"
    stmnt_traffic = "SELECT REP_BRG_ID, REP_TRAFFIC_SENT, \
                        REP_TRAFFIC_RECEIVED \
                     FROM Report \
                     WHERE REP_DATE > DATE %(date)s-7 \
                     ORDER BY REP_BRG_ID, REP_DATE ASC;"
    cur = db.cursor()


    traffic_data = {}
    cur.execute(stmnt_traffic, {'date': date.isoformat()})
    for dataset in cur.fetchall():
        if not traffic_data.has_key(dataset[0]):
            traffic_data[dataset[0]] = {'sent':[],'received':[]}
        traffic_data[dataset[0]]['sent'].append(dataset[1])
        traffic_data[dataset[0]]['received'].append(dataset[2])
        

    cur.execute(stmnt_usage, {'date': date.isoformat()})
    bridge_lines = StringIO.StringIO()
    for dataset in cur.fetchall():
        line = bridge_line % {'users': dataset[1],
                              'sparkline': generate_bridge_sparkline(traffic_data[dataset[0]])}
        bridge_lines.write(line)


    return bridge_table % {'date': date.isoformat(),
                           'content': bridge_lines.getvalue()}


def generate_report_for_day(date):
    content = report_header%{'date': date.isoformat()}
    country_html = generate_countryreport(date)
    bridge_html = generate_bridgereport(date)

    content += country_html
    content += bridge_html
    content += generate_transportreport(date)

    reportfile = open("%s%s%s" % (REPORTS, date.isoformat(), ".html"), "w")
    reportfile.write(content)
    reportfile.close()

