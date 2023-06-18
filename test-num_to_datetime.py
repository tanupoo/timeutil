from datetime_util import num_to_datetime
from dateutil.parser import parse as dtparse

def test_01():
    a = num_to_datetime(1491395277, "seconds")
    b = dtparse("2017-04-05 12:27:57+00:00")
    print(a)
    print(b)
    assert a == b

def test_02():
    a = num_to_datetime(1491395277123, "milliseconds")
    b = dtparse("2017-04-05 12:27:57.123000+00:00")
    print(a)
    print(b)
    assert a == b

def test_03():
    a = num_to_datetime(1491395277123456, "microseconds")
    b = dtparse("2017-04-05 12:27:57.123456+00:00")
    print(a)
    print(b)
    assert a == b

if __name__ == "__main__":
    test_01()
    test_02()
    test_03()
