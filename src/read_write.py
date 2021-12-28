from tkinter.constants import NONE
from typing import List
import images as img
import tags
import json
import os
import shutil
from tkinter import filedialog

""" This file is all about reading and writing files """


def find_image(img_path, list_img: List[img.Img]):
    for i in list_img:
        if img_path == i.path:
            return i


def read_file(list_img: List[img.Img]):
    """
        Opening of json file which store all the annotations.
        We browse them all and we assign them respectively to each of the images
    """
    file = filedialog.askopenfile(filetypes=[('JSON', '.json')])
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
    file.close()


def write_file(list_img: List[img.Img]):
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


def create_all_cropped_images(image_list: List[img.Img]):
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
    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs
    for i in img_list:
        i.set_tag_list(tag_list)
    # img_list[0].add_tag('tipo', 4, 5, 999, 888)
    # img_list[0].add_tag('tipo', 0, 2, 444, 555)
    # img_list[0].add_tag('tipo', 1000, 1000, 2000, 2000)
    # img_list[0].add_tag('t1', 0, 2, 333, 222)
    # img_list[1].add_tag('ffff', 0, 99, 111, 666)
    # write_file(img_list, "file_name")
    # tag_list.remove('tipo')
    # tag_list.remove('ffff')
    # tag_list.remove('t1')
    # read_file('file_name', img_list)
