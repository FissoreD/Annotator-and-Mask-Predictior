"""
    This file is aims to:
        - open images from img folder
        - list the options of objects linked to the image, and create 
          an association
"""
import re
from typing import List
from os import listdir
from PIL import Image, UnidentifiedImageError
import json
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import annotator
import shapely
import itertools
from shapely.geometry import box
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
        image = Image.open(img_path)
        width, height = image.size
        maxSize = 120
        XSIZE = maxSize if width > height else maxSize*width//height
        YSIZE = maxSize if height > width else maxSize*height//width
        self.img = image.resize((XSIZE, YSIZE), Image.ANTIALIAS)
        self.tag_of_points: dict = dict()
        self.tag_of_rect: dict = dict()
        self.tag_list: set = set()
        self.is_selected = False

    def set_tag_list(self, l):
        self.tag_list = l

    def add_tag(self, tag, x1, y1, x2, y2, rect_id):
        x1, x2, y1, y2 = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        coords = [[x1, y1], [x2, y2]]
        box_from_coord = box(x1, y1, x2, y2)
        if abs(x1-x2) <= 5 or abs(y1-y2) <= 5 or box_from_coord.area <= 40:
            # TODO : add popUp
            print('Trop petit')
            return False
        for (pos, (i, r)) in enumerate(list(itertools.chain(*self.tag_of_rect.values()))):
            if (box_from_coord.contains(i)):
                print(box_from_coord, 'contains', i)
                return 'contains', r
            elif (i.contains(box_from_coord)):
                print(box_from_coord, 'is contained in', i)
                return 'contained', r
            elif box_from_coord.intersects(i):
                a1 = box_from_coord.area
                a2 = i.area
                if box_from_coord.intersection(i).area/a1 >= 0.2:
                    print('New rect cover more then 40% an existing shape')
                    return 'overlap', r
                elif box_from_coord.intersection(i).area/a2 >= 0.2:
                    print('New rect is covered for more then 40% an existing shape')
                    return 'overlapped', r

        if tag in self.tag_of_points:
            self.tag_of_points[tag].append(coords)
            self.tag_of_rect[tag].append([box_from_coord, rect_id])
        else:
            self.tag_list.add(tag)
            self.tag_of_points[tag] = [coords]
            self.tag_of_rect[tag] = [[box_from_coord, rect_id]]
        return True

    def delete_from_id(self, id):
        for tag in self.tag_of_rect:
            for pos, elt in enumerate(self.tag_of_rect[tag]):
                if elt[1] == id:
                    self.tag_of_points[tag].pop(pos)
                    self.tag_of_rect[tag].pop(pos)
                    if len(self.tag_of_points[tag]) == 0:
                        self.tag_of_points.pop(tag)
                        self.tag_of_rect.pop(tag)
                    return

    def remove_tag(self, tag):
        self.tag_of_points.pop(tag, None)
        self.tag_of_rect.pop(tag, None)

    def update_tag(self, old_value, new_value):
        if old_value in self.tag:
            old_coord = self.tag.pop(old_value)
            self.tag[new_value] = old_coord

    def __str__(self) -> str:
        return json.dumps((self.path, self.tag_of_points))

    def __repr__(self):
        return self.__str__()

    def createMiniLabel(self, frm):
        photo = ImageTk.PhotoImage(self.img)
        imgLabel = tk.Label(frm, image=photo)
        imgLabel.image = photo
        self.imgLabel: tk.Label = imgLabel
        imgLabel.bind("<Button>", self.mouseClick)
        return imgLabel

    def createMiniLabel2(self, frm):
        photo = ImageTk.PhotoImage(self.img)
        imgLabel = tk.Label(frm, image=photo)
        imgLabel.image = photo
        self.imgLabel2: tk.Label = imgLabel
        imgLabel.bind(
            "<Button-1>", lambda e: annotator.main(frm, self))
        return imgLabel

    def select(self, b):
        if self.is_selected != b:
            self.mouseClick(None)

    def mouseClick(self, event):
        if self.is_selected:
            self.imgLabel.config(relief="flat",
                                 bg="SystemButtonFace", fg="SystemButtonFace")
            self.is_selected = not self.is_selected
        else:
            self.imgLabel.config(relief="sunken",
                                 bg="gray51", fg="white")
            self.is_selected = not self.is_selected


if __name__ == '__main__':
    print(open_files())
