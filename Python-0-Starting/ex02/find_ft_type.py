def all_thing_is_obj(object: any) -> int:
	var_type = type(object)
	flag = True
	if (var_type == list):
		print("List :", var_type)
	elif (var_type == tuple):
		print("Tuple :", var_type)
	elif (var_type == set):
		print("Set :", var_type)
	elif (var_type == dict):
		print("Dict :", var_type)
	elif (var_type == str):
		print(object, "is in the kitchen :", var_type)
	else:
		print("Type not found")
	return 42