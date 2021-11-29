
"""
    This file aims to create the guy for the ImageAnnotator
    It only contains the structure and :
        ask for images to image_reader library
"""

from os import execlpe
from tkinter import Scrollbar, ttk
from PIL import ImageTk, Image
import images as img
from typing import Collection, List
from tkinter.constants import HORIZONTAL
import tkinter as tk
import tags
import scrollableframe as sf


def get_selected_images(list_images: List[img.Img]):
    return [i for i in list_images if i.is_selected]


class ImageMakeRect():
    def __init__(self, root, image: img.Img) -> None:
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()
        print(image.img)
        self.img = ImageTk.PhotoImage(image.img)
        self.canvas.create_image(20, 20, anchor=tk.NW, image=img)


class right_panel:
    def __init__(self, root, father, list_image, left_panel) -> None:
        self.root = root
        self.father = father
        self.main_panel = tk.PanedWindow(father)
        self.list_img = list_image
        self.lp = left_panel

    def initialise(self):
        self.tc = self.theme_class(self)
        self.sb = self.select_option(self)

    class select_option:
        def __init__(self, rp) -> None:
            self.rp = rp
            self.main = tk.PanedWindow(rp.father)
            self.main.pack()
            self.lp = rp.lp
            self.create_buttons()

        def create_buttons(self):
            self.lab = tk.Label(self.main, text='Check/Uncheck box')
            self.button_pane = tk.PanedWindow(self.main)
            self.b1 = tk.Button(self.button_pane, text='CheckAll')
            self.b2 = tk.Button(self.button_pane, text='UncheckAll')
            self.b1.bind("<Button-1>", lambda e: self.listener(True))
            self.b2.bind("<Button-1>", lambda e: self.listener(False))
            self.b1.pack(side="left")
            self.b2.pack(side="right")
            self.lab.pack()
            self.button_pane.pack()

        def listener(self, select_all):
            for i in self.rp.list_img:
                i.select(select_all)
            self.lp.updateSelected(None)

    class theme_class:
        def __init__(self, rp) -> None:
            self.rp = rp
            self.create_theme_option_panel()

        def create_theme_option_panel(self):
            self.variable = tk.StringVar(self.rp.father)
            self.style = ttk.Style(self.rp.root)
            themes = self.style.theme_names()
            self.variable.set(themes[0])
            self.variable.trace("w", self.callback)
            opt = tk.OptionMenu(self.rp.father, self.variable, *themes)
            opt.pack(side='top')

        def callback(self, *args):
            self.style.theme_use(self.variable.get())


class left_panel:
    def __init__(self, father, images: List[img.Img]) -> None:
        self.father = father
        self.images = images
        self.notebook = ttk.Notebook(father)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.titles = ["All images", "Selected images", "Tags", "Help"]
        self.tabs = [tk.Frame(self.notebook) for i in range(len(self.titles))]

        self.under_frame1 = sf.create_scrollable_frame(self.tabs[0])
        self.under_frame2 = sf.create_scrollable_frame(self.tabs[1])

    def initialise(self):
        for f in self.tabs:
            f.pack()

        self.notebook.bind("<<NotebookTabChanged>>", self.updateSelected)

        pos = 0
        mod = 4
        for i in self.images:
            img = i.createMiniLabel(self.under_frame1)
            img.grid(row=pos // mod, column=pos %
                     mod, ipadx=5, ipady=5)
            pos += 1

        for f, i in zip(self.tabs, self.titles):
            self.notebook.add(f, text=i)

    def updateSelected(self, event):

        pos = 0
        mod = 4
        if self.notebook.index(self.notebook.select()) == 1:
            for widget in self.under_frame2.winfo_children():
                widget.destroy()
            for i in self.images:
                if i.is_selected:
                    img = i.createMiniLabel2(self.under_frame2)
                    img.grid(row=pos // mod, column=pos %
                             mod, ipadx=4, ipady=4)
                    pos += 1


class main_class:
    def __init__(self, list_tag, list_img: List[img.Img], root) -> None:
        self.list_tag = list_tag
        self.list_img = list_img
        self.root = root
        root.title('ImageAnnotator')
        self.initiate()

    def initiate(self):
        self.frame = tk.PanedWindow(self.root)
        self.left_panel = tk.PanedWindow(self.frame)
        self.right_panel = tk.PanedWindow(self.frame)
        self.left_panel.pack(side="left", fill=tk.BOTH, expand=1)
        self.right_panel.pack(side="right", fill=tk.Y)

        self.frame.pack(fill=tk.BOTH, expand=1)

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.lp = left_panel(self.left_panel, self.list_img)
        self.lp.initialise()

    def create_right_panel(self):
        self.rp = right_panel(self.root, self.right_panel,
                              self.list_img, self.lp)
        self.rp.initialise()


def main(list_tag, list_img: List[img.Img]):

    root = tk.Tk()

    # style = ttk.Style(root)
    # style.theme_use('winnative')
    # for i in style.theme_names():
    #     print(i)

    mc = main_class(list_tag, list_img, root)
    # mc.initiate()
    # root.title('ImageAnnotator')

    root.minsize(670, 400)
    root.mainloop()


if __name__ == '__main__':

    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs

    for i in img_list:
        i.set_tag_list(tag_list)
    main(tag_list, img_list)
