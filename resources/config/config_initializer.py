import json
import os

path_to_current_config_folder = r'project_data/config/current_config'
path_to_current_config_json = r'project_data/config/current_config/config.json'
path_to_default_config_json = r'resources/defaults/config.json'


def load_initial_config():
    """ :return default or an existing config dict"""

    def create_current_config_from_default():
        """ Creates a default config file when the current config file is missing
            :returns config dict with that info
        """
        with open(path_to_current_config_json, 'w') as f:
            with open(path_to_default_config_json) as g:
                json.dump(json.load(g), f, indent=2, sort_keys=True)

        with open(path_to_current_config_json) as f:
            current_config_json = json.load(f)
        return current_config_json

    if not os.path.isdir(path_to_current_config_folder):
        os.makedirs(path_to_current_config_folder)

    if os.path.isfile(path_to_current_config_json):
        with open(path_to_current_config_json) as f:
            current_config_json = json.load(f)
        return current_config_json
    else:
        return create_current_config_from_default()
