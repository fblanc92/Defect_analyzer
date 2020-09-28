from resources.project_utils import get_coils_in_folder, create_coil_register, get_unregistered_coils_in_path
from resources.configs.configs import path_coils_folder


def init_app():
    coils_in_folder = get_coils_in_folder(path_coils_folder)
    create_coil_register(coils_in_folder)

    return True


def start_app():
    """ Contains the app flow """
    unregistered_coils_dict = get_unregistered_coils_in_path(path_coils_folder)
    if unregistered_coils_dict:
        for coil in unregistered_coils_dict['coils']:
            print(f'New coil: {coil.id}')
    else:
        print('No new coils')


if __name__ == '__main__':
    init_app()
    start_app()
