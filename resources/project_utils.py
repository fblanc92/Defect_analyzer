# project methods
import os
import datetime
import json
from resources.configs.configs import input_images_formats, default_coils_filepath
from collections import defaultdict


def read_json(json_path):
    json_path = r'defaults/coils.json'
    with open(json_path) as f:
        coil_data = json.load(f)
        print(type(coil_data))
        print(json.dumps(coil_data, indent=2))
        for coil in coil_data['coils']:
            print(coil['id'])
        coil_data

    return


def get_coils_in_folder(path):
    """Scans folders in the passed path, and check if are compatible with web inspector saving format
        args: path to scan
        return: folders that are in web inspector format"""
    coils_dict = defaultdict(list)

    def check_web_inspector_format():
        if os.path.isdir(item_path):  # is a dir
            if len(os.path.basename(item_path).split('-')) == 3:  # is in WI format
                return True
        else:
            return False

    def extract_data_from_folder_name():
        item_data = item.split('-')  # item_data example: [111111A, 1_ 1_2001, 13_ 2_20]
        coil_id = item_data[0]

        dd = int(item_data[1].split('_')[0])
        mm = int(item_data[1].split('_')[1])
        yyyy = int(item_data[1].split('_')[2])
        coil_date = datetime.date(yyyy, mm, dd).strftime('%d/%m/%Y')

        hh = int(item_data[2].split('_')[0])
        mm = int(item_data[2].split('_')[1])
        ss = int(item_data[2].split('_')[2])
        coil_time = datetime.time(hh, mm, ss)

        return coil_id, coil_date, coil_time

    def get_images_in_path():
        """return the images in the path. Possible extensions are specified in input_images_formats lists"""
        return [file for file in os.listdir(item_path) if any(file.endswith(ext) for ext in input_images_formats)]

    for item in os.listdir(path):  # item example: 111111A-1_ 1_2001-13_ 2_20
        item_path = os.path.join(path, item)
        if check_web_inspector_format():
            id_coil, date, time = extract_data_from_folder_name()
            coils_dict['coils'].append({"id": id_coil,
                                        "date": str(date),
                                        "time": str(time),
                                        "path": item_path,
                                        "image_files": get_images_in_path()})

    return coils_dict


coils_ = get_coils_in_folder(r'C:/test')

