from resources.coil_utils import get_coils_in_folder, create_coil_register, get_unregistered_coils_in_path, \
    analyze_coil_list
from resources.configs.configs import path_coils_folder


def init_register():
    coils_in_folder = get_coils_in_folder(path_coils_folder)
    create_coil_register(coils_in_folder)
    return True


def start_app():
    """ Contains the app flow """
    unregistered_coils_list = get_unregistered_coils_in_path(path_coils_folder)
    if unregistered_coils_list:
        analyze_coil_list(unregistered_coils_list)
    else:
        print('No new coils')


if __name__ == '__main__':
    init_register()
    start_app()
