
"""
    This file aims to create the guy for the ImageAnnotator
    It only contains the structure and :
        ask for images to image_reader library
"""

from tkinter import Frame, ttk, filedialog
import images as img
from typing import List
from tkinter.constants import BOTH, CENTER, HORIZONTAL
import tkinter as tk
import tags
import scrollableframe as sf
import help_panel
import read_write
import tag_panel
from ttkthemes import ThemedTk

param = {'expand': 1, "fill": BOTH}


def get_selected_images(list_images: List[img.Img]):
    return [i for i in list_images if i.is_selected]


class right_panel:
    def __init__(self, root, father, list_image, list_tag, left_panel) -> None:
        self.root = root
        self.father = father
        self.list_img = list_image
        self.list_tag = list_tag
        self.lp = left_panel

    def initialise(self):
        self.tc = self.theme_class(self)
        sb = self.select_option(self)
        f1 = [read_write.write_file, read_write.read_file]
        save = ttk.Button(self.father, text='SaveToFile',
                          command=lambda: f1[0](self.list_img))
        load = ttk.Button(self.father, text='LoadFile',
                          command=lambda: f1[1](self.list_img))
        load.pack(param)
        save.pack(param)

    class select_option:
        def __init__(self, rp) -> None:
            self.main = ttk.PanedWindow(rp.father)
            self.rp = rp
            self.lp = rp.lp
            self.create_buttons()
            self.main.pack(param)

        def charge_img_folder(self, _):
            img.path_to_image = filedialog.askdirectory()
            tag_list = self.rp.list_tag
            tag_list.imgs = img.open_files()
            while self.rp.list_img:
                self.rp.list_img.pop()
            self.rp.list_img.extend(tag_list.imgs)
            for j in self.rp.list_img:
                j.set_tag_list(tag_list)
            self.rp.lp.updateSelected(None)
            return

        def create_buttons(self):
            self.lab = ttk.Label(
                self.main, text='Check/Uncheck box', anchor=CENTER)
            bp = ttk.PanedWindow(self.main)
            self.b1 = ttk.Button(bp, text='CheckAll',
                                 command=lambda: self.listener(True))
            self.b2 = ttk.Button(bp, text='UncheckAll',
                                 command=lambda: self.listener(False))
            self.b3 = ttk.Button(bp, text='Open Images From Folder',
                                 command=lambda: self.charge_img_folder(None))
            self.b1.grid(column=0, row=0, sticky='nsew')
            self.b2.grid(column=1, row=0, sticky='nsew')
            self.b3.grid(column=0, row=1, columnspan=2, sticky='nsew')
            self.lab.pack(fill=BOTH)
            bp.pack()

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
            themes = [i.upper() for i in self.style.theme_names()]
            self.variable.set(themes[0])
            self.variable.trace("w", self.callback)
            ttk.Label(self.rp.father, text= "Set theme:", anchor=CENTER).pack(fill=BOTH)
            opt = ttk.OptionMenu(self.rp.father, self.variable, *themes)
            opt.pack(side='top', fill=BOTH, pady=(0, 15))

        def callback(self, *args):
            self.style.theme_use(self.variable.get().lower())


class left_panel:
    def __init__(self, father, images: List[img.Img], tags) -> None:
        self.mod = 4
        self.father = father
        self.images = images
        self.old_path = img.path_to_image
        self.notebook = ttk.Notebook(father)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.titles = ["All images", "Selected images", "Tags", "Help"]
        self.tabs = [ttk.Frame(self.notebook) for i in range(len(self.titles))]

        self.under_frame1 = sf.create_scrollable_frame(self.tabs[0])
        self.under_frame2 = sf.create_scrollable_frame(self.tabs[1])

        self.create_frame(self.under_frame1)
        self.create_frame(self.under_frame2)

        tags.tag_panel = tag_panel.tag_panel(self.tabs[2], tags)
        help_panel.main(self.tabs[3])

    def create_frame(self, parent):
        f1 = ttk.Frame(parent)
        parent.canvas.bind('<Configure>', lambda e: f1.config(width=e.width))
        f1.grid(columnspan=self.mod)

    def initialise(self):
        [f.pack() for f in self.tabs]
        self.notebook.bind("<<NotebookTabChanged>>", self.updateSelected)
        for pos, i in enumerate(self.images):
            self.create_img(i, self.under_frame1, pos)
        for f, i in zip(self.tabs, self.titles):
            self.notebook.add(f, text=i)
        self.notebook.select(self.notebook.tabs()[2])

    def updateSelected(self, _):
        if self.notebook.index(self.notebook.select()) == 1 or self.old_path != img.path_to_image:
            for widget in self.under_frame2.winfo_children():
                widget.grid_forget() if isinstance(widget, tk.Label) else None
            image = [image for image in self.images if image.is_selected]
            for pos, i in enumerate(image):
                self.create_img(i, self.under_frame2, pos)
        if self.notebook.index(self.notebook.select()) == 0 and self.old_path != img.path_to_image:
            for widget in self.under_frame1.winfo_children():
                widget.grid_forget() if isinstance(widget, tk.Label) else None
            for pos, i in enumerate(self.images):
                self.create_img(i, self.under_frame1, pos)
            self.old_path = img.path_to_image

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
