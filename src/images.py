"""
    This file is aims to:
        - open images from img folder
        - list the options of objects linked to the image, and create 
          an association
"""
from typing import List
from os import listdir
from PIL import Image, UnidentifiedImageError
import json
from PIL import ImageTk, Image
import tkinter as tk
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
        XSIZE = 100
        YSIZE = XSIZE
        self.img = Image.open(img_path).resize((XSIZE, YSIZE), Image.ANTIALIAS)
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
        if tag in self.tag:
            self.tag.pop(tag)

    def update_tag(self, old_value, new_value):
        if old_value in self.tag:
            old_coord = self.tag.pop(old_value)
            self.tag[new_value] = old_coord

    def __str__(self) -> str:
        return json.dumps((self.path, self.tag))

    def __repr__(self):
        return self.__str__()

    def createMiniLabel(self, frm):
        photo = ImageTk.PhotoImage(self.img)
        imgLabel = tk.Label(frm, image=photo, anchor=tk.CENTER)
        imgLabel.image = photo
        self.imgLabel: tk.Label = imgLabel
        self.imgLabelConfigs = [imgLabel.config()]
        imgLabel.bind("<Enter>", self.mouseEnter)
        imgLabel.bind("<Leave>", self.mouseLeave)
        imgLabel.bind("<Button>", self.mouseClick)
        return imgLabel

    def createMiniLabel2(self, frm):
        photo = ImageTk.PhotoImage(self.img)
        imgLabel = tk.Label(frm, image=photo, anchor=tk.CENTER)
        imgLabel.image2 = photo
        self.imgLabel2: tk.Label = imgLabel
        self.imgLabelConfigs2 = [imgLabel.config()]
        imgLabel.bind("<Enter>", self.mouseEnter)
        imgLabel.bind("<Leave>", self.mouseLeave)
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
        print(self.path, "Mouse click")

    def mouseEnter(self, event):
        print(self.path, "Mouse entered")

    def mouseLeave(self, event):
        print(self.path, "Mouse left")


if __name__ == '__main__':
    print(open_files())
