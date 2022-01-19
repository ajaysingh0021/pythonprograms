#
# Name: convert_12_24_hours.py
# Purpose: Convert 12-hour time to 24-hour time
# Author: Ajay Singh
# Date: 19th Jan 2022

# AM time
s="12:01:00AM"
if int(s[:2]) == 12:
    s = "00" + s[2:]
if "am" in s.lower():
    print(s[:-2])
else:
    new_hour =  int(s[:2]) + 12
    print(str(new_hour) + s[2:-2])
    

# PM time
s="12:01:00PM"
if int(s[:2]) == 12:
    s = "00" + s[2:]
if "am" in s.lower():
    print(s[:-2])
else:
    new_hour =  int(s[:2]) + 12
    print(str(new_hour) + s[2:-2])

