from datetime_util import datetime_to_str
from dateutil.parser import parse as dtparse

output_format_strings = [
    "iso",
    "ctime",
    "year",
    "month",
    "week",
    "day",
    "hour",
    "min",
    "sec",
    "msec",
    "usec",
    "hex",
    ]

def test_010():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt)
    b = "2017-04-05T12:27:57.123456+01:00"
    print(a)
    print(b)
    assert a == b

def test_011():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "iso")
    b = "2017-04-05T12:27:57.123456+01:00"
    print(a)
    print(b)
    assert a == b

def test_020():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "ctime")
    b = "Wed Apr  5 12:27:57 2017"
    print(a)
    print(b)
    assert a == b

def test_030():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "years")
    b = "47.292"
    print(a)
    print(b)
    assert a == b

def test_040():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "months")
    b = "575.383"
    print(a)
    print(b)
    assert a == b

def test_050():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "weeks")
    b = "2465.925"
    print(a)
    print(b)
    assert a == b

def test_060():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "days")
    b = "17261.478"
    print(a)
    print(b)
    assert a == b

def test_070():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "hours")
    b = "414275.466"
    print(a)
    print(b)
    assert a == b

def test_080():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "minutes")
    b = "24856527.952"
    print(a)
    print(b)
    assert a == b

def test_090():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "seconds")
    b = "1491391677.123"
    print(a)
    print(b)
    assert a == b

def test_100():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "milliseconds")
    b = "1491391677123.456"
    print(a)
    print(b)
    assert a == b

def test_110():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "microseconds")
    b = "1491391677123456"
    print(a)
    print(b)
    assert a == b

def test_120():
    dt = dtparse("2017-04-05 12:27:57.123456+01:00")
    a = datetime_to_str(dt, "hex")
    b = "58e4d4bd"
    print(a)
    print(b)
    assert a == b

def test_130():
    dt = dtparse("2017-04-05 12:27:57+01:00")
    a = datetime_to_str(dt, "HEX")
    b = "58E4D4BD"
    print(a)
    print(b)
    assert a == b

if __name__ == "__main__":
    test_030()
    #test_120()
    #test_130()
    pass
