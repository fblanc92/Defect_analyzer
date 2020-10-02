from resources.coil_utils import get_coils_in_folder, update_coil_register, get_unregistered_coils_in_path, \
    analyze_coil_list
from resources.configs.configs import path_coils_folder, scan_timer_delay
import threading


def init_register():
    coils_in_folder = get_coils_in_folder(path_coils_folder)
    update_coil_register(coils_in_folder)
    return True


def create_and_start_scan_timer(delay_s):
    """ Creates and starts the Timer Thread that calls the
        starting function
        args: delay_s -> Timer delay in seconds to start the function
    """
    app_timer = threading.Timer(delay_s, start_app)
    app_timer.start()


def start_app():
    """ Contains the app flow """
    unregistered_coils_list = get_unregistered_coils_in_path(path_coils_folder)
    if unregistered_coils_list:
        print(f'New unregistered folders {[coil.id for coil in unregistered_coils_list]}')
        analyze_coil_list(unregistered_coils_list)
    else:
        print('No new coils')

    create_and_start_scan_timer(scan_timer_delay)


if __name__ == '__main__':
    init_register()
    start_app()
