"""
    This file is aims to:
        - open images from img folder
        - list the options of objects linked to the image, and create 
          an association
"""
from typing import List
from os import listdir
from PIL import Image, UnidentifiedImageError
import shapely
import json

path_to_image: str = "../img"


def is_valid_image(image: str):
    try:
        return Img(f"{path_to_image}/{image}")
    except UnidentifiedImageError:
        return None


def open_files():
    imgs = map(is_valid_image, listdir(path_to_image))
    return [i for i in imgs if i != None]


class Img:
    def __init__(self, img_path: str) -> None:
        self.path = img_path
        self.img = Image.open(img_path)
        self.tag: dict = dict()
        self.tag_list: set = set()
        self.is_selected = False

    def set_tag_list(self, l):
        self.tag_list = l

    def add_tag(self, tag, x1, y1, x2, y2):
        self.tag_list.add(tag)
        if tag in self.tag:
            self.tag[tag].append(((x1, y1), (x2, y2)))
        else:
            self.tag[tag] = ((x1, y1), (x2, y2))

    def remove_tag(self, tag):
        self.tag.pop(tag)

    def update_tag(self, old_value, new_value):
        if old_value in self.tag:
            old_coord = self.tag.pop(old_value)
            self.tag[new_value] = old_coord

    def __str__(self) -> str:
        return json.dumps((self.path, self.tag))

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    print(open_files())
