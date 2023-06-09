def obtain_saves():
    from configparser import ConfigParser
    import os.path
    path = "config.ini"

    config = ConfigParser()

    config["SAVES"] = {
        "max_saves": "5"
    }

    if not os.path.isfile(path): 
        with open("config.ini", "w") as conf:
            config.write(conf)
        return 5
    else:
        config.read("config.ini")
        saves_config = config["SAVES"]
        return int(saves_config['max_saves'])