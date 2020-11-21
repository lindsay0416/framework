import time  # This is required to include time module.
import calendar

ticks = time.time()
localTime = time.localtime(time.time())
readableLocaltime = time.asctime(time.localtime(time.time()))
print("Number of ticks since 12:00am, January 1, 1970:", ticks)
print(localTime)
print(localTime.tm_year)
print(readableLocaltime)


cal = calendar.month(2008, 1)
print("Here is the calendar:")
print(cal)
