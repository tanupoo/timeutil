#!/usr/bin/env python

from datetime import datetime, timedelta, timezone
import dateutil.tz
import dateutil.parser
import re

__tz_gmt = dateutil.tz.gettz("GMT")
__epoch = datetime(1970, 1, 1, tzinfo=__tz_gmt)

"""
def naive_to_aware(dt, default_tzinfo=__tz_gmt):
    if dt.tzinfo == None or dt.tzinfo.utcoffset(dt) == None:
        return dt.replace(tzinfo=default_tzinfo)
    return dt
"""

"""
def datetime_to_timestamp_raw(dt, default_tzinfo=__tz_gmt):
    dt_aware = naive_to_aware(dt, default_tzinfo=default_tzinfo)
    return dt_aware.astimezone(__tz_gmt) - __epoch

def datetime_to_timestamp_days(dt, default_tzinfo=__tz_gmt):
    delta = datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo)
    #return delta.days
    return delta.total_seconds()//86400

def datetime_to_timestamp_hours(dt, default_tzinfo=__tz_gmt):
    delta = datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo)
    return delta.total_seconds()//3600

def datetime_to_timestamp_min(dt, default_tzinfo=__tz_gmt):
    delta = datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo)
    return delta.total_seconds()//60

def datetime_to_timestamp(dt, default_tzinfo=__tz_gmt):
    return int(datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo).total_seconds())

def datetime_to_timestamp_usec(dt, default_tzinfo=__tz_gmt):
    return datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo).total_seconds()

def datetime_to_iso(dt):
    return dt.isoformat()

def datetime_to_ctime(dt):
    return dt.ctime()

def datetime_to_day(dt):
    return datetime_to_timestamp_days(dt)

def datetime_to_hour(dt):
    return datetime_to_timestamp_hours(dt)

def datetime_to_min(dt):
    return datetime_to_timestamp_minutes(dt)

def datetime_to_sec(dt):
    return datetime_to_timestamp(dt)

def datetime_to_msec(dt):
    return int(datetime_to_timestamp_usec(dt)*1000)

def datetime_to_usec(dt):
    return datetime_to_timestamp_usec(dt)

def datetime_to_hex(dt):
    return "0x{:x}".format(datetime_to_sec(dt))
"""

datestr_mode_list = [
        "iso", "iso8601",
        "ctime",
        "hex",
        "weeks", "week",
        "days", "day",
        "hours", "hour",
        "minutes", "min",
        "seconds", "sec",
        "milliseconds", "msec",
        "microseconds", "usec"
        ]

def timedelta_to_datestr(time_delta, out_form="iso"):
    if out_form in ["iso", "iso8601", "ctime"]:
        raise NotImplementedError
    elif out_form in ["weeks", "week"]:
        raise NotImplementedError
    elif out_form == "hex":
        return hex(round(time_delta.total_seconds()))
    elif out_form in ["days", "day"]:
        return str(time_delta.days)
    elif out_form in ["hours", "hour"]:
        return str(time_delta.total_seconds()/3600)
    elif out_form in ["minutes", "min"]:
        return str(time_delta.total_seconds()/60)
    elif out_form in ["seconds", "sec"]:
        return str(time_delta.total_seconds())
    elif out_form in ["milliseconds", "msec"]:
        return str(round(time_delta.total_seconds() / 1000, 3))
    elif out_form in ["microseconds", "usec"]:
        return str(round(time_delta.total_seconds() / 1000000, 6))
    else:
        raise ValueError("unknown out_form {}.".format(out_form))

def datetime_to_datestr(dt, out_form="iso"):
    if out_form in ["iso", "iso8601"]:
        return dt.isoformat("T")
    elif out_form == "ctime":
        return dt.ctime()
    return timedelta_to_datestr(dt - __epoch, out_form=out_form)

def numstr_to_datetime(tn, unit="microseconds"):
    """
    converting the number string specified by tn into a datetime object.
    the type of the number must be either int or float.
    unit specifies the unit of the number.
    seconds, milliseconds, microseconds are acceptable.
    """
    # XXX shoult be compared with datetime.max (0x3afff3c2f0) ?
    if not isinstance(tn, (int, float)):
        raise ValueError("numstr_to_datetime() must take a number.")
    if unit == "seconds":
        return __epoch + timedelta(seconds=tn)
    elif unit == "milliseconds":
        return __epoch + timedelta(milliseconds=tn)
    elif unit == "microseconds":
        return __epoch + timedelta(microseconds=tn)
    else:
        raise ValueError("unit must be either 'seconds', 'milliseconds', or 'microseconds'.")

def datestr_get_tzinfo(datestr, default_tzname):
    """
    return datetime_string and tzinfo.
    """
    if datestr.find("+") > 0:
        dt_str, diff_str = datestr.split("+")
        if diff_str.find(":"):
            timediff = float(diff_str.replace(":","."))
            return dt_str, timezone(timedelta(hours=timediff))
        else:
            ValueError("a timediff string must have a colon.")
    else:
        return datestr, dateutil.tz.gettz(default_tzname)

