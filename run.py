import threading
from Defect_analyzer_back.resources.config.config_initializer import load_initial_config
import time
from Defect_analyzer_back.resources.config import configs_utils

load_initial_config()

from Defect_analyzer_back.resources.coil_utils import get_coils_in_folder, update_coil_register, \
    get_unregistered_coils_in_path, analyze_coil_list

from Defect_analyzer_back.resources.config.configs_utils import get_current_config_json


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


def start_backend():
    # if __name__ == '__main__':

    init_register()
    start_app()
    time.sleep(5)
    update_dict = {"path_to_current_coil_register_folder": "C:/code/Defect_analyzer_back/project_data/register/TEST", "path_to_current_coil_register_json": "C:/code/Defect_analyzer_back/project_data/register/TEST/coil_register.json"}
    from Defect_analyzer_back.resources.config.configs_utils import update_config
    update_config(update_dict)
    from Defect_analyzer_back.resources.config.configs_utils import get_all_the_configs_list
    get_all_the_configs_list()


start_backend()