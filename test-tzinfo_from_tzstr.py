from datetime_util import tzinfo_from_tzstr
from dateutil.tz import gettz as dtgettz
from datetime import timezone, timedelta

# America/New_York UTC-4 EDT
# America/New_York UTC-5 EST
# Europe/Berlin    UTC+1 CET
# Europe/Berlin    UTC+2 CEST

"""
+01:00
-01:00
+01:30
-01:30
@CET
@America/New_York
"""

def test_01():
    a = tzinfo_from_tzstr(None)
    b = dtgettz("GMT")
    print(a)
    print(b)
    assert a == b

def test_02():
    a = tzinfo_from_tzstr("")
    b = dtgettz("GMT")
    print(a)
    print(b)
    assert a == b

def test_03():
    a = tzinfo_from_tzstr("+01:00")
    b = timezone(timedelta(hours=1))
    print(a)
    print(b)
    assert a == b

def test_04():
    a = tzinfo_from_tzstr("-01:00")
    b = timezone(timedelta(hours=-1))
    print(a)
    print(b)
    assert a == b

def test_05():
    a = tzinfo_from_tzstr("+01:30")
    b = timezone(timedelta(hours=1.5))
    print(a)
    print(b)
    assert a == b

def test_06():
    a = tzinfo_from_tzstr("-01:30")
    b = timezone(timedelta(hours=-1.5))
    print(a)
    print(b)
    assert a == b

def test_07():
    a = tzinfo_from_tzstr("@CET")
    b = dtgettz("CET")
    print(a)
    print(b)
    assert a == b

def test_08():
    a = tzinfo_from_tzstr("@Europe/Berlin")
    b = dtgettz("Europe/Berlin")
    print(a)
    print(b)
    assert a == b

if __name__ == "__main__":
    test_08()
    pass
