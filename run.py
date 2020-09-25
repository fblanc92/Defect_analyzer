from resources.project_utils import get_coils_in_folder
import os
def init_app():
    coils_dict = get_coils_in_folder(r'c:/test')
    print(os.getcwd())


if __name__ == '__main__':
    init_app()