from datetime import datetime, timedelta, timezone
from dateutil.tz import gettz as dtgettz
from dateutil import parser as dtparser
import re

"""
datetime_util:
    The internal timezone is always GMT.
"""

__tz_gmt = dtgettz("GMT")
__epoch = datetime(1970, 1, 1, tzinfo=__tz_gmt)

# this is intended to use by argparser().
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

def timedelta_to_str(time_delta, output_form="iso", digit=3, output_tzname=None):
    """
    digit: the number of digits in the string.
        the output is rounded if the digit is 0.
    """
    if output_form in ["iso", "iso8601", "ctime"]:
        raise NotImplementedError
    elif output_form == "hex":
        a = int(time_delta.total_seconds()).to_bytes(4, byteorder="big")
        return a.hex()
    elif output_form == "HEX":
        a = int(time_delta.total_seconds()).to_bytes(4, byteorder="big")
        return a.hex().upper()
    else:
        if output_form in ["years", "year"]:
            result = time_delta.total_seconds() / 86400 / 365   # TBD
        elif output_form in ["months", "month"]:
            result = time_delta.total_seconds() / 86400 / 30   # TBD
        elif output_form in ["weeks", "week"]:
            result = time_delta.total_seconds() / 86400 / 7
        elif output_form in ["days", "day"]:
            result = time_delta.total_seconds() / 86400
        elif output_form in ["hours", "hour"]:
            result = time_delta.total_seconds() / 3600
        elif output_form in ["minutes", "min"]:
            result = time_delta.total_seconds() / 60
        elif output_form in ["seconds", "sec"]:
            result = time_delta.total_seconds()
        elif output_form in ["milliseconds", "msec"]:
            result = time_delta.total_seconds() * 1000
        elif output_form in ["microseconds", "usec"]:
            result = int(time_delta.total_seconds() * 1000000)
        else:
            raise ValueError("unknown output_form {}.".format(output_form))
        if digit == 0:
            return str(int(result))
        else:
            return str(round(result, digit))

def tzname_to_tzinfo(tzstr):
    tzinfo = dtgettz(tzstr)
    if tzinfo is None:
        raise ValueError(f"invalid TZ string: {tzstr}")
    else:
        return tzinfo

def datetime_to_str(dt, output_form="iso", digit=3, output_tzname=None):
    """
    converts datetime into a string.
    dt must be a timezone aware.
    if rounding is True, the output will be rounded into the form of
    output_form.
    converts a timezone according to the output_tzname if not None.
    """
    if output_tzname is not None:
        dt = dt.astimezone(tzname_to_tzinfo(output_tzname))
    if output_form in ["iso", "iso8601"]:
        return dt.isoformat("T")
    elif output_form == "ctime":
        return dt.ctime()
    return timedelta_to_str(dt - __epoch, output_form=output_form, digit=digit)

def num_to_datetime(tn, unit="microseconds"):
    """
    converting the number specified by tn into a datetime object.
    the type of the number must be either int or float.
    unit specifies the unit of the number.
    seconds, milliseconds, microseconds are acceptable.
    """
    # XXX shoult be compared with datetime.max (0x3afff3c2f0) ?
    if not isinstance(tn, (int, float)):
        raise ValueError("num_to_datetime() must take a number.")
    if unit == "seconds":
        return __epoch + timedelta(seconds=tn)
    elif unit == "milliseconds":
        return __epoch + timedelta(milliseconds=tn)
    elif unit == "microseconds":
        return __epoch + timedelta(microseconds=tn)
    else:
        raise ValueError("unit must be either 'seconds', 'milliseconds', or 'microseconds'.")

def tzinfo_from_tzstr(tzstr, default_tzname="GMT"):
    """
    return tzinfo from tzstr. the valid tzstr are:
        +TZ_OFFSET
        -TZ_OFFSET
        @TZ_STR
        TZ_STR
    """
    if tzstr is None or tzstr == "":
        return tzname_to_tzinfo(default_tzname)
    #
    r = re.search(r"(?P<sign>[+\-])(?P<val>[\d:]+)", tzstr)
    if r:
        hm = r.group("val").split(":")
        if len(hm) == 2:
            h = int(hm[0]) + float(hm[1])/60
            if r.group("sign") == "-":
                h = -h
            return timezone(timedelta(hours=h))
        elif len(hm) == 1:
            return timezone(timedelta(hours=int(hm[0])))
        else:
            raise ValueError(f"unknown TZ string {tzstr}")
    r = re.search(r"@(?P<name>[a-zA-Z_/]+)", tzstr)
    if r:
        tzs = r.group("name")
        tzinfo = tzname_to_tzinfo(tzs)
        if tzinfo is None:
            raise ValueError(f"unknown TZ string {tzs}")
        return tzinfo
    # otherwise, try to convert by gettz() anyway.
    try:
        tzinfo = tzname_to_tzinfo(tzstr)
    except ValueError as e:
        raise ValueError(f"unknown TZ string {tzstr}")
    return tzinfo

def str_convert_now(dtstr, tzstr, default_tzname):
    tzinfo = tzinfo_from_tzstr(tzstr, default_tzname)
    dt = datetime.now(tz=tzinfo)
    return dt

def str_convert_hexstr(dtstr, tzstr, default_tzname):
    tzinfo = tzinfo_from_tzstr(tzstr, default_tzname)
    dt = num_to_datetime(int(dtstr, 16), unit)
    return dt.replace(tzinfo=tzinfo)

def str_convert_numstr(dtstr, tzstr, default_tzname, unit="seconds"):
    tzinfo = tzinfo_from_tzstr(tzstr, default_tzname)
    n = float(dtstr)
    if n > 9999999999:
        n /= 1000
    dt = num_to_datetime(n, unit)
    return dt.replace(tzinfo=tzinfo)

def str_to_datetime(dttz_str, default_tzname="GMT", unit="seconds"):
    r"""
    convert the datetime string into an timezone-aware datetime object.
        dttz_str: datetime string, acceptable strings are:
            now[TZSTR]
            0x[a-fA-F\d]+[TZSTR]
            [\d\.]+[TZSTR]
            whatever dateutil.parser() can accept.
        default_tzname: will be used as the timezone name in case the dtstr
            doesn't have a timezone.
        unit: valid if dtstr is a number. specify the unit of datestr number.
    """
    patt = [
            { "regex": r"(?P<dtstr>now)(?P<tzstr>.*)", "func": str_convert_now },
            { "regex": r"(?P<dtstr>0x[a-fA-F0-9]+)(?P<tzstr>.*)", "func": str_convert_hexstr },
            { "regex": r"(?P<dtstr>[\d\.]+)(?P<tzstr>.*)", "func": str_convert_numstr },
        ]
    try:
        dt = dtparser.parse(dttz_str)
    except dtparser._parser.ParserError as e:
        for rp in patt:
            r = re.match(rp["regex"], dttz_str)
            if r:
                dt = rp["func"](r.group("dtstr"), r.group("tzstr"), default_tzname)
                return dt
        else:
            raise ValueError(f"ERROR: unknown format {dttz_str}")
    else:
        return dt

def str_to_timedelta(given_str):
    """
    days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]
    """
    r = re.match(r"[\d,\.]+$", given_str)
    if not r:
        raise ValueError("ERROR: arg must consist of [\\d,\\.]+")
    params = ["days","seconds","microseconds","milliseconds","minutes","hours","weeks"]
    args = [int(i) for i in given_str.split(",")]
    return timedelta(**dict(zip(params,args)))

