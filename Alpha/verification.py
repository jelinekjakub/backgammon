
def save_exists():
    import glob
    results = glob.glob("saves/????????-??????.json")
    if results:
        return True
    else:
        return False
    return 
def list_int(x, item_list) -> bool:
    try:
        x = int(x)
        if x in item_list:
            return True
    except:
        pass
    return False