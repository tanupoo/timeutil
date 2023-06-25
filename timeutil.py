#!/usr/bin/env python

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import environ
from datetime_util import *

DEFAULT_TZNAME = environ.get("TZ", "GMT")

usage = '''
  %(prog)s [options] STR1

    This command converts STR1 into the format specified.
    STR1 is a datetime string.

  %(prog)s [options] STR1 STR2

    This command shows the difference of time between STR1 and STR2.
    STR1 is a datetime string as same as STR2.
    "epoch" is acceptable as STR2, which means 1970-01-01T00:00:00

  %(prog)s [options] STR1 (+|-|/|x) STR2

    This command shows the result where the operand is adopted.
    STR1 is a datetime string.  STR2 is a string, which is the arguments
    of the timedelta object in python.  The STR2 format is like below:

      days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]

'''

desc = '''
description:
  yet another kitchen nife to handle the time strings.

  if a string is either:
      1. a hex string.
      2. a number.
      3. now will be a current time.
      4. a iso6801 like string.

  A timezone name or offset can be added at the end of the string.
  '@' (atmark) can be used as a delimiter to specify the timezone
  if the string is like above 1, 2, and 3,
  For example, now@Europe/Paris, 1491391677.123@JST

  the -m option may be used to specify the output format.
  It is one of the following string.

      iso: iso8601. (default)
    ctime: ctime(3). e.g. Sat Jul 29 16:37:02 JST 2017
      day: days from 1970-01-01T00:00:00 (epoch).
     hour: hours from epoch.
      min: minutes from epoch.
      sec: seconds from epoch.
     msec: miliseconds from epoch.
           e.g. 1546919546426 if datetime object is like below:
                datetime.datetime(2019, 1, 8, 12, 52, 26, 426765)
     usec: seconds with microseconds from epoch.
           e.g. 1546919546.426765 if datetime object is like below:
                datetime.datetime(2019, 1, 8, 12, 52, 26, 426765)
      hex: microseconds in a hex string of the big endian.
      HEX: same as hex, but will be upper case.

  e.g.
'''

ap = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=desc,
        usage=usage,
        epilog="")
ap.add_argument("args", metavar="ARGs [...]", type=str, nargs="*",
                help="a datetime string such as iso8601, ctime,"
                " timestamp, etc.")
ap.add_argument("-m", action="store", dest="output_format",
                help="specify the output format. default is 'iso'.")
ap.add_argument("--rounding", "-R",
                action="store", dest="digit",
                type=int, default=3,
                help="specify a digit to round the output.")
ap.add_argument("--input-tz", "-i", action="store", dest="default_input_tzname",
                help="specify the timezone name for the input string"
                " in case the datetime string doesn't have any timezone."
                f"  default is {DEFAULT_TZNAME}")
ap.add_argument("--replace-str1-tz", "-r", action="store_true", dest="replace_str1_tz",
                help="replace the STR1's timezone "
                " into the one specified by --input-tz"
                " even when the datetime has a timezone.")
ap.add_argument("--output-tz", "-o", action="store", dest="output_tzname",
                help="specify the timezone to show."
                "  default is same as the one specified by"
                " the --input-tz option")
ap.add_argument("-v", action="store_true", dest="verbose",
                help="enable verbose mode.")
opt = ap.parse_args()

if not opt.default_input_tzname:
    opt.default_input_tzname = DEFAULT_TZNAME
#
if opt.verbose:
    print("Default Input Timezone:", opt.default_input_tzname)
    print("Output Timezone:", opt.output_tzname)
    print("Replace STR1 Timezone:", opt.replace_str1_tz)

# conversion
def conversion(opt):
    if len(opt.args) == 1:
        #
        if opt.output_format is None:
            opt.output_format = "iso"
        dt1 = str_to_datetime(opt.args[0],
                              default_tzname=opt.default_input_tzname)
        if opt.replace_str1_tz:
            dt1 = dt1.replace(
                    tzinfo=tzinfo_from_tzstr(opt.default_input_tzname))
        if opt.verbose:
            print("STR1:", dt1)
        result = datetime_to_str(dt1, output_form=opt.output_format,
                                 digit=opt.digit,
                                 output_tzname=opt.output_tzname)
    elif len(opt.args) == 2:
        #
        if opt.output_format is None:
            opt.output_format = "sec"
        dt1 = str_to_datetime(opt.args[0],
                              default_tzname=opt.default_input_tzname)
        if opt.replace_str1_tz:
            dt1 = dt1.replace(
                    tzinfo=tzinfo_from_tzstr(opt.default_input_tzname))
        if opt.args[1] in ["epoch", "EPOCH"]:
            arg2 = "1970-01-01T00:00:00"
        else:
            arg2 = opt.args[1]
        dt2 = str_to_datetime(arg2, default_tzname=opt.default_input_tzname)
        if opt.verbose:
            print("STR1:", dt1)
            print("STR2:", dt2)
        result = timedelta_to_str(dt1 - dt2, output_form=opt.output_format,
                                        output_tzname=opt.output_tzname)
    elif len(opt.args) == 3:
        #
        if opt.output_format is None:
            opt.output_format = "iso"
        dt1 = str_to_datetime(opt.args[0],
                              default_tzname=opt.default_input_tzname)
        if opt.replace_str1_tz:
            dt1 = dt1.replace(
                    tzinfo=tzinfo_from_tzstr(opt.default_input_tzname))
        op = opt.args[1]
        time_delta = str_to_timedelta(opt.args[2])
        if opt.verbose:
            print("STR1:", dt1)
            print("STR2:", time_delta)
        if op == "+":
            result = datetime_to_str(dt1 + time_delta,
                                     output_form=opt.output_format,
                                     digit=opt.digit,
                                     output_tzname=opt.output_tzname)
        elif op == "-":
            result = datetime_to_str(dt1 - time_delta,
                                     output_form=opt.output_format,
                                     digit=opt.digit,
                                     output_tzname=opt.output_tzname)
        else:
            ap.print_help()
            exit(1)
    else:
        ap.print_help()
        exit(1)
    #
    return result

try:
    print(conversion(opt))
except Exception as e:
    print(f"ERROR: {e}")
