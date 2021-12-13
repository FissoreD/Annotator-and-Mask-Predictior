import tkinter as tk
from tkinter import ttk
import time
from PIL import Image
from PIL import ImageTk
import time
from tkinter import messagebox


class annotator:
    def __init__(self, frm, image):
        self.tag_list = image.tag_list
        self.frm = frm
        self.window = tk.Toplevel(self.frm)
        self.window.title("Annotator")
        self.window.focus()
        self.window.grab_set()
        self.window.wm_resizable(False, False)

        self.rect_list = []

        self.image = image

        mainPanel = ttk.PanedWindow(self.window)
        mainPanel.grid(row=0, column=0)

        im1 = Image.open(image.path)
        maxSize = 500
        XSIZE = maxSize if im1.width > im1.height else maxSize * im1.width//im1.height
        YSIZE = maxSize if im1.height > im1.width else maxSize * im1.height//im1.width

        im1 = im1.resize((XSIZE, YSIZE), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(im1)
        self.canvas = tk.Canvas(mainPanel, height=YSIZE, width=XSIZE)
        self.canvas.create_image(im.width()/2, im.height()/2, image=im)
        self.canvas.image = im
        self.canvas.pack()

        for tag_name in image.tag_of_rect:
            rects = image.tag_of_points[tag_name]
            for pos, rec in enumerate(rects):
                x, y, x1, y1 = rec[0][0], rec[0][1], rec[1][0], rec[1][1]
                rec_id = self.create_rec(x, y, x1, y1)
                image.tag_of_rect[tag_name][pos][1] = rec_id

        mainPanel.pack(fill=tk.BOTH, expand=1)

        self.mainPanel = mainPanel
        self.is_clicked = False

        self.canvas.bind('<Motion>', self.draw_rect_on_motion)
        self.canvas.bind('<Button-1>', self.swap)
        self.window.bind('<Escape>', self.escape)

    def deleteCurrent(self):
        try:
            self.canvas.delete(self.r[0])
            self.canvas.delete(self.r[1])
        except AttributeError:
            pass

    def escape(self, event):
        if self.is_clicked:
            self.is_clicked = not self.is_clicked
            self.deleteCurrent()

    def draw_rect_on_motion(self, event):
        if self.is_clicked:
            self.deleteCurrent()
            x, y = event.x, event.y
            self.r = self.create_rec(x, y, *self.old_coords)

    def swap(self, event):
        x, y = event.x, event.y
        self.is_clicked = not self.is_clicked
        if self.is_clicked:
            try:
                del self.r
            except AttributeError:
                pass
            self.old_coords = (x, y)
        else:
            res = self.image.add_tag(
                "&#undefined", *self.old_coords, event.x, event.y, self.r)
            if res == False:
                self.delete_elt(self.r, "The selected zone is too small")
                return
            elif type(res) == tuple:
                info, other = res
                if info == 'contains':
                    self.delete_elt(
                        self.r, "New zone convers an existing zone")
                elif info == 'contained':
                    self.delete_elt(
                        self.r, "New zone is convered by an existing zone")
                elif info == 'overlapped':
                    self.delete_elt(
                        self.r, "New zone overlaps more than 20% of an existing zone")
                elif info == 'overlap':
                    self.delete_elt(
                        self.r, "More than 20% of new zone is overlapped by an existing zone")
            else:
                self.set_tag_for_annotation()

    def delete_elt(self, r, errorMsg):
        self.canvas.delete(r[0])
        self.canvas.delete(r[1])
        self.image.delete_from_id(r)
        if errorMsg != "":
            messagebox.showinfo("Warning", errorMsg)

    def create_rec(self, x, y, x1, y1):
        r = self.create_rectangle(
            x, y, x1, y1, width=2, fill='green', alpha=.5)
        self.canvas.tag_bind(r[0], '<Button-3>',
                             lambda x: self.delete_elt(r, ""))
        return r

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.frm.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (abs(x2-x1), abs(y2-y1)), fill)
            self.rect_list.append(ImageTk.PhotoImage(image))
            img = self.canvas.create_image(
                min(x1, x2), min(y1, y2), image=self.rect_list[-1], anchor='nw')
        return img, self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def set_tag_for_annotation(self):
        window = tk.Toplevel(self.window)
        window.title("Set tag")
        window.focus()
        window.grab_set()
        window.wm_resizable(False, False)

        L = [i for i in self.image.tag_list if i != "&#undefined"]

        if len(L) != 0:
            x = L[0]

            variable = tk.StringVar(window)
            variable.set(x)

            opt = ttk.OptionMenu(window, variable, *L)
            opt.pack()

            def on_change():
                x = variable.get()
                window.destroy()
                self.window.focus()
                self.window.grab_set()
                self.tag_list.rename("&#undefined", x)
            butt = ttk.Button(window, text='Send', command=on_change)
            butt.pack(expand=1, fill=tk.BOTH)
        entry = ttk.Entry(window)

        def create_tag():
            x = entry.get()
            if x == "":
                messagebox.showinfo("Error", "Invalid Tag name")
                return
            self.tag_list.add(x)
            self.tag_list.rename("&#undefined", x)
            window.destroy()
            self.window.focus()
            self.window.grab_set()

        entry.bind("<Return>", lambda e: create_tag())
        entry.pack(expand=1, fill=tk.BOTH)

        creator = ttk.Button(
            window, text="Create And Send", command=create_tag)
        creator.pack(expand=1, fill=tk.BOTH)


def main(frm, frame):
    annotator(frm, frame)
