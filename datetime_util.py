#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime, timedelta
import dateutil.tz
import dateutil.parser
import re

__tz_gmt = dateutil.tz.gettz("GMT")
__epoch = datetime(1970, 1, 1, tzinfo=__tz_gmt)

def naive_to_aware(dt, default_tzinfo=__tz_gmt):
    if dt.tzinfo == None or dt.tzinfo.utcoffset(dt) == None:
        return dt.replace(tzinfo=default_tzinfo)
    return dt

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

def datetime_to_timestamp_minutes(dt, default_tzinfo=__tz_gmt):
    delta = datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo)
    return delta.total_seconds()//60

def datetime_to_timestamp(dt, default_tzinfo=__tz_gmt):
    return int(datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo).total_seconds())

def datetime_to_timestamp_msec(dt, default_tzinfo=__tz_gmt):
    return int(datetime_to_timestamp_raw(dt, default_tzinfo=default_tzinfo).total_seconds() * 1000)

'''
convert the datetime string into an timezone-aware datetime object.
it can accept whatever dateutil.parser() can accept.
'''
def datestr_to_datetime(s, default_tzname="GMT"):
    default_tzinfo = dateutil.tz.gettz(default_tzname)
    if s == "now":
        return datetime.now(default_tzinfo)
    if re.match("[\d]+$", s):
        dt = __epoch + timedelta(0, int(s))
    elif re.match("[\d\.]+$", s):
        ss, micross = s.split(".")
        zero_len = 0
        r = re.match("0+", micross)
        if r:
            zero_len = len(r.group(0))
        micross = int(micross) * 100000 / (10**zero_len)
        dt = __epoch + timedelta(0, int(ss), micross)
    else:
        dt = dateutil.parser.parse(s)
    return naive_to_aware(dt, default_tzinfo=default_tzinfo)

def datestr_to_timedelta(s):
    r = re.match("[\d,\.]+$", s)
    if not r:
        raise("ERROR")
    return eval("timedelta(" + s + ")")

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
def datestr_to_timestamp_msec(s, default_tzname="GMT"):
    dt = datestr_to_datetime(s, default_tzname=default_tzname)
    default_tzinfo = dateutil.tz.gettz(default_tzname)
    return datetime_to_timestamp_msec(dt, default_tzinfo=default_tzinfo)

if __name__ == "__main__":
    # 2017-04-05T14:27:57.944+02:00 => 1491395277944
    print(datestr_to_timestamp_msec("2017-04-05T14:27:57.944+02:00"))
    #print(datestr_to_timestamp_msec("2017-03-24T06:53:32.502+01:00"))
    #print(datestr_to_timestamp_msec("2017-03-24T06:53:32.50+01:00"))
    #print(datestr_to_timestamp_msec("2017-03-24T06:53:32.50"))
    #print(datestr_to_timestamp_msec("2017-03-24T06:53:32.502345"))
    #print(datestr_to_timestamp_msec("2017-03-24T06:53:32"))
    s = "20170509T12:09:45.363"
    print(s, datestr_to_timestamp_msec(s))

'''
from datetime_util import *
'''

