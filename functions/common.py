

def remove_unused_keys(data):
    new_data = {}
    for key,value in data.items():
        if value:
            new_data[key] = value
    return new_data