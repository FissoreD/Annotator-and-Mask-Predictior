
"""
    This file aims to create the guy for the ImageAnnotator
    It only contains the structure and :
        ask for images to image_reader library
"""

from tkinter import Scrollbar, ttk
from PIL import ImageTk, Image
import images as img
from typing import Collection, List
from tkinter.constants import HORIZONTAL
import tkinter as tk
import tags
from scrollableframe import ScrollableFrame


def get_selected_images(list_images: List[img.Img]):
    return [i for i in list_images if i.is_selected]


class ImageMakeRect():
    def __init__(self, root, image: img.Img) -> None:
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()
        print(image.img)
        self.img = ImageTk.PhotoImage(image.img)
        self.canvas.create_image(20, 20, anchor=tk.NW, image=img)


class ImageScrollBar:
    import tkinter as tk

    def __init__(self, list_img, window):
        self.frm = tk.Frame(window)
        self.canvas = tk.Label(
            self.frm, image=ImageTk.PhotoImage(list_img[0].img))
        self.canvas.pack()


def main(list_tag, list_img: List[img.Img]):

    root = tk.Tk()
    # style = ttk.Style(root)
    # style.theme_use('winnative')
    # for i in style.theme_names():
    #     print(i)
    root.title('ImageAnnotator')

    frm = ScrollableFrame(root)

    pos = 0
    mod = 4
    for i in list_img:
        img = i.createMiniLabel(frm)
        img.grid(row=pos // mod, column=pos %
                 mod, ipadx=4, ipady=4)
        pos += 1

    frm.pack()
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':

    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs

    for i in img_list:
        i.set_tag_list(tag_list)
    main(tag_list, img_list)
