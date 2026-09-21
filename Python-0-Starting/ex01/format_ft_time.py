import datetime
now = datetime.datetime.now().timestamp()
snow = f"{now:,.4f}"
enow = f"{now:.2e}"
fnow = datetime.datetime.now().strftime("%b %d %Y")
print("Seconds since January 1, 1970:",snow, "or" , enow, "in scientific notation")
print(fnow)