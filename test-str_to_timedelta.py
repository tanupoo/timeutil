from datetime_util import str_to_timedelta
from datetime import timedelta

def test_01():
    a = str_to_timedelta("1")
    b = timedelta(days=1)
    print(a)
    print(b)
    assert a == b

def test_02():
    a = str_to_timedelta("1,2")
    b = timedelta(days=1,seconds=2)
    print(a)
    print(b)
    assert a == b

def test_03():
    a = str_to_timedelta("1,2,3")
    b = timedelta(days=1,seconds=2,microseconds=3)
    print(a)
    print(b)
    assert a == b

def test_04():
    a = str_to_timedelta("1,2,3,4")
    b = timedelta(days=1,seconds=2,microseconds=3,milliseconds=4)
    print(a)
    print(b)
    assert a == b

def test_05():
    a = str_to_timedelta("1,2,3,4,5")
    b = timedelta(days=1,seconds=2,microseconds=3,milliseconds=4,minutes=5)
    print(a)
    print(b)
    assert a == b

def test_06():
    a = str_to_timedelta("1,2,3,4,5,6")
    b = timedelta(days=1,seconds=2,microseconds=3,milliseconds=4,minutes=5,hours=6)
    print(a)
    print(b)
    assert a == b

def test_07():
    a = str_to_timedelta("1,2,3,4,5,6,7")
    b = timedelta(days=1,seconds=2,microseconds=3,milliseconds=4,minutes=5,
                  hours=6,weeks=7)
    print(a)
    print(b)
    assert a == b

if __name__ == "__main__":
    test_07()
    pass
