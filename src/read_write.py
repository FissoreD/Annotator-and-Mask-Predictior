from tkinter.constants import NONE
from typing import List
import images
import tags
import os
import json
import shutil
from tkinter import filedialog
from global_vars import *

""" This file is all about reading and writing files """


def find_image(img_path, list_img):
    for i in list_img:
        if os.path.abspath(img_path) == os.path.abspath(i.path):
            return i


def read_file(list_img, file_path=None):
    """
        Opening of json file which store all the annotations.
        We browse them all and we assign them respectively to each of the images
    """
    if file_path == None:
        file = filedialog.askopenfile(filetypes=[('JSON', '.json')])
    else:
        file = open(file_path)
    if file == None:
        return
    try:
        D = json.load(file)
    except UnicodeDecodeError:
        return
    for elt in D:
        img = find_image(elt[0], list_img)
        if img == None:
            continue
        for tag_name in elt[1]:
            for coor in elt[1][tag_name]:
                img.add_tag(tag_name, *coor, None)
                img.is_selected = True
    file.close()


def write_file(list_img):
    """ We browse all annotations and store them in a json file """
    file = filedialog.asksaveasfile(
        defaultextension='.json', filetypes=[('JSON', '.json')],
        initialfile='output.json')
    if file == None:
        return
    L = []
    for elt in list_img:
        L.append([elt.path, elt.tag_of_points])
    json.dump(L, file)
    file.close()


def clear_floder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def create_all_cropped_images(image_list):
    if not os.path.exists(crop_dir):
        os.mkdir(crop_dir)
    clear_floder(crop_dir)
    for i in image_list:
        i.crop_image()


if __name__ == '__main__':
    tag_list = tags.Tag(images.open_files())
    img_list = tag_list.imgs
    for i in img_list:
        i.set_tag_list(tag_list)
