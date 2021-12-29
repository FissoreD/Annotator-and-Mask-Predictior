from tkinter.constants import NONE
from typing import List
import images
import tags
import json
import os
import shutil
from tkinter import filedialog

""" This file is all about reading and writing files """


def find_image(img_path, list_img):
    for i in list_img:
        if img_path == i.path:
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


def create_all_cropped_images(image_list):
    folder = "crop_img"
    if not os.path.exists(folder):
        os.mkdir(folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    for i in image_list:
        if i.is_selected:
            i.crop_image()


if __name__ == '__main__':
    tag_list = tags.Tag(images.open_files())
    img_list = tag_list.imgs
    for i in img_list:
        i.set_tag_list(tag_list)
