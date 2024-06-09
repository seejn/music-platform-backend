def check_required_fields(input_fields, required_fields):
    for field in required_fields:
        print(field not in input_fields)
        if field not in input_fields:
            return False
    return True

def does_field_exist(input_fields, required_fields):
    for field in input_fields:
        print(field not in required_fields)
        if field not in required_fields:
            return False
    return True
