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

    current_config_json = get_current_config_json()
    unregistered_coils_list = get_unregistered_coils_in_path(current_config_json['config']['path_coils_folder'])
    if unregistered_coils_list:
        print(f'New unregistered folders {[coil.id for coil in unregistered_coils_list]}')
        analyze_coil_list(unregistered_coils_list)
    else:
        print('No new coils')

    app_timer = threading.Timer(float(current_config_json['config']['scan_timer_delay']), start_app).start()



def start_backend():
    # if __name__ == '__main__':

    init_register()
    start_app()
