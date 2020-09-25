# project methods
import os
import datetime
import json
from resources.configs.configs import input_images_formats
from collections import defaultdict
from resources.models.coil import Coil


def get_images_in_path(path):
    """return the images in the path. Possible extensions are specified in input_images_formats lists"""
    return [file for file in os.listdir(path) if any(file.endswith(ext) for ext in input_images_formats)]


def get_coils_in_folder(path):
    """Scans folders in the passed path, and check if are compatible with web inspector saving format
        args: path to scan
        return: defaultdict with folders that are in web inspector format"""
    coils_dict = defaultdict(list)

    def check_web_inspector_format():
        if os.path.isdir(item_path):  # is a dir
            if len(os.path.basename(item_path).split('-')) == 3:  # is in WI format
                return True
        else:
            return False

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

    for item in os.listdir(path):  # item example: 111111A-1_ 1_2001-13_ 2_20
        item_path = os.path.join(path, item)
        if check_web_inspector_format():
            coil = create_coil_from_coil_path(item_path)
            coils_dict['coils'].append({"id": coil.id,
                                        "date": coil.date,
                                        "time": coil.time,
                                        "path": coil.path,
                                        "image_files": coil.image_list})

    return coils_dict


coils_ = get_coils_in_folder(r'C:/test')
