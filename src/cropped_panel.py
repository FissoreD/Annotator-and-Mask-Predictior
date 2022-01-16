from tkinter import Label, ttk, filedialog
from PIL import ImageTk
from PIL.Image import Image
import PIL
import images
from typing import List
from tkinter.constants import BOTH, LEFT
import tkinter as tk
import read_write
import tags
import scrollableframe as sf
import nnl_process
from tkinter.scrolledtext import ScrolledText
from global_vars import *

param = {'expand': 1, "fill": BOTH}


def create_image(parent, img: Image, tag_name):
    pnl = ttk.Frame(parent, borderwidth=1)
    Label(pnl, text=tag_name).pack(param)
    img = img.resize(
        (int(img.width * 0.8), int(img.height * 0.8)), PIL.Image.HAMMING)
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

        self.botton_panel = ttk.PanedWindow(self.main_pane)

        self.image_panel = ttk.PanedWindow(self.main_pane)
        self.image_panel_scroll = sf.create_scrollable_frame(self.image_panel)
        f1 = tk.Frame(self.image_panel_scroll)
        self.image_panel_scroll.canvas.bind(
            '<Configure>', lambda e: f1.config(width=e.width))

        self.image_panel.pack(param, side=LEFT)
        self.botton_panel.pack(expand=1)
        self.pack(param)
        f1.grid(columnspan=self.mod, row=100)

        self.list_of_cropped_images: List[Image] = []
        self.list_of_cropped_labels: List[Label] = []
        self.img_list = img_list
        self.initialize(self.botton_panel)
        self.main_pane.pack(param)

    def initialize(self, parent):
        button = ttk.Button(
            parent,
            text='Create cropped images',
            command=self.cropped_images_listener)
        train_model = ttk.Button(
            parent,
            text='Train the model',
            command=nnl_process.train_the_model)
        makePrediction = ttk.Button(
            parent,
            text='Make Prediction',
            command=self.make_prediction_panel)

        self.text = tk.Text(parent, width=20, height=20,
                            wrap='word', fg='blue')
        self.text.insert(tk.END,
                         "HELP :\n"
                         "1. Click crop images \n"
                         " → this will crop all annotation of the 'All images' panel\n\n"
                         "2. Train the model\n"
                         " → this will create and train the model from cropped images\n\n"
                         "3. Make prediction\n"
                         " → this will open a new window where you can load "
                         "images from disk and make the prediction")
        self.text.config(state=tk.DISABLED)

        button.pack(**param)
        train_model.pack(**param)
        makePrediction.pack(**param)
        self.text.pack()

    def cropped_images_listener(self):
        cp_list = self.list_of_cropped_images
        lb_list = self.list_of_cropped_labels
        while cp_list:
            lb_list.pop().grid_forget()
            cp_list.pop()
        for img in self.img_list:
            img.crop_image(cp_list)
        for img in cp_list:
            lb_list.append(create_image(self.image_panel_scroll, *img))
        for pos, lbl in enumerate(lb_list):
            lbl.grid(row=pos // self.mod, column=pos % self.mod,
                     ipadx=5, ipady=5, sticky='nswe')
        read_write.create_all_cropped_images(self.img_list)

    def make_prediction_panel(self):
        def make_perc(nb):
            return round(float(nb * 100), 2)

        path = [""]

        def sel():
            try:
                isProba = var.get() == 1
                scroll.delete('1.0', tk.END)
                for fn in path[0]:
                    res = nnl_process.predict(
                        model, fn, isProba=isProba)
                    fn = fn.split("/")[-1]
                    if not isProba:
                        scroll.insert(
                            tk.INSERT, f"{fn} is a {res[0]} at {make_perc(res[1])} %\n")
                    else:
                        L = sorted([(i, j) for (i, j) in zip(
                            res[0], res[1])], key=lambda a: a[1], reverse=True)
                        scroll.insert(tk.INSERT, f"{fn} is a:\n")
                        for (i, j) in L:
                            perc = make_perc(j)
                            scroll.insert(tk.INSERT, f" - {i} at ")
                            scroll.insert(tk.INSERT, f"{perc} %\n",
                                          'red' if perc > 50 else 'blue')
            except FileNotFoundError:
                pass

        def choose_path():
            path[0] = filedialog.askopenfilenames(
                filetypes=[('Images', img_ext)])
            sel()

        model = nnl_process.read_model()
        tl = tk.Toplevel(self)
        tl.focus()
        tl.grab_set()

        choose_path_bt = ttk.Button(
            tl, text='Choose your image to analyse', command=choose_path)
        choose_path_bt.pack(param)

        panel_radio = ttk.PanedWindow(tl)

        var = tk.IntVar()
        radio1 = ttk.Radiobutton(
            panel_radio, text="Probability", variable=var,
            value=1, command=sel)
        radio2 = ttk.Radiobutton(
            panel_radio, text="Category", variable=var,
            value=2, command=sel)
        radio1.pack(param, side=tk.LEFT)
        radio2.pack(param, side=tk.LEFT)
        panel_radio.pack(param)
        var.set('1')

        scroll = ScrolledText(tl, width=20, height=10)
        color_list = ['red', 'green', 'blue', 'magenta']
        for i in color_list:
            scroll.tag_config(i, foreground=i)
        scroll.pack(param)


if __name__ == "__main__":
    tag_list = tags.Tag(images.open_files())
    img_list = tag_list.imgs

    for j in img_list:
        j.set_tag_list(tag_list)

    main = tk.Tk()
    Cropped_Panel(main, img_list).make_prediction_panel()
    main.mainloop()
