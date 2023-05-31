
def save_exists():
    import os.path
    return os.path.isfile("result.json")

def list_int(x, item_list) -> bool:
    try:
        x = int(x)
        if x in item_list:
            return True
    except:
        pass
    return False