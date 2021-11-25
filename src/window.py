
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


def createLabel(im, frm):

    photo = ImageTk.PhotoImage(im.img)
    imgLabel = ttk.Label(frm.scrollable_frame, image=photo)
    imgLabel.image = photo
    imgLabel.pack()
    return imgLabel


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


def main(list_tag, list_img):
    """
    print(123)
    root_window = tk.Tk()
    notebook = ttk.Notebook(root_window)
    # notebook.add(ImageMakeRect(
    #     notebook, list_img[0]).canvas, text="All images")
    #notebook.add(grep(notebook), text="Selected images")
    # scrollbar = ImageScrollBar(list_img, root_window)
    im = ImageTk.PhotoImage(list_img[0].img)
    frame = tk.Frame(root_window)
    label = tk.Label(frame, image=im)
    label.image = im
    root_window.mainloop()
    """

    root = tk.Tk()
    root.title('ImageAnnotator')
    root.geometry('400x300')

    frm = ScrollableFrame(root)

    frm.grid(row=100, column=100)

    for i in range(len(list_img)):
        createLabel(list_img[i], frm)

    root.mainloop()


if __name__ == '__main__':

    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs

    for i in img_list:
        i.set_tag_list(tag_list)
    main(tag_list, img_list)
