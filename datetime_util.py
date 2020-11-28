from datetime import datetime, timedelta, timezone
import dateutil.tz
import dateutil.parser
import re

"""
datetime_util:
    The internal timezone is always GMT.
"""

__tz_gmt = dateutil.tz.gettz("GMT")
__epoch = datetime(1970, 1, 1, tzinfo=__tz_gmt)

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

def timedelta_to_datestr(time_delta, output_form="iso", output_rounded=False,
                         output_tzname=None):
    if output_form in ["iso", "iso8601", "ctime"]:
        raise NotImplementedError
    elif output_form == "hex":
        return hex(round(time_delta.total_seconds()))
    elif output_form in ["years", "year"]:
        result = time_delta.total_seconds() / 86400 / 365   # TBD
        if output_rounded:
            return str(int(result))
        else:
            return str(round(result, 3))
    elif output_form in ["months", "month"]:
        result = time_delta.total_seconds() / 86400 / 30   # TBD
        if output_rounded:
            return str(int(result))
        else:
            return str(round(result, 3))
    elif output_form in ["weeks", "week"]:
        result = time_delta.total_seconds() / 86400 / 7
        if output_rounded:
            return str(int(result))
        else:
            return str(round(result, 3))
    elif output_form in ["days", "day"]:
        # equal to time_delta.days
        result = time_delta.total_seconds() / 86400
        if output_rounded:
            return str(int(result))
        else:
            return str(round(result, 3))
    elif output_form in ["hours", "hour"]:
        result = time_delta.total_seconds() / 3600
        if output_rounded:
            return str(int(result))
        else:
            return str(round(result,3))
    elif output_form in ["minutes", "min"]:
        result = time_delta.total_seconds() / 60
        if output_rounded:
            return str(int(result))
        else:
            return str(round(result,3))
    elif output_form in ["seconds", "sec"]:
        return str(int(time_delta.total_seconds()))
    elif output_form in ["milliseconds", "msec"]:
        return str(int(time_delta.total_seconds() * 1000))
    elif output_form in ["microseconds", "usec"]:
        return str(int(time_delta.total_seconds() * 1000000))
    else:
        raise ValueError("unknown output_form {}.".format(output_form))

def datetime_to_datestr(dt, output_form="iso", output_rounded=False,
                        output_tzname=None):
    if output_tzname is not None:
        dt = dt.astimezone(dateutil.tz.gettz(output_tzname))
    if output_form in ["iso", "iso8601"]:
        return dt.isoformat("T")
    elif output_form == "ctime":
        return dt.ctime()
    return timedelta_to_datestr(dt - __epoch, output_form=output_form,
                                output_rounded=output_rounded)

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

def tzinfo_from_datestr(datestr, default_tzname):
    """
    return datetime_string and tzinfo.
    """
    if datestr.find("+") > 0:
        dt_str, diff_str = datestr.split("+")
        if diff_str.find(":"):
            timediff = float(diff_str.replace(":","."))
            return dt_str, timezone(timedelta(hours=timediff))
        else:
            raise ValueError("a timediff string must have a colon.")
    else:
        tz = dateutil.tz.gettz(default_tzname)
        if tz is None:
            raise ValueError("unknown TZ name")
        return datestr, tz

def datestr_to_datetime(datestr, default_tzname="GMT", replace_tz=False,
                        unit="seconds"):
    """
    convert the datetime string into an timezone-aware datetime object.
        datestr: datetime string, acceptable strings are:
            now
            ^0x[a-fA-F\d]+$
            ^[\d\.]+$
            whatever dateutil.parser() can accept.
        default_tzname: will be used as the timezone name in case the datestr
            doesn't have a timezone.
        replace_tz: indicates to replace the timezone name by the
            default_tzname.
        unit: specify the unit of the datetime object converted.
    """
    if datestr == "now":
        dt = datetime.now()
        # datetime.now() always doesn't have tzinfo.
        tzinfo = dateutil.tz.gettz(default_tzname)
    else:
        dtstr, tzinfo = tzinfo_from_datestr(datestr, default_tzname)
        if re.match("^0x[a-fA-F\d]+$", dtstr):
            dt = numstr_to_datetime(int(dtstr, 16), unit)
        elif re.match("^[\d\.]+$", dtstr):
            n = float(dtstr)
            if n > 9999999999:
                n /= 1000
            dt = numstr_to_datetime(n, unit)
        else:
            dt = dateutil.parser.parse(dtstr)
        # replace default_tzname if needed.
        if replace_tz is True:
            tzinfo = dateutil.tz.gettz(default_tzname)
    return dt.replace(tzinfo=tzinfo)

def datestr_to_timedelta(given_str):
    """
    days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]
    """
    r = re.match("[\d,\.]+$", given_str)
    if not r:
        raise ValueError("ERROR: arg must consist of [\\d,\\.]+")
    return eval("timedelta(" + given_str + ")")

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

