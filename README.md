timeutil.py
===========

yet another kitchen nife for datetime.

## usage

      timeutil.py [-m opt] [-z str] [-vd] STR
    
        This command converts STR into the format specified.
        STR is a datetime string.
    
      timeutil.py [-m opt] [-z str] [-avd] STR1 STR2
    
        This command shows the difference of time between STR1 and STR2.
        STR1 is a datetime string as same as STR2.
    
      timeutil.py [-m opt] [-z str] [-avd] STR1 (+|-|/|x) STR2
    
        This command shows the result where the operand is adopted.
        STR1 is a datetime string.  STR2 is a string, which is the arguments
        of the timedelta object in python.  The STR2 format is like below:
    
          days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]
    
      if STR is "now", current time is used.
      "opt" of the -m option may be one of the following string.
    
          iso: iso8601. (default)
         msec: seconds with miliseconds from 00:00:00 1-Jan-1970.
               e.g. 1491395277944.524
        ctime: ctime(3). e.g. Sat Jul 29 16:37:02 JST 2017
          day: days from 00:00:00 1-Jan-1970.
         hour: hours from 00:00:00 1-Jan-1970.
          min: minutes from 00:00:00 1-Jan-1970.
          sec: seconds from 00:00:00 1-Jan-1970.
    
      if an operand is not specified, "-" is used.

