
"""
    This file aims to create the guy for the ImageAnnotator
    It only contains the structure and :
        ask for images to image_reader library
"""

from tkinter import Frame, ttk
import images as img
from typing import List
from tkinter.constants import HORIZONTAL
import tkinter as tk
import tags
import scrollableframe as sf
import help_panel
import read_write
import tag_panel
from ttkthemes import ThemedTk


def get_selected_images(list_images: List[img.Img]):
    return [i for i in list_images if i.is_selected]


class right_panel:
    def __init__(self, root, father, list_image, left_panel) -> None:
        self.root = root
        self.father = father
        self.list_img = list_image
        self.lp = left_panel

    def initialise(self):
        self.tc = self.theme_class(self)
        self.sb = self.select_option(self)
        self.save = ttk.Button(self.father, text='SaveToFile')
        self.save.bind('<Button>',
                       lambda x: read_write.write_file(self.list_img, 'test'))
        self.load = ttk.Button(self.father, text='LoadFile')
        self.load.bind('<Button>',
                       lambda x: read_write.read_file(self.list_img, 'test'))
        self.load.pack()
        self.save.pack()

    class select_option:
        def __init__(self, rp) -> None:
            self.rp = rp
            self.main = ttk.PanedWindow(rp.father)
            self.main.pack()
            self.lp = rp.lp
            self.create_buttons()

        def create_buttons(self):
            self.lab = ttk.Label(self.main, text='Check/Uncheck box')
            self.button_pane = ttk.PanedWindow(self.main)
            self.b1 = ttk.Button(self.button_pane, text='CheckAll')
            self.b2 = ttk.Button(self.button_pane, text='UncheckAll')
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
            opt = ttk.OptionMenu(self.rp.father, self.variable, *themes)
            opt.pack(side='top')

        def callback(self, *args):
            self.style.theme_use(self.variable.get())


class left_panel:
    def __init__(self, father, images: List[img.Img], tags) -> None:
        self.mod = 4
        self.father = father
        self.images = images
        self.notebook = ttk.Notebook(father)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.titles = ["All images", "Selected images", "Tags", "Help"]
        self.tabs = [ttk.Frame(self.notebook) for i in range(len(self.titles))]

        self.under_frame1 = sf.create_scrollable_frame(self.tabs[0])
        f1 = ttk.Frame(self.under_frame1)
        self.under_frame1.canvas.bind(
            '<Configure>', lambda e: f1.config(width=e.width))

        self.under_frame2 = sf.create_scrollable_frame(self.tabs[1])
        f2 = ttk.Frame(self.under_frame2)
        self.under_frame2.canvas.bind(
            '<Configure>', lambda e:  f2.config(width=e.width))
        f1.grid(columnspan=self.mod)
        f2.grid(columnspan=self.mod)
        self.f2 = f2
        tags.tag_panel = tag_panel.tag_panel(self.tabs[2], tags)
        help_panel.main(self.tabs[3])

    def initialise(self):
        for f in self.tabs:
            f.pack()
        self.notebook.bind("<<NotebookTabChanged>>", self.updateSelected)
        for pos, i in enumerate(self.images):
            self.create_img(i, self.under_frame1, pos)
        for f, i in zip(self.tabs, self.titles):
            self.notebook.add(f, text=i)
        self.notebook.select(self.notebook.tabs()[2])

    def updateSelected(self, _):
        if self.notebook.index(self.notebook.select()) == 1:
            for widget in self.under_frame2.winfo_children():
                None if widget == self.f2 else widget.grid_forget()
            img = [img for img in self.images if img.is_selected]
            for pos, i in enumerate(img):
                self.create_img(i, self.under_frame2, pos)

    def create_img(self, i,  frm: Frame, pos):
        img = i.createMiniLabel2(
            self.under_frame2) if frm == self.under_frame2 else i.createMiniLabel(self.under_frame1)
        img.grid(row=pos // self.mod, column=pos %
                 self.mod, ipadx=5, ipady=5, sticky='nswe')


class main_class:
    def __init__(self, list_tag, list_img: List[img.Img], root) -> None:
        self.list_tag = list_tag
        self.list_img = list_img
        self.root = root
        root.title('ImageAnnotator')
        self.initiate()

    def initiate(self):
        self.frame = ttk.PanedWindow(self.root)
        self.left_panel = ttk.PanedWindow(self.frame)
        self.right_panel = ttk.PanedWindow(self.frame)
        self.left_panel.pack(side="left", fill=tk.BOTH, expand=1)
        self.right_panel.pack(side="right", fill=tk.Y)

        self.frame.pack(fill=tk.BOTH, expand=1)

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.lp = left_panel(self.left_panel, self.list_img, self.list_tag)
        self.lp.initialise()

    def create_right_panel(self):
        self.rp = right_panel(self.root, self.right_panel,
                              self.list_img, self.lp)
        self.rp.initialise()


def main(list_tag, list_img: List[img.Img]):

    root = ThemedTk(theme='black')
    main_class(list_tag, list_img, root)

    root.minsize(750, 480)
    root.mainloop()


if __name__ == '__main__':

    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs

    for j in img_list:
        j.set_tag_list(tag_list)
    tag_list.add('Test')
    main(tag_list, img_list)
