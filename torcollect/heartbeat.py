import re
import datetime


LOGPATH = "/var/lib/torcollect/"

class Heartbeat(object):
    """
    The functions in this class are meant to parse information from human-
    readable written "heartbeat"-lines in TOR's notices-logfile
    """
    @classmethod
    def _calc_bytesize(cls, bytestring):
        amount, suffix = bytestring.split(" ")
        amount = float(amount)
        if suffix == "kB":
            retval = amount * (10**3)
        elif suffix == "MB":
            retval = amount * (10**6)
        elif suffix == "GB":
            retval = amount * (10**9)
        elif suffix == "TB":
            retval = amount * (10**12)
        elif suffix == "PB":
            retval = amount * (10**15)
        elif suffix == "EB":
            retval = amount * (10**18)
        else:
            retval = amount
        return int(retval)
            
    @classmethod
    def _parse_timestamp(cls, dateline):
        # TODO: Discuss whether the workaround for the missing year suffices for
        #       productive use
        dateline = re.sub(r"\.\d{3}$", "", dateline)
        probing_date = datetime.datetime.strptime(dateline, "%b %d %H:%M:%S")
        now = datetime.datetime.now()
        if probing_date.month > now.month:
            dateline = "%d %s"%(now.year-1, dateline)
        else:
            dateline = "%d %s"%(now.year, dateline)
        return datetime.datetime.strptime(dateline, "%Y %b %d %H:%M:%S")

    @classmethod
    def _parse_uptime(cls, groupdict):
        timedict = {}
        timedict['days'] = int(groupdict['days'])
        hours, minutes = groupdict['hours'].split(":")
        timedict['hours'] = int(hours)
        timedict['minutes'] = int(minutes)
        return datetime.timedelta(**timedict)

    RE_NUMBER = re.compile(r"^\d+")
    RE_TIMESTAMP = re.compile(r"\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{3}")
    RE_UPTIME = re.compile(r"((?P<days>\d+?) days )?((?P<hours>(\d\d?:\d{2})?) hours)?")
    RE_BYTES = re.compile(r"\d+\.\d{2} [EPTGMk]?B")

    @classmethod
    def parse(cls, hb_line):
        """
        This function parses the information of one grepped Heartbeat-line 
        in a tor notices logfile
        """
        ret = Heartbeat()
        # Drop unnecessary human-readable stuff
        hb_line = hb_line.replace(LOGPATH+"notices","")
        hb_line = hb_line.replace(".log.1:"," ")
        hb_line = hb_line.replace("[notice] Heartbeat: Tor's uptime is ","")
        hb_line = hb_line.replace(", with","")
        hb_line = hb_line.replace("circuits open. I've sent","")
        hb_line = hb_line.replace("and received","")

        # Find the bridge-number
        hb_line = hb_line.strip()
        m = re.match(Heartbeat.RE_NUMBER, hb_line)
        ret.bridge_nr = int(m.group())
        hb_line = re.sub(Heartbeat.RE_NUMBER, "", hb_line, 1)
        
        # Find the timestamp and convert it to a real timestamp
        hb_line = hb_line.strip()
        m = re.search(Heartbeat.RE_TIMESTAMP, hb_line)
        ret.timestamp = Heartbeat._parse_timestamp(m.group())
        hb_line = re.sub(Heartbeat.RE_TIMESTAMP, "", hb_line, 1)
        
        # Find the uptime
        hb_line = hb_line.strip()
        m = re.match(Heartbeat.RE_UPTIME, hb_line)
        ret.uptime = Heartbeat._parse_uptime(m.groupdict())
        hb_line = re.sub(Heartbeat.RE_UPTIME, "", hb_line, 1)

        # Get the number of running circuits
        hb_line = hb_line.strip()
        m = re.match(Heartbeat.RE_NUMBER, hb_line)
        ret.circuits = int(m.group())
        hb_line = re.sub(Heartbeat.RE_NUMBER, "", hb_line, 1)
        
        # Get the amount of data sent
        hb_line = hb_line.strip()
        m = re.match(Heartbeat.RE_BYTES, hb_line)
        ret.sent = Heartbeat._calc_bytesize(m.group())
        hb_line = re.sub(Heartbeat.RE_BYTES, "", hb_line, 1)

        # Get the amount of data receiveed
        hb_line = hb_line.strip()
        m = re.match(Heartbeat.RE_BYTES, hb_line)
        ret.received = Heartbeat._calc_bytesize(m.group())
        
        return ret
  
    def __init__(self):
        self.bridge_nr = None
        self.timestamp = None
        self.uptime = None
        self.circuits = None
        self.received = None
        self.sent = None

