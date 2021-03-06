"""
    This file is aims to:
        - open images from img folder
        - list the options of objects linked to the image, and create
          an association
"""
import os
import json
from PIL import ImageTk, Image, UnidentifiedImageError
import tkinter as tk
import annotator
import itertools
from shapely.geometry import box
import nnl_process
from global_vars import *


def is_valid_image(image: str):
    """ Check if the path exists or not """
    try:
        return Img(f"{path_to_image}/{image}")
    except (UnidentifiedImageError, PermissionError):
        return None


def create_image(parent, img):
    photo = ImageTk.PhotoImage(img)
    imgLabel = tk.Label(parent, image=photo, anchor=tk.CENTER)
    imgLabel.image = photo
    return imgLabel


def open_files():
    """ Return a list of images (according to the path name given in listdir argument) """
    imgs = map(is_valid_image, os.listdir(path_to_image))
    return [i for i in imgs if i != None]


class Img:
    """
        This class represent an image
        An image :
            - can be selected for annotating or not
            - contains a set of annotations and the set of tag names
            - is automatically resized for standatization

        It contains in majority utility methods

    """

    def __init__(self, img_path: str) -> None:
        self.path = img_path
        """ The image of labels in selected images panel """
        image = Image.open(img_path)
        width, height = image.size
        maxSize = 150
        XSIZE = maxSize if width > height else maxSize*width//height
        YSIZE = maxSize if height > width else maxSize*height//width
        self.img = image.resize((XSIZE, YSIZE), Image.ANTIALIAS)

        """ The image of annotator """
        big_image: Image = Image.open(img_path)
        maxSize = 600
        XSIZE = maxSize if big_image.width > big_image.height else maxSize * \
            big_image.width//big_image.height
        YSIZE = maxSize if big_image.height > big_image.width else maxSize * \
            big_image.height//big_image.width
        self.big_image = big_image.resize((XSIZE, YSIZE), Image.ANTIALIAS)

        self.tag_and_points: dict = dict()
        self.tag_and_rect: dict = dict()
        self.tag_list: set = set()
        self.is_selected = False

    def set_tag_list(self, l):
        self.tag_list = l

    def add_tag(self, tag, x1, y1, x2, y2, rect_id):
        """
            Before adding the tag in the list, we make sure that it is valid by checking its size
            or if it is in conflict with another one (via several 'shapely' pre-built utility methods)
        """
        x1, x2, y1, y2 = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        coords = [x1, y1, x2, y2]
        box_from_coord = box(x1, y1, x2, y2)
        if abs(x1-x2) <= 5 or abs(y1-y2) <= 5 or box_from_coord.area <= 40:
            return False
        for (i, r) in list(itertools.chain(*self.tag_and_rect.values())):
            if (box_from_coord.contains(i)):
                return 'contains', r
            elif (i.contains(box_from_coord)):
                return 'contained', r
            elif box_from_coord.intersects(i):
                a1 = box_from_coord.area
                a2 = i.area
                if box_from_coord.intersection(i).area/a1 >= 0.2:
                    return 'overlap', r
                elif box_from_coord.intersection(i).area/a2 >= 0.2:
                    return 'overlapped', r
        if tag in self.tag_and_points:
            self.tag_and_points[tag].append(coords)
            self.tag_and_rect[tag].append([box_from_coord, rect_id])
        else:
            self.tag_list.add(tag)
            self.tag_and_points[tag] = [coords]
            self.tag_and_rect[tag] = [[box_from_coord, rect_id]]
        self.inEvidence()
        return True

    def remove_if_empty(self, tag):
        if len(self.tag_and_points[tag]) == 0:
            self.tag_and_points.pop(tag)
            self.tag_and_rect.pop(tag)
            self.inEvidence()

    def delete_from_id(self, id):
        for tag in self.tag_and_rect:
            for pos, elt in enumerate(self.tag_and_rect[tag]):
                if elt[1] == id:
                    self.tag_and_points[tag].pop(pos)
                    self.tag_and_rect[tag].pop(pos)
                    self.remove_if_empty(tag)
                    return

    def remove_tag(self, tag):
        self.tag_and_points.pop(tag, None)
        self.tag_and_rect.pop(tag, None)
        self.inEvidence()

    def find_tag_by_rect_id(self, rect_id):
        for key, value in self.tag_and_rect.items():
            for pos, x in enumerate(value):
                if rect_id == x[1]:
                    return key, pos

    def rename_tag_of_rect(self, rect_id, new_tag_name):
        old_tag, pos = self.find_tag_by_rect_id(rect_id)
        self.tag_and_rect[old_tag].pop(pos)
        coords = self.tag_and_points[old_tag].pop(pos)
        self.remove_if_empty(old_tag)
        self.add_tag(new_tag_name, *coords, rect_id)

    def update_tag(self, old_value, new_value):
        if old_value in self.tag_and_points:
            old_coord1 = self.tag_and_points.pop(old_value)
            old_coord2 = self.tag_and_rect.pop(old_value)
            if new_value in self.tag_and_rect:
                self.tag_and_points[new_value].extend(old_coord1)
                self.tag_and_rect[new_value].extend(old_coord2)
            else:
                self.tag_and_points[new_value] = old_coord1
                self.tag_and_rect[new_value] = old_coord2

    def __str__(self) -> str:
        return json.dumps((self.path, self.tag_and_points))

    def __repr__(self):
        return self.__str__()

    def createMiniLabel2(self, frm):
        """ In 'Selected images' tab, if we rigth-click on an image, the annotator class's window appears """
        imgLabel = create_image(frm, self.img)
        self.imgLabel = imgLabel
        imgLabel.bind("<Button-1>", lambda _: annotator.main(frm, self))
        imgLabel.config(relief="sunken")
        return imgLabel

    def crop_image(self, list_of_cropped=None, path=None):
        """ For every tag of the image we create a sub-image and save it in 'crop_img' folder """
        not_on_the_fly = path == None
        path = path if path != None else crop_dir
        if not_on_the_fly and not os.path.exists(path):
            os.mkdir(path)
        for tag, coordsList in self.tag_and_points.items():
            folder_path = f"{path}/{tag}" if not_on_the_fly else path
            if not os.path.exists(folder_path) and not_on_the_fly:
                os.mkdir(folder_path)
            for coords in coordsList:
                x1, y1, x2, y2 = coords
                cropped: Image = self.big_image.crop(coords)
                height = y2 - y1
                width = x2 - x1
                ratio = min(180 / height, 180 / width)
                file_name = f"{folder_path}/{self.path.split('/')[-1].split('.')[0]}-bb-{x1}x{y1}-{width}-{height}.jpg"
                cropped = cropped.resize(
                    (int(width*ratio), int(height*ratio)), Image.ANTIALIAS)
                cropped.convert('RGB').save(file_name, 'JPEG')
                if list_of_cropped != None:
                    list_of_cropped.append((cropped, tag))
                if not_on_the_fly:
                    nnl_process.remove_not_valid_images(file_name)

    def inEvidence(self):
        opts = [
            {"bg": "SystemButtonFace", "fg": "SystemButtonFace"},
            {"bg": "gray51", "fg": "white"}
        ]
        is_selected = len(self.tag_and_points) > 0
        try:
            self.imgLabel.config(opts[is_selected])
        except AttributeError:
            pass


if __name__ == '__main__':
    print(open_files())
