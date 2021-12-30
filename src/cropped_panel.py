from tkinter import Button, Frame, Label, ttk, filedialog
from PIL import ImageTk

from PIL.Image import Image
import images
from typing import List
from tkinter.constants import BOTH, CENTER, LEFT
import tkinter as tk
import tags
import scrollableframe as sf
from ttkthemes import ThemedTk
from sys import argv
import nnl_process
import window

param = {'expand': 1, "fill": BOTH}


def create_image(parent, img, tag_name):
    pnl = ttk.Frame(parent, borderwidth=1)
    Label(pnl, text=tag_name).pack(param)
    photo = ImageTk.PhotoImage(img)
    imgLabel = Label(pnl, image=photo, anchor=tk.CENTER)
    imgLabel.image = photo
    imgLabel.pack(param)
    return pnl


class Cropped_Panel(ttk.Frame):
    def __init__(self, parent_panel, img_list: List[images.Img]):
        super().__init__(parent_panel)
        self.mod = 4

        self.main_pane = ttk.PanedWindow(self)
        self.upper_pane = sf.create_scrollable_frame(self.main_pane)
        f1 = tk.Frame(self.upper_pane)
        self.upper_pane.canvas.bind(
            '<Configure>', lambda e: f1.config(width=e.width))
        self.bottom_pane = ttk.PanedWindow(self.main_pane)

        self.bottom_pane.pack(fill=tk.BOTH)
        self.main_pane.pack(param)
        self.pack(param)
        f1.grid(columnspan=self.mod, row=100)

        self.list_of_cropped_images: List[Image] = []
        self.list_of_cropped_labels: List[Label] = []
        self.img_list = img_list
        self.initialize()

    def initialize(self):
        button = ttk.Button(
            self.bottom_pane,
            text='Create cropped images',
            command=self.cropped_images_listener)
        launchPrediction = ttk.Button(
            self.bottom_pane,
            text='LaunchPrediction',
            command=nnl_process.make_all)
        # TODO make a listener on this button
        makePrediction = ttk.Button(
            self.bottom_pane,
            text='MakePrediction')
        button.pack(**param)
        launchPrediction.pack(side=LEFT, **param)
        makePrediction.pack(side=LEFT, **param)

    def cropped_images_listener(self):
        cp_list = self.list_of_cropped_images
        lb_list = self.list_of_cropped_labels
        while cp_list:
            lb_list.pop().grid_forget()
            cp_list.pop()
        for img in self.img_list:
            img.crop_image(cp_list)
        for img in cp_list:
            lb_list.append(create_image(self.upper_pane, *img))
        for pos, lbl in enumerate(lb_list):
            lbl.grid(row=pos // self.mod, column=pos % self.mod,
                     ipadx=5, ipady=5, sticky='nswe')
