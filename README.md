
## Usage

datetime [-m opt] STR1

    convert STR1 into the format specified.

datetime [-m opt] [-vdh] STR1 [+|-|/] STR2

    show the result to adopt the operand into STR1 and STR2.

if STR is "now", current time is used.
"opt" of the -m option may be one of the following string.

      iso: iso8601. (default)
      day: days
     hour: hours
      min: minutes
      sec: seconds
       ms: timestamp with miliseconds.  e.g. 1491395277944.524
    ctime: ctime(3). e.g. Sat Jul 29 16:37:02 JST 2017
