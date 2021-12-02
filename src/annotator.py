import tkinter as tk
import time
from PIL import Image
from PIL import ImageTk


class annotator:
    def __init__(self, frm, image):
        self.frm = frm
        self.window = tk.Toplevel(self.frm)
        self.window.title("Annotator")
        self.window.focus()
        self.window.grab_set()

        self.rect_list = []

        self.image = image

        mainPanel = tk.PanedWindow(self.window, bg='red')
        mainPanel.grid(row=0, column=0)

        # img = Image.open(image.path)

        # img.resize((500, 500), Image.ANTIALIAS)
        # photo = ImageTk.PhotoImage(img)
        # imgLabel = tk.Label(mainPanel, image=photo, anchor=tk.CENTER)
        # imgLabel.image = photo
        # self.imgLabel: tk.Label = imgLabel
        # imgLabel.place(relx=0.5, rely=0.5, anchor='center')

        transp = tk.PhotoImage(file=image.path)
        self.canvas = tk.Canvas(mainPanel, width=400, height=300)
        self.canvas.create_image(200, 150, image=transp)
        self.canvas.image = transp
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.pack()
        for tag_name in image.tag_of_rect:
            rects = image.tag_of_points[tag_name]
            for pos, rec in enumerate(rects):
                x, y, x1, y1 = rec[0][0], rec[0][1], rec[1][0], rec[1][1]
                rec_id = self.create_rec(x, y, x1, y1)
                image.tag_of_rect[tag_name][pos][1] = rec_id

        # transp = ImageTk.PhotoImage(file='../img/transparent.png')
        # self.canvas.create_image(0, 0, image=transp)

        # imgLabel.pack()
        mainPanel.pack()

        self.mainPanel = mainPanel
        self.is_clicked = False
        self.canvas.bind('<Motion>', self.myfunction)
        self.canvas.bind('<Button-1>', self.swap)
        self.canvas.bind('<Button-3>', self.clear)

    def myfunction(self, event):
        if self.is_clicked:
            try:
                self.canvas.delete(self.r[0])
                self.canvas.delete(self.r[1])
            except AttributeError:
                pass
            x, y = event.x, event.y
            canvas = self.canvas
            x1, y1 = self.old_coords
            self.r = self.create_rec(x, y, x1, y1)

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
            print('Adding', self.r)
            res = self.image.add_tag(
                'test', *self.old_coords, event.x, event.y, self.r)
            if res == False:
                self.canvas.delete(self.r[0])
                self.canvas.delete(self.r[1])
                # TODO: Add popup to say that the window is too small
                return
            if type(res) == tuple:
                info, other = res
                if info == 'contains':
                    # self.canvas.itemconfigure(other, outline='red')
                    # self.canvas.itemconfigure(self.r, outline='green')
                    self.canvas.delete(self.r[0])
                    self.canvas.delete(self.r[1])
                elif info == 'contained':
                    # self.canvas.itemconfigure(other, outline='green')
                    # self.canvas.itemconfigure(self.r, outline='red')
                    self.canvas.delete(self.r[0])
                    self.canvas.delete(self.r[1])
                elif info == 'overlap':
                    self.canvas.delete(self.r[0])
                    self.canvas.delete(self.r[1])
                elif info == 'overlapped':
                    self.canvas.delete(self.r[0])
                    self.canvas.delete(self.r[1])

    def create_rec(self, x, y, x1, y1):
        return self.create_rectangle(x, y, x1, y1, width=2, fill='green', alpha=.5)

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

    def open(self):
        self.window.deiconify()

    def clear(self, event):
        print('ciao')
        self.canvas.delete('all')

    def close(self):
        self.window.withdraw()


def main(frm, frame):
    annot = annotator(frm, frame)
    return annot.open()
