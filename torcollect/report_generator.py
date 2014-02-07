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

import torcollect.database
import datetime

class MonthlyReport(object):
    """ Generates a Monthly report of the bridge-usage in HTML-format
    """
    _USAGE_STMNT = "SELECT SUM(TRP_USERS) FROM Report INNER JOIN TransportReport \
                        ON (REP_ID = TRP_REP_ID) \
                    WHERE REP_DATE >= %(startdate)s AND REP_DATE <= %(end_date)s \
                    GROUP BY (REP_DATE) \
                    ORDER BY REP_DATE ASC;"

    _TRFFC_STMNT = "SELECT SUM(REP_TRAFFIC_RECEIVED), SUM(REP_TRAFFIC_SENT) \
                    FROM Report \
                    WHERE REP_DATE >= %(startdate)s AND REP_DATE <= %(end_date)s \
                    GROUP BY (REP_DATE) \
                    ORDER BY REP_DATE ASC;"

    _CNMAP_STMNT = "SELECT CCO_SHORT, SUM(CRP_USERS) \
                    FROM CountryReport INNER JOIN CountryCode \
                        ON (CCO_ID = CRP_CCO_ID) \
                    INNER JOIN Report \
                        ON (REP_ID = CRP_REP_ID) \
                    WHERE REP_DATE >= %(startdate)s AND REP_DATE <= %(end_date)s \
                    GROUP BY CCO_SHORT \
                    ORDER BY CCO_SHORT ASC;"

    _CNHIS_STMNT = "SELECT CT.CCO_SHORT, RT.USAGE, CT.DATE FROM \
                        (SELECT CCO_SHORT, DT.DATE AS DATE FROM \
                            (SELECT CURRENT_DATE + i AS DATE FROM \
                                GENERATE_SERIES(DATE %(start_date)s - CURRENT_DATE, \ 
                                                DATE %(end_date)s - CURRENT_DATE) i) \
                            AS DT \
                            CROSS JOIN CountryCode) AS CT \
                        LEFT JOIN \
                        (SELECT CCO_SHORT, SUM(CRP_USERS) AS USAGE, REP_DATE  \
                         FROM CountryReport INNER JOIN CountryCode \
                            ON (CCO_ID = CRP_CCO_ID)  \
                        INNER JOIN Report \
                            ON (REP_ID = CRP_REP_ID) \
                        WHERE REP_DATE >= %(start_date)s  AND REP_DATE <= %(end_date)s \
                        GROUP BY CCO_SHORT, REP_DATE \
                        ORDER BY CCO_SHORT, REP_DATE ASC) \
                    AS RT ON (RT.CCO_SHORT = CT.CCO_SHORT AND RT.REP_DATE = CT.DATE);"

    def __init__(self, year=None, month=None):
        """ The Monthly Report is initialized by giving it a Month it should represent """
        # if no date and year given, assume its this date and year
        if month is None or year is None:
            date = datetime.datetime.now()
            date.day = 1
        else:
            date = datetime.datetime(year, month, 1)

        self.start_date = date
        
        # determine end date
        self.days_of_month = (datetime.datetime(date.year, date.month+1, 1) - date).days
        self.end_date = datetime.datetime(date.year, date.month, self.days_of_month)

        # define structures to save data in
        self.usage_data = []
        self.traffic_sent = []
        self.traffic_received = []
        self.country_overall_data = {}
        self.country_usage_date = {}

        # proceed with gathering the needed data
        self.gather_data()
    
    def gather_data(self):
        """ Gathering the data needed to generate the report """
        self.check_validity()
        db = torcollect.database.Database()
        cur = db.cursor()

        cur.execute(MonthlyReport._USAGE_STMNT, {'start_date': self.start_date.isoformat(),
                                   'end_date'  : self.end_date.isoformat()})
        for dataset in cur.fetchall():
            self.usage_data.append(dataset[0])
        
        cur.execute(MonthlyReport._TRFFC_STMNT, {'start_date': self.start_date.isoformat(),
                                   'end_date'  : self.end_date.isoformat()})
        for dataset in cur.fetchall():
            self.traffic_send.append(dataset[1])
            self.traffic_received.append(dataset[0])

        cur.execute(MonthlyReport._CNMAP_STMNT, {'start_date': self.start_date.isoformat(),
                                   'end_date'  : self.end_date.isoformat()})
        for dataset in cur.fetchall():
            self.country_overall_data[dataset[0].lower()] = dataset[1]
        
        cur.execute(MonthlyReport._CNHIS_STMNT, {'start_date': self.start_date.isoformat(),
                                   'end_date'  : self.end_date.isoformat()})
        for dataset in cur.fetchall():
            cc = dataset[0].lower()
            if not self.country_usage_data.has_key(cc):
                self.country_usage_data[cc] = []
            self.country_usage_data[cc].append(dataset[1])
      
    def check_validity(self):
        """ Check if there is all data needed to generate the report """
        if self.end_date > datetime.datetime.now():
            difference = (self.end_date - datetime.datetime.now()).days
            raise Exception("This month is not finished yet. Try again in %d days"%difference)
