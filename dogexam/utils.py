# The utilities functions for dogexam.

import os
import json
import datetime

def check_file_exists(file_path):
    """ Check whether the file at file_path exists. """

    if os.path.isfile(file_path):
        return True
    else:
        return False


def check_date_string(date):
    """ Return True if the input string is a valid YYYY-MM-DD date, False
        otherwise. """

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False

    return True


def read_config(config_file):
    """ Read and validate configuration file stored at config_file location. """

    if not check_file_exists(config_file):
        raise NameError("Error: Cannot read config file at " + config_file)

    with open(config_file, "r") as config_f:
        config = json.load(config_f)

    if not isinstance(config['irc_port'], int):
        raise ValueError("Error: Invalid irc_port, must be an integer.")

    if not 0 < config['irc_port'] < 65536:
        raise ValueError("Error: Invalid irc_port, must be between 1 - 65535.")

    if len(config['irc_nickname']) < 3:
        raise ValueError("Error: Invalid irc_nickname, must be at least 3 characters long.")

    if len(config['irc_channels']) < 1:
        print("Warning: no channel set in config/config.json, no channel will be connected.")

    return config
