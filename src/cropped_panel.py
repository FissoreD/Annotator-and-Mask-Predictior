from tkinter import Label, messagebox, ttk, filedialog
from PIL import ImageTk
from PIL.Image import Image
import images
from typing import List
from tkinter.constants import BOTH, LEFT
import tkinter as tk
import read_write
import tags
import scrollableframe as sf
import nnl_process
from tkinter.scrolledtext import ScrolledText

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
        train_model = ttk.Button(
            self.bottom_pane,
            text='Train the model',
            command=nnl_process.make_all)
        makePrediction = ttk.Button(
            self.bottom_pane,
            text='Make Prediction',
            command=self.make_prediction_panel)
        button.pack(**param)
        train_model.pack(side=LEFT, **param)
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
        read_write.create_all_cropped_images(self.img_list)

    def make_prediction_panel(self):
        def make_perc(nb):
            return round(float(nb * 100), 2)

        def sel():
            try:
                isProba = var.get() == 1
                scroll.delete('1.0', tk.END)
                for fn in file_name.get().split(', '):
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
                messagebox.showinfo("Error", "Choose a valid file")

        def choose_path():
            path = filedialog.askopenfilenames(
                filetypes=[('Images', '*.jpg *.png')])
            file_name.delete(0, tk.END)
            file_name.insert(0, ', '.join(path))
            sel()

        model = nnl_process.read_model()
        tl = tk.Toplevel(self)
        tl.focus()
        tl.grab_set()

        choose_path_pnl = ttk.PanedWindow(tl)
        file_name = ttk.Entry(choose_path_pnl)
        send_bt = ttk.Button(choose_path_pnl, text='Send', command=sel)
        file_name.pack(param, side=tk.LEFT)
        send_bt.pack(**param, side=tk.LEFT)
        choose_path_pnl.pack(param)

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
