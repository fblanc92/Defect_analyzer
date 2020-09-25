from resources.project_utils import get_coils_in_folder
from resources.configs.configs import path_coils_folder, path_initial_coils_json
import json


def init_app():
    """ Create a JSON file containing the coils that are in the folder before the analysis starts.
     Those coils are not supposed to be analyzed """

    def create_initial_json():
        with open(path_initial_coils_json, 'w') as f:
            json.dump(coils_dict, f, indent=2)

    coils_dict = get_coils_in_folder(path_coils_folder)
    create_initial_json()

    return True

def start_app():
    """ Contains the app flow """
    pass


if __name__ == '__main__':
    init_app()
    start_app()