def datestr_to_datetime(datestr, default_tzname="GMT", unit="seconds"):
    """
    convert the datetime string into an timezone-aware datetime object.
    acceptable string:
        now
        ^0x[a-fA-F\d]+$
        ^[\d\.]+$
        whatever dateutil.parser() can accept.
    tzname:
    if the datetime string doesn't have a timezone,
    this function will add the timezone being specified.
    """
    if datestr == "now":
        dt = datetime.now()
        tzinfo = dateutil.tz.gettz(default_tzname)
    else:
        dtstr, tzinfo = datestr_get_tzinfo(datestr, default_tzname)
        if re.match("^0x[a-fA-F\d]+$", dtstr):
            dt = numstr_to_datetime(int(dtstr, 16), unit)
        elif re.match("^[\d\.]+$", dtstr):
            dt = numstr_to_datetime(float(dtstr), unit)
        else:
            dt = dateutil.parser.parse(dtstr)
    return dt.replace(tzinfo=tzinfo)

def datestr_to_timedelta(given_str):
    """
    days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]
    """
    r = re.match("[\d,\.]+$", given_str)
    if not r:
        raise ValueError("ERROR: arg must consist of [\\d,\\.]+")
    return eval("timedelta(" + given_str + ")")

'''
convert the datetime string into an integer timestamp in second.
it can accept whatever dateutil.parser() can accept.
'''
def datestr_to_timestamp(s, default_tzname="GMT"):
    dt = datestr_to_datetime(s, default_tzname=default_tzname)
    default_tzinfo = dateutil.tz.gettz(default_tzname)
    return datetime_to_timestamp(dt, default_tzinfo=default_tzinfo)

'''
convert the datetime string into an integer timestamp in microsecond.
it can accept whatever dateutil.parser() can accept.
'''
"""
def datestr_to_timestamp_msec(s, default_tzname="GMT"):
    dt = datestr_to_datetime(s, default_tzname=default_tzname)
    default_tzinfo = dateutil.tz.gettz(default_tzname)
    return datetime_to_timestamp_msec(dt, default_tzinfo=default_tzinfo)
"""

if __name__ == "__main__":
    test_strings = [
            ("1491395277", "seconds", int, 10),
            ("1491395277123", "milliseconds", int, 10),
            ("1491395277123456", "microseconds", int, 10),
            ]
    for v in test_strings:
        print(numstr_to_datetime(v[2](v[0], v[3]), unit=v[1]))
    test_strings = [
            ("1491395277", "seconds", int, 10),
            ("1491395277123", "milliseconds", int, 10),
            ("1491395277123456", "microseconds", int, 10),
            ("1491395277+09:00", "seconds", int, 10),
            ("1491395277123+09:00", "milliseconds", int, 10),
            ("1491395277123456+09:00", "microseconds", int, 10),
            ]
    for v in test_strings:
        print(datestr_to_datetime(v[0], unit=v[1]))

"""
# 2017-04-05T14:27:57.944+02:00 => 1491395277944
print(datestr_to_timestamp_msec("2017-04-05T14:27:57.944+02:00"))
#print(datestr_to_timestamp_msec("2017-03-24T06:53:32.502+01:00"))
#print(datestr_to_timestamp_msec("2017-03-24T06:53:32.50+01:00"))
#print(datestr_to_timestamp_msec("2017-03-24T06:53:32.50"))
#print(datestr_to_timestamp_msec("2017-03-24T06:53:32.502345"))
#print(datestr_to_timestamp_msec("2017-03-24T06:53:32"))
s = "20170509T12:09:45.363"
print(s, datestr_to_timestamp_msec(s))

from datetime_util import *

test_strings = [
    "2019-05-15T10:47:11.094980+00:00",
    "2019-05-15T10:47:11.094980+09:00",
    "2019-05-15T10:47:11.094980",
    "2019-05-15T19:48:07",
    "2019-05-15",
    "2019-05-15T",
    ]

now=`date +'%Y-%m-%dT%H:%M:%S'`
timeutil.py now

 timeutil.py 18:42:22.654
 2019-05-15T18:42:22.654000+00:00

timeutil.py 18:42:22.654
timeutil.py 18:42:22.654 -m iso
timeutil.py 18:41:12.232 -m ctime
timeutil.py 18:41:12.232 -m day
timeutil.py 18:41:12.232 -m hour
timeutil.py 18:41:12.232 -m min
timeutil.py 18:41:12.232 -m sec
timeutil.py 18:41:12.232 -m msec
timeutil.py 18:41:12.232 -m usec
timeutil.py 18:41:12.232 -m hex
#timeutil.py 18:41:12:232 -m ieee754
"""
