timeutil.py
===========

yet another kitchen nife for datetime conversion.

## usage

Below command converts STR into the format specified.
STR is a datetime string.

```
timeutil.py [-m opt] [-z str] [-vd] STR
```

Below command shows the difference of time between STR1 and STR2.
STR1 is a datetime string as same as STR2.

```
timeutil.py [-m opt] [-z str] [-avd] STR1 STR2
```

Below command shows the result where the operand is adopted.
STR1 is a datetime string.

```
timeutil.py [-m opt] [-z str] [-avd] STR1 (+|-|/|x) STR2
```

STR2 is a string, which is the arguments
of the timedelta object in python.  The STR2 format is like below:

```
days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]
```

If STR is "now", current time is used.

"opt" of the -m option may be one of the following string.
if an operand is not specified, "-" is used.

```
  iso: iso8601. (default)
 msec: seconds with miliseconds from 00:00:00 1-Jan-1970.
       e.g. 1491395277944.524
ctime: ctime(3). e.g. Sat Jul 29 16:37:02 JST 2017
  day: days from 00:00:00 1-Jan-1970.
 hour: hours from 00:00:00 1-Jan-1970.
  min: minutes from 00:00:00 1-Jan-1970.
  sec: seconds from 00:00:00 1-Jan-1970.
```

Below command converts from a number taken
from a system runing with local timezone
into a datetime string with the local timezone.

```
$ timeutil.py 1671692020.652136 -i Asia/Tokyo
2022-12-22T06:53:40.652136+09:00
```

```
$ timeutil.py 1671692020.652136@Asia/Tokyo
2022-12-22T06:53:40.652136+09:00
```

## full usage

```
Description:

  Yet another kitchen nife to handle the time strings.

  If a string is either:
      1. a hex string.
      2. a number.
      3. now will be a current time.
      4. a iso6801 like string.

  Even when the time string is not formed to ISO8601, a timezone name or
  offset can be added at the end of the string in case of above 1, 2, and 3.
  Below is the accepted way to specify the timezone of the time string:

        TIME_STR+TZ_OFFSET
        TIME_STR-TZ_OFFSET
        TIME_STR@TZ_STR
        TIME_STRTZ_STR

  For example,

      now@Europe/Paris
      now-7:00
      1671692020.652136+1:00
      1491391677.123@America/Los_Angeles

  The -m option may be used to specify the output format.
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

Examples

  timeutil.py [options] STR1

    This command converts STR1 into the format specified.
    STR1 is a datetime string.

  timeutil.py [options] STR1 STR2

    This command shows the difference of time between STR1 and STR2.
    STR1 is a datetime string as same as STR2.
    "epoch" is acceptable as STR2, which means 1970-01-01T00:00:00

  timeutil.py [options] STR1 (+|-|/|x) STR2

    This command shows the result where the operand is adopted.
    STR1 is a datetime string.  STR2 is a string, which is the arguments
    of the timedelta object in python.  The STR2 format is like below:

      days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]

positional arguments:
  ARGs [...]            a datetime string such as iso8601, ctime, timestamp,
                        etc.

options:
  -h, --help            show this help message and exit
  -m OUTPUT_FORMAT      specify the output format. default is 'iso'.
  --rounding DIGIT, -R DIGIT
                        specify a digit to round the output.
  --input-tz DEFAULT_INPUT_TZNAME, -i DEFAULT_INPUT_TZNAME
                        specify the timezone name for the input string in case
                        the datetime string doesn't have any timezone. default
                        is GMT
  --replace-str1-tz, -r
                        replace the STR1's timezone into the one specified by
                        --input-tz even when the datetime has a timezone.
  --output-tz OUTPUT_TZNAME, -o OUTPUT_TZNAME
                        specify the timezone to show. default is same as the
                        one specified by the --input-tz option
  -v                    enable verbose mode.
```
