#!/usr/bin/env python

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import getenv
from datetime_util import *

DEFAULT_TZNAME = "GMT"

usage = '''
  %(prog)s [-m opt] [-z str] [-vd] STR

    This command converts STR into the format specified.
    STR is a datetime string.

  %(prog)s [-m opt] [-z str] [-avd] STR1 STR2

    This command shows the difference of time between STR1 and STR2.
    STR1 is a datetime string as same as STR2.

  %(prog)s [-m opt] [-z str] [-avd] STR1 (+|-|/|x) STR2

    This command shows the result where the operand is adopted.
    STR1 is a datetime string.  STR2 is a string, which is the arguments
    of the timedelta object in python.  The STR2 format is like below:

      days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]

'''

desc = '''
description:
  yet another kitchen nife for datetime.
  if STR is "now", current time is used.
  "opt" of the -m option may be used to specify the output format.
  It is one of the following string.

      iso: iso8601. (default)
    ctime: ctime(3). e.g. Sat Jul 29 16:37:02 JST 2017
      day: days from 00:00:00 1-Jan-1970.
     hour: hours from 00:00:00 1-Jan-1970.
      min: minutes from 00:00:00 1-Jan-1970.
      sec: seconds from 00:00:00 1-Jan-1970.
     msec: miliseconds from 00:00:00 1-Jan-1970.
           e.g. 1546919546426 if datetime object is like below:
                datetime.datetime(2019, 1, 8, 12, 52, 26, 426765)
     usec: seconds with microseconds from 00:00:00 1-Jan-1970.
           e.g. 1546919546.426765 if datetime object is like below:
                datetime.datetime(2019, 1, 8, 12, 52, 26, 426765)
      hex: microseconds in a hex string of the big endian.

  if an operand is not specified, "-" is used.

  e.g.
'''

ap = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=desc,
        usage=usage,
        epilog="")
ap.add_argument("args", metavar="ARGs [...]", type=str, nargs="*",
                help="""a datetime string such as iso8601, ctime,
                timestamp, etc.""")
ap.add_argument("-m", action="store", dest="output_format",
                default="default",
                help="specify the output format. default is 'iso'")
ap.add_argument("-z", action="store", dest="tzname",
                help="""specify the timezone of the
                input/output datetime string.  It orverwrites both
                --output-tz and --input-tz options.""")
ap.add_argument("--output-tz", action="store", dest="output_tzname",
                help="""specify the timezone to show""")
ap.add_argument("--input-tz", action="store", dest="input_tzname",
                help="""specify the timezone name for
                the input string in case the datetime string doesn't
                have any timezone.""")
ap.add_argument("--replace-tz", action="store_true", dest="replace_tz",
                help="""force to use the timezone name even when the
                datetime string has a timezone.""")
ap.add_argument("-v", action="store_true", dest="verbose",
                help="enable verbose mode.")
opt = ap.parse_args()

# decisding the timezone name.
default_tzname = getenv("TZ")
if default_tzname is None:
    default_tzname = DEFAULT_TZNAME
if opt.input_tzname is None:
    opt.input_tzname = default_tzname
if opt.output_tzname is None:
    opt.output_tzname = default_tzname
if opt.tzname is not None:
    # overwrites the input/output tzname by opt.tzname.
    opt.input_tzname = opt.tzname
    opt.output_tzname = opt.tzname
#
if opt.verbose:
    print("Default Timezone:", default_tzname)
    print("Input Timezone:", opt.input_tzname)
    print("Output Timezone:", opt.output_tzname)

# conversion
if len(opt.args) == 1:
    #
    if opt.output_format == "default":
        opt.output_format = "iso"
    dt1 = datestr_to_datetime(opt.args[0], default_tzname=opt.input_tzname,
                                replace_tz=opt.replace_tz)
    result = datetime_to_datestr(dt1, out_form=opt.output_format,
                                    output_tzname=opt.output_tzname)
elif len(opt.args) == 2:
    #
    if opt.output_format == "default":
        opt.output_format = "sec"
    dt1 = datestr_to_datetime(opt.args[0], default_tzname=opt.input_tzname,
                                replace_tz=opt.replace_tz)
    dt2 = datestr_to_datetime(opt.args[1], default_tzname=opt.input_tzname,
                                replace_tz=opt.replace_tz)
    result = timedelta_to_datestr(dt1 - dt2, out_form=opt.output_format,
                                    output_tzname=opt.output_tzname)
elif len(opt.args) == 3:
    #
    if opt.output_format == "default":
        opt.output_format = "sec"
    dt1 = datestr_to_datetime(opt.args[0], default_tzname=opt.input_tzname,
                                replace_tz=opt.replace_tz)
    op = opt.args[1]
    time_delta = datestr_to_timedelta(opt.args[2])
    if op == "+":
        result = datetime_to_datestr(dt1 + time_delta,
                                        out_form=opt.output_format,
                                        output_tzname=opt.output_tzname)
    elif op == "-":
        result = datetime_to_datestr(dt1 - time_delta,
                                        out_form=opt.output_format,
                                        output_tzname=opt.output_tzname)
    else:
        ap.print_help()
        exit(1)
else:
    ap.print_help()
    exit(1)
#
print(result)
