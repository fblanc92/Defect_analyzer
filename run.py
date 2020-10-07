import threading
from resources.config.config_initializer import load_initial_config
import time
from resources.config import configs_utils
load_initial_config()

from resources.coil_utils import get_coils_in_folder, update_coil_register, \
    get_unregistered_coils_in_path, analyze_coil_list
from resources.config.configs_utils import get_current_config_json


def init_register():
    current_config_json = get_current_config_json()
    coils_in_folder = get_coils_in_folder(current_config_json['config']['path_coils_folder'])
    update_coil_register(coils_in_folder)


def start_app():
    """ Contains the app flow """

    def start_scan_timer(timer):
        """ Creates and starts the Timer Thread that calls the
            starting function
            args: delay_s -> Timer delay in seconds to start the function
        """
        timer.start()

    current_config_json = get_current_config_json()
    unregistered_coils_list = get_unregistered_coils_in_path(current_config_json['config']['path_coils_folder'])
    if unregistered_coils_list:
        print(f'New unregistered folders {[coil.id for coil in unregistered_coils_list]}')
        analyze_coil_list(unregistered_coils_list)
    else:
        print('No new coils')

    app_timer = threading.Timer(current_config_json['config']['scan_timer_delay'], start_app)
    start_scan_timer(app_timer)


if __name__ == '__main__':
    init_register()
    start_app()
    time.sleep(12)
    update_dict = {"path_to_current_coil_register_folder": "project_data/register/TEST",
                   "path_to_current_coil_register_json": "project_data/register/TEST/coil_register.json"}
    configs_utils.update_config(update_dict)
