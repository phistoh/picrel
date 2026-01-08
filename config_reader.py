import configparser
import os.path


def get_config():
    # check if config file exists, if not: create Default one
    if not os.path.isfile("config.ini"):
        print("No config found.")
        return None

    config = configparser.ConfigParser()
    config.read("config.ini")
    return config
