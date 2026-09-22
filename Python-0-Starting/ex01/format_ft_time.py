import datetime

now = datetime.datetime.now()
snow = now.timestamp()
fnow = now.strftime("%b %d %Y")

print(f"Seconds since January 1, 1970: {snow:,.4f} or "
      f"{snow:.2e} in scientific notation")
print(fnow)
