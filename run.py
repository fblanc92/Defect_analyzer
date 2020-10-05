from resources.coil_utils import get_coils_in_folder, update_coil_register, get_unregistered_coils_in_path, \
    analyze_coil_list
from resources.configs.globals import app_config

import threading


def init_register():
    coils_in_folder = get_coils_in_folder(app_config['path_coils_folder'])
    update_coil_register(coils_in_folder)  # creates the coil register


def start_scan_timer(timer):
    """ Creates and starts the Timer Thread that calls the
        starting function
        args: delay_s -> Timer delay in seconds to start the function
    """
    timer.start()


def start_app():
    """ Contains the app flow """
    unregistered_coils_list = get_unregistered_coils_in_path(app_config['path_coils_folder'])
    if unregistered_coils_list:
        print(f'New unregistered folders {[coil.id for coil in unregistered_coils_list]}')
        analyze_coil_list(unregistered_coils_list)
    else:
        print('No new coils')

    app_timer = threading.Timer(app_config['scan_timer_delay'], start_app)
    start_scan_timer(app_timer)


if __name__ == '__main__':
    init_register()
    start_app()
