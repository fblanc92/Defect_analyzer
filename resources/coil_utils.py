# project methods
import datetime
import os
from collections import defaultdict
import json

from resources.configs.configs import input_images_formats, path_coils_folder, path_coil_register
from resources.models.coil import Coil


def get_unregistered_coils_in_path(path=path_coils_folder):
    """ retruns a dict containing the coils in the passed path, that are not in the register

        returns None if there are no unregistered coils"""
    coils_in_register_list = get_coils_in_register(path_coil_register)
    coils_in_path_list = get_coils_in_folder(path_coils_folder)
    unregistered_coils_list = [pathcoil for pathcoil in coils_in_path_list if
                               all(pathcoil.id != registercoil.id for registercoil in coils_in_register_list)]

    return unregistered_coils_list if len(unregistered_coils_list) else None


def json_to_coil_list(json_dict):
    """ Converts a dict (json) to a list of Coil objects
        arg: dict
        return: list of Coil objects"""
    return [Coil(coil['id'], coil['date'], coil['time'], coil['path'], coil['image_list']) for coil in
            json_dict['coils']]


def get_coils_in_register(register_path=path_coil_register):
    """ Reads the register and returns a list with the coils in it
        args: register path (default register is set)
        return: coil object list """
    with open(path_coil_register) as f:
        register = json.load(f)
    coils_in_register = json_to_coil_list(register)

    return coils_in_register if len(coils_in_register) else None  # list of Coil-type elements


def coil_list_to_json(coil_list):
    """ Takes a list of Coil objects and returns a defaultdict with the information
        args: coil object list
        return: defaultdict (json) with coil list info """
    coil_dict = defaultdict(list)
    for coil in coil_list:
        coil_dict['coils'].append({'id': coil.id, 'date': coil.date, 'time': coil.time, 'path': coil.path,
                                   'image_list': coil.image_list})
    return coil_dict


def create_coil_register(coil_list):
    """ Create a JSON file containing the coils that are in the folder before the analysis starts.
        Those coils are not supposed to be analyzed
        args: Coil object list
        return: True if succeed in creating register"""

    with open(path_coil_register, 'w') as f:
        json.dump(coil_list_to_json(coil_list), f, indent=2)
        return True


def get_images_in_path(path):
    """ return the images in the path. Possible extensions are specified in input_images_formats lists"""
    images_in_path = [file for file in os.listdir(path) if any(file.endswith(ext) for ext in input_images_formats)]
    return images_in_path if len(images_in_path) else None


def create_coil_from_coil_path(coil_path):
    """ Create a Coil object from the coil path.
        args: coil_path
        return: coil object"""
    coil_data = os.path.basename(coil_path).split('-')  # coil_data example: [111111A, 1_ 1_2001, 13_ 2_20]
    coil_id = coil_data[0]

    dd = int(coil_data[1].split('_')[0])
    mm = int(coil_data[1].split('_')[1])
    yyyy = int(coil_data[1].split('_')[2])
    coil_date = datetime.date(yyyy, mm, dd).strftime('%d/%m/%Y')

    hh = int(coil_data[2].split('_')[0])
    mm = int(coil_data[2].split('_')[1])
    ss = int(coil_data[2].split('_')[2])
    coil_time = datetime.time(hh, mm, ss).strftime('%H:%M:%S')

    coil_images = get_images_in_path(coil_path)

    coil = Coil(coil_id, coil_date, coil_time, coil_path, coil_images)

    return coil


def get_coils_in_folder(path):
    """Scans folders in the passed path, and check if are compatible with web inspector saving format

        args: path with coil folders
        return: list of Coil objects, or None"""

    coil_list = []

    def check_web_inspector_format():
        """ check if the paths corresponds to a web inspector format folder"""
        if os.path.isdir(item_path):  # is a dir
            if len(os.path.basename(item_path).split('-')) == 3:
                return True
        else:
            return False

    for item in os.listdir(path):  # item example: 111111A-1_ 1_2001-13_ 2_20
        item_path = os.path.join(path, item)
        if check_web_inspector_format():
            coil_list.append(create_coil_from_coil_path(item_path))

    return coil_list if len(coil_list) else None
