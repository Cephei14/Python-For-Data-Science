def all_thing_is_obj(object: any) -> int:
    var_type = type(object)
    if var_type is list:
        print(f"List : {var_type}")
    elif var_type is tuple:
        print(f"Tuple : {var_type}")
    elif var_type is set:
        print(f"Set : {var_type}")
    elif var_type is dict:
        print(f"Dict : {var_type}")
    elif var_type is str:
        print(f"{object} is in the kitchen : {var_type}")
    else:
        print("Type not found")
    return 42
