#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import argparse
from argparse import RawDescriptionHelpFormatter
from datetime_util import *

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

def timedelta_to_sec(delta, f_abs=False):
    if f_abs:
        delta = abs(delta)
    return delta.total_seconds()

def timedelta_to_msec(delta, f_abs=False):
    if f_abs:
        delta = abs(delta)
    return delta.total_seconds()

def parse_args():
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
  "opt" of the -m option may be one of the following string.

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
    p = argparse.ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            description=desc,
            usage=usage,
            epilog="")
    p.add_argument("args", metavar="ARGs [...]", type=str, nargs="*",
        help="a datetime string such as iso8601, ctime, timestamp, etc.")
    p.add_argument("-m", action="store", dest="mode", default="default",
        choices=["iso","ctime","day","hour","min","sec","msec","usec","hex"],
        help="specify the output format. default is 'iso'")
    p.add_argument("-z", action="store", dest="tzname", default="GMT",
        help="specify the name of timezone like 'Asia/Tokyo'.")
    p.add_argument("-a", action="store_true", dest="f_abs", default=False,
        help="specify to adopt abs() into the result.")
    p.add_argument("-v", action="store_true", dest="f_verbose", default=False,
        help="enable verbose mode.")
    p.add_argument("-d", action="append_const", dest="_f_debug", default=[],
        const=1, help="increase debug mode.")
    args = p.parse_args()
    args.debug_level = len(args._f_debug)
    return p

'''
test code
'''
if __name__ == "__main__" :
    parser = parse_args()
    opt = parser.parse_args()
    #
    if len(opt.args) == 1:
        if opt.mode == "default":
            opt.mode = "iso"
        output_func = eval("datetime_to_%s" % opt.mode)
        dt1 = datestr_to_datetime(opt.args[0])
        ret = output_func(dt1)
    #
    elif len(opt.args) == 2 and opt.args[1] in ["-", "+", "/", "x"]:
        '''
        this is the case where the 3rd argument comes from the stdin.
        '''
        print("NOT SUPPORTED YET")
        exit(1)
    #
    elif len(opt.args) == 2:
        if opt.mode == "default":
            opt.mode = "sec"
        elif opt.mode in ["iso","ctime"]:
            parser.print_help()
            exit(1)
        output_func = eval("timedelta_to_%s" % opt.mode)
        dt1 = datestr_to_datetime(opt.args[0])
        dt2 = datestr_to_datetime(opt.args[1])
        ret = output_func(dt1 - dt2, f_abs=opt.f_abs)
    #
    elif len(opt.args) == 3:
        op = opt.args[1]
        if op in ["-", "+"]:
            if opt.mode == "default":
                opt.mode = "iso"
            dt1 = datestr_to_datetime(opt.args[0])
            delta = datestr_to_timedelta(opt.args[2])
            ret = eval("datetime_to_%s(dt1 %s delta)" % (opt.mode, op))
        elif op in ["/", "x"]:
            if opt.mode == "default":
                opt.mode = "sec"
            if op == "/":
                op = "//"
            elif op == "x":
                op = "*"
            dt1 = datestr_to_timestamp_msec(opt.args[0])
            num = int(opt.args[2])
            ret = eval("timedelta_to_%s(dt1 %s num)" % (opt.mode, op))
        else:
            parser.print_help()
            exit(1)
    #
    else:
        parser.print_help()
        exit(1)
    #
    print(ret)
