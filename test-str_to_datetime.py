from datetime_util import str_to_datetime
from datetime import datetime
from dateutil.parser import parse as dtparse
from dateutil.tz import gettz as dtgettz

# for the some tests, removed seconds to compare two times.

def test_010():
    a = str_to_datetime("now").isoformat(timespec="minutes")
    b = datetime.now(dtgettz("GMT")).isoformat(timespec="minutes")
    print(a)
    print(b)
    assert a == b

def test_020():
    a = str_to_datetime("now+01:00").isoformat(timespec="minutes")
    b = datetime.now(dtgettz("UTC+01:00")).isoformat(timespec="minutes")
    print(a)
    print(b)
    assert a == b

def test_030():
    a = str_to_datetime("now@CET").isoformat(timespec="minutes")
    b = datetime.now(dtgettz("CET")).isoformat(timespec="minutes")
    print(a)
    print(b)
    assert a == b

def test_090():
    a = str_to_datetime("2017-04-05 12:27:57.123456+01:00")
    b = dtparse("2017-04-05 12:27:57.123456+01:00")
    print(a)
    print(b)
    assert a == b

if __name__ == "__main__":
    #test_010()
    test_090()
    pass
