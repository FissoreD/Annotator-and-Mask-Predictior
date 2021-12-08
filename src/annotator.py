import tkinter as tk
import time
from PIL import Image
from PIL import ImageTk


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

        mainPanel = tk.PanedWindow(self.window, bg='red')
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

    def draw_rect_on_motion(self, event):
        if self.is_clicked:
            try:
                self.canvas.delete(self.r[0])
                self.canvas.delete(self.r[1])
            except AttributeError:
                pass
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
            chosen_tag = self.set_tag_for_annotation()
            res = self.image.add_tag(
                chosen_tag, *self.old_coords, event.x, event.y, self.r)
            if res == False:
                self.delete_elt(self.r)
                # TODO: Add popup to say that the window is too small
                return
            elif type(res) == tuple:
                info, other = res
                if info == 'contains':
                    self.delete_elt(self.r)
                elif info == 'contained':
                    self.delete_elt(self.r)
                elif info == 'overlap':
                    self.delete_elt(self.r)
                elif info == 'overlapped':
                    self.delete_elt(self.r)

    def delete_elt(self, r):
        self.canvas.delete(r[0])
        self.canvas.delete(r[1])
        self.image.delete_from_id(r)

    def create_rec(self, x, y, x1, y1):
        r = self.create_rectangle(
            x, y, x1, y1, width=2, fill='green', alpha=.5)
        self.canvas.tag_bind(r[0], '<Button-3>', lambda x: self.delete_elt(r))
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

        L = list(self.image.tag_list)
        x = L[0]

        variable = tk.StringVar(window)
        variable.set(x)

        opt = tk.OptionMenu(window, variable, *L)
        opt.config(width=8, font=('Helvetica', 12))
        opt.pack()

        def on_change():
            x = variable.get()
            window.destroy()
        butt = tk.Button(window, text='Send', command=on_change)
        butt.pack()
        return x


def main(frm, frame):
    annotator(frm, frame)
