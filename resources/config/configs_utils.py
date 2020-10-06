from resources.config.config_initializer import path_to_current_config_folder, path_to_default_config_json, \
    path_to_current_config_json
import json
import os
from datetime import datetime


def get_current_config_json():
    """ :return an existing config dict from an existing config file """
    with open(path_to_current_config_json) as f:
        current_config_json = json.load(f)
    return current_config_json


def update_config(config_dict):
    """ Makes the backup and config update of the config file keys using the config dict passed
        :arg config_dict : dict containing the key values to update
     """
    def save_current_config_file_into_previous_configs_folder():
        """ Makes the backup of the current config into the previous config folder,
            naming the file with date and time
            :return path to the saved config file
        """
        current_config_json = get_current_config_json()

        if not os.path.isdir(current_config_json['config']['path_to_previous_config_folder']):
            os.makedirs(current_config_json['config']['path_to_previous_config_folder'])

        sdatetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        filepath_to_save = os.path.join(current_config_json['config']['path_to_previous_config_folder'],
                                        sdatetime + '.json')

        with open(filepath_to_save, 'w') as g:
            json.dump(current_config_json, g, indent=2, sort_keys=True)

        return filepath_to_save

    def update_config_values():
        """ Updates the current configuration using the config_dict passed to the parent function
            :return json type config variable: for writing the current config file
        """
        print('Updating config.json')
        config_to_update = get_current_config_json()
        config_to_update['config']['path_to_previous_config_file'] = previous_config_path
        for conf in config_dict:
            try:
                config_to_update['config'][conf] = config_dict[conf]
                print(f'Config value {conf} UPDATED')
            except KeyError as e:
                print(f'\n{conf} is not a valid config, {e}')
        print('Config UPDATED')
        return config_to_update

    def save_updated_config():
        """ Saves the updated configuration into the json config file """
        with open(path_to_current_config_json, 'w') as f:
            json.dump(updated_config, f, indent=2)

    # Backup
    previous_config_path = save_current_config_file_into_previous_configs_folder()

    # Update parameters: config_dict -> current_config_dict
    updated_config = update_config_values()

    # Save new config.json
    save_updated_config()

    print(json.dumps(get_current_config_json(), indent=2, sort_keys=True))
