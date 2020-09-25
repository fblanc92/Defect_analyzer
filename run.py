from resources.project_utils import get_coils_in_folder
import os
def init_analyzer():
    coils_dict = get_coils_in_folder(r'c:/test')
    print(os.getcwd())


if __name__ == '__main__':
    init_analyzer()