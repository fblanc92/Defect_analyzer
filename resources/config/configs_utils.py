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
        config_to_update_json = get_current_config_json()
        config_to_update_json['config']['path_to_previous_config_file'] = previous_config_path
        for conf in config_dict:
            try:
                config_to_update_json['config'][conf] = config_dict[conf]
                print(f'Config value {conf} UPDATED')
            except KeyError as e:
                print(f'\n{conf} is not a valid config, {e}')

        # print('Config UPDATED')
        return config_to_update_json

    def set_updated_config():
        """ Saves the updated configuration into the json config file """

        def recreate_register_if_changed():
            """ If the path to the register json file is changed, then creates the needed folder and
                recreates the current register json inside it """

            if 'path_to_current_coil_register_json' in config_dict:
                new_register_json_path = config_dict['path_to_current_coil_register_json']
                new_register_folder_path = os.path.dirname(new_register_json_path)
                if not os.path.isdir(new_register_folder_path):
                    os.makedirs(new_register_folder_path)

                with open(get_current_config_json()['config']['path_to_current_coil_register_json']) as f:
                    register_json = json.load(f)
                with open(new_register_json_path, 'w') as g:
                    json.dump(register_json, g, indent=2)

                print(f'Register Recreated In Location {new_register_json_path}')

        recreate_register_if_changed()  # if config_dict implies a change in the register location > recreate

        with open(get_current_config_json()['config']['path_to_current_config_json'], 'w') as f:
            json.dump(updated_config, f, indent=2)



    # Backup
    previous_config_path = save_current_config_file_into_previous_configs_folder()

    # Update parameters: config_dict -> current_config_dict
    updated_config = update_config_values()
    # Save new config.json
    set_updated_config()



    print(json.dumps(get_current_config_json(), indent=2, sort_keys=True))


def revert_config():
    def get_existing_config_json(config_path):
        with open(config_path) as f:
            config_json = json.load(config_path)
        return config_json

    def load_default_config():
        # Uses variables in config_initializer.py because it must load the default files that comes with the project
        with open(path_to_default_config_json) as f:
            default_config_json = json.load(path_to_default_config_json)
        with open(path_to_current_config_json, 'w') as f:
            json.dumps(default_config_json, f, indent=2)
        print('Default config loaded')

    current_config_json = get_current_config_json()
    path_to_previous_config_file = current_config_json['config']['path_to_previous_config_file']
    if os.path.isfile(path_to_previous_config_file):
        previous_config_dict = get_existing_config_json(path_to_previous_config_file)['config']
        update_config(previous_config_dict)
    else:
        print('No previous config found.')
        ans = input('Want to load the default config file?(y/n)')
        while ans not in ['n', 'N', 'y', 'Y']:
            ans = input('Enter a valid answer: y/n')
        if ans in ['y', 'Y']:
            load_default_config()
        elif ans in ['n', 'N']:
            print(f'Build a config.json file, like the following model, place it in {path_to_default_config_json} and try again')
            print(json.dump(path_to_default_config_json, indent=2, sort_keys=True))

