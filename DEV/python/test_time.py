# from datetime import timedelta

# UNITS = {"s":"second", "m":"minute", "h":"hour", "D":"day", "W":"week", "M":"month", "Y":"year"}

# def convert_to_seconds(s):
#     count = int(s[:-1])
#     unit = UNITS[ s[-1] ]
#     td = timedelta(**{unit: count})
#     return td.seconds + 60 * 60 * 24 * td.days

SECONDS_PER_UNIT = {"second":1, "minute":60, "hour":60*60, "day":60*60*24, "week":60*60*24*7, "month":60*60*24*7*30, "year":60*60*24*7*365}

def convert_to_seconds(s):
	s = s.split(" ")
	return int(s[0]) * SECONDS_PER_UNIT[s[1]]


print(convert_to_seconds("1 minute"))