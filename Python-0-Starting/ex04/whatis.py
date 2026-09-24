import sys

args = sys.argv[1:]
try:
	if len(args) == 0:
		sys.exit
	elif len(args) > 1:
		raise AssertionError("more than one argument is provided")
	try:
		n = int(args[0])
	except ValueError:
		raise AssertionError("argument is not an integer")
	if n % 2 == 0:
		print("I'm Even.")
	else:
		print("I'm Odd.")
except AssertionError as error:
    print(f"AssertionError: {error}")