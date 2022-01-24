
"""
    This file aims to create the GUI for the ImageAnnotator
    It only contains the structure and :
        ask for images to image_reader library
"""

from tkinter import Frame, ttk, filedialog
from annotator import annotator
import cropped_panel
import images as img
from typing import List
from tkinter.constants import BOTH, CENTER
import tkinter as tk
import tags
import scrollableframe as sf
import help_panel
import read_write
import tag_panel
from global_vars import *

param = {'expand': 1, "fill": BOTH}


def annotate_on_the_fly(parent):
    def save():
        path = filedialog.askdirectory()
        if path == '':
            return
        image.crop_image(path=path)
    path = filedialog.askopenfilename(
        filetypes=[('Images', img_ext)])
    if path == '':
        return
    image = img.Img(path)
    image.set_tag_list(tags.Tag([image]))
    w = annotator(parent, image)
    m = tk.Menu(w)
    m.add_cascade(label="Save your annotations", command=save)
    w.config(menu=m)


def get_selected_images(list_images: List[img.Img]):
    return [i for i in list_images if i.is_selected]


def create_frame(mod, parent):
    f1 = ttk.Frame(parent)
    parent.canvas.bind('<Configure>', lambda e: f1.config(width=e.width))
    f1.grid(columnspan=mod)


class right_panel:
    """
    This class is a panel wich will always display.
    It's in this panel where we can set the theme, check or uncheck all images or open the images' folder 

    """

    def __init__(self, root, father, img_list, tag_list, left_panel) -> None:
        self.root = root
        self.father = father
        self.img_list = img_list
        self.tag_list = tag_list
        self.lp = left_panel

    def initialise(self):
        """
            Creation of Save/Load File button
            'Save as JSON' (resp. 'Load JSON') command is a reference of write_file (resp. read_file) method (cf read_write.py)
        """
        self.tc = self.theme_class(self)
        self.select_option(self)
        f1 = [read_write.write_file,
              read_write.read_file]
        ttk.Button(
            self.father, text='Annotate On-The-Fly',
            command=lambda: annotate_on_the_fly(self.father)).pack(param)
        ttk.Button(
            self.father, text='Save as JSON',
            command=lambda: f1[0](self.img_list)).pack(param)
        ttk.Button(
            self.father, text='Load JSON',
            command=lambda: f1[1](self.img_list)).pack(param)

    class select_option:
        def __init__(self, rp) -> None:
            self.main = ttk.PanedWindow(rp.father)
            self.rp = rp
            self.lp = rp.lp
            self.create_buttons()
            self.main.pack(param)

        def charge_img_folder(self, _):
            new_path = filedialog.askdirectory()
            if new_path == '':
                return
            img.path_to_image = new_path
            tag_list = self.rp.tag_list
            tag_list.imgs = img.open_files()
            while self.rp.list_img:
                self.rp.list_img.pop()
            self.rp.list_img.extend(tag_list.imgs)
            for j in self.rp.list_img:
                j.set_tag_list(tag_list)
            self.rp.lp.updateSelected(None)

        def create_buttons(self):
            """ Creation of practical button like the possibility of check/uncheck all images or change the folder of images """
            bp = ttk.PanedWindow(self.main)
            self.b3 = ttk.Button(bp, text='Open Images From Folder',
                                 command=lambda: self.charge_img_folder(None))
            self.b3.grid(column=0, row=0, sticky='nsew')
            bp.pack()

        def listener(self, select_all):
            """ Browse all images and set it to True/False (according to 'select_all' boolean) """
            for i in self.rp.list_img:
                i.select(select_all)
            self.lp.updateSelected(None)

    class theme_class:
        """ This class manages theme settings """

        def __init__(self, rp) -> None:
            self.rp = rp
            self.create_theme_option_panel()

        def create_theme_option_panel(self):
            """
                Creation of the scrolling menu in which several pre-built themes are proposed
                Default theme : ALT
            """
            self.variable = tk.StringVar(self.rp.father)
            self.style = ttk.Style(self.rp.root)
            themes = [i.upper() for i in self.style.theme_names()]
            self.variable.set(themes[0])
            self.variable.trace("w", self.callback)
            ttk.Label(self.rp.father, text="Set theme:",
                      anchor=CENTER).pack(fill=BOTH)
            opt = ttk.OptionMenu(
                self.rp.father, self.variable, themes[0], *themes)
            opt.pack(side='top', fill=BOTH, pady=(0, 15))

        def callback(self, *args):
            self.style.theme_use(self.variable.get().lower())


class left_panel:
    """
        This class presents 4 tabs ('All images', 'Selected images', 'Tags', 'Help') in which we can browse.
        This tabs are frames. The first 2 are scrollable.
    """

    def __init__(self, father, images: List[img.Img], tags) -> None:
        self.mod = 4
        self.father = father
        self.img_list = images
        self.old_path = img.path_to_image
        self.notebook = ttk.Notebook(father)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.titles = ["All images", "Cropped images", "Tags", "Help"]
        self.tabs = [ttk.Frame(self.notebook) for i in range(len(self.titles))]

        self.under_frame1 = sf.create_scrollable_frame(self.tabs[0])
        self.under_frame2 = self.tabs[1]
        self.list_of_cropped_images: List[img.Img] = []

        create_frame(self.mod, self.under_frame1)
        # self.create_frame(self.under_frame2)

        tags.tag_panel = tag_panel.tag_panel(self.tabs[-2], tags)
        help_panel.main(self.tabs[-1])

    def initialise(self):
        """ We create the 4 tabs and all images object in 'All images' frame """
        map(tk.Pack, self.tabs)
        # self.notebook.bind("<<NotebookTabChanged>>", self.updateSelected)
        for pos, i in enumerate(self.img_list):
            self.create_img(i, self.under_frame1, pos)
        for f, i in zip(self.tabs, self.titles):
            self.notebook.add(f, text=i)
        self.cropped_panel = cropped_panel.Cropped_Panel(
            self.under_frame2, self.img_list)

    def create_img(self, i,  frm: Frame, pos):
        """
            If we are in 'All images' frame (under_frame1) (resp. 'Selected images' (under_frame2))
            then we create a image object with corresponding bind (cf. images.py)
        """
        img = i.createMiniLabel2(self.under_frame1)
        img.grid(row=pos // self.mod, column=pos %
                 self.mod, ipadx=5, ipady=5, sticky='nswe')


class main_class:
    """ The main class wich manages both left and rigth panels (creation and initialization) """

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
        self.right_panel.pack(side="right", fill=tk.Y, padx=10, pady=10)

        self.frame.pack(fill=tk.BOTH, expand=1)

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.lp = left_panel(self.left_panel, self.list_img, self.list_tag)
        self.lp.initialise()

    def create_right_panel(self):
        self.rp = right_panel(self.root, self.right_panel,
                              self.list_img, self.list_tag, self.lp)
        self.rp.initialise()
