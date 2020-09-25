from resources.project_utils import get_coils_in_folder
from resources.configs.configs import path_coils_folder, path_initial_coils_json
import json


def init_app():
    def create_initial_json():
        with open(path_initial_coils_json, 'w') as f:
            json.dump(coils_dict, f, indent=2)

    coils_dict = get_coils_in_folder(path_coils_folder)
    create_initial_json()


if __name__ == '__main__':
    init_app()
