from resources.configs.globals import path_to_config_json
import json


def get_app_config():
    with open(path_to_config_json) as f:
        configs = json.load(f)
    return configs


def update_config():
    pass
