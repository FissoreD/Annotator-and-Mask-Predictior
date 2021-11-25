
"""
    This file aims to create the guy for the ImageAnnotator
    It only contains the structure and :
        ask for images to image_reader library
"""

import tkinter as tk
from typing import List
import images as img
from PIL import ImageTk, Image
from tkinter import ttk


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

        self.scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)

        self.canvas = tk.Canvas(
            self.scrollbar, bd=0, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.scrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        for img in list_img:
            img.img.show()
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img.img)


def main(list_tag, list_img):
    print(123)
    root_window = tk.Tk()
    notebook = ttk.Notebook(root_window)
    # notebook.add(ImageMakeRect(
    #     notebook, list_img[0]).canvas, text="All images")
    #notebook.add(grep(notebook), text="Selected images")
    scrollbar = ImageScrollBar(list_img, root_window)
    root_window.mainloop()
