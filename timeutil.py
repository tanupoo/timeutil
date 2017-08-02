#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import argparse
from argparse import RawDescriptionHelpFormatter
from datetime_util import *

def datetime_to_iso(dt):
    return dt.isoformat()

def datetime_to_day(dt):
    return datetime_to_timestamp_days(dt)

def datetime_to_hour(dt):
    return datetime_to_timestamp_hours(dt)

def datetime_to_min(dt):
    return datetime_to_timestamp_minutes(dt)

def datetime_to_sec(dt):
    return datetime_to_timestamp(dt)

def datetime_to_msec(dt):
    return datetime_to_timestamp_msec(dt)

def datetime_to_ctime(dt):
    return dt.ctime()

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
  %(prog)s [-m opt] [-z str] [-vd] STR1

    convert STR1 into the format specified.

  %(prog)s [-m opt] [-z str] [-avd] STR1 [+|-|/|x] STR2

    show the result to adopt the operand into STR1 and STR2.
'''
    desc = '''
description:
  yet another kichen nife for datetime.
  if STR is "now", current time is used.
  "opt" of the -m option may be one of the following string.

      iso: iso8601. (default)
      day: days
     hour: hours
      min: minutes
      sec: seconds
     msec: timestamp with miliseconds.  e.g. 1491395277944.524
    ctime: ctime(3). e.g. Sat Jul 29 16:37:02 JST 2017

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
        choices = ["iso","day","hour","min","sec","msec","ctime"],
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
        if opt.mode == "default":
            opt.mode = "sec"
        elif opt.mode in ["iso","ctime"]:
            parser.print_help()
            exit(1)
        output_func = eval("timedelta_to_%s" % opt.mode)
        dt1 = datestr_to_datetime(opt.args[0])
        op = opt.args[1]
        dt2 = datestr_to_datetime(opt.args[2])
        if op == "-":
            ret = output_func(dt1 - dt2, f_abs=opt.f_abs)
        elif op == "+":
            ret = output_func(dt1 + dt2)
        elif op == "/":
            ret = output_func(dt1 // dt2)
        elif op == "x":
            ret = output_func(dt1 // dt2)
        else:
            parser.print_help()
            exit(1)
    #
    else:
        parser.print_help()
        exit(1)
    #
    print(ret)
