def remove_null_values_recursive(obj):
    if isinstance(obj, dict):
        return {key: remove_null_values_recursive(value) for key, value in obj.items() if value is not None}
    elif isinstance(obj, list):
        return [remove_null_values_recursive(item) for item in obj if item is not None]
    else:
        return obj


def dict_slice_keys(dict, keys_to_include):
    return {k:v for k,v in dict.items() if k in keys_to_include}

def dict_slice_not_keys(dict, keys_to_include):
    return {k:v for k,v in dict.items() if k not in keys_to_include}