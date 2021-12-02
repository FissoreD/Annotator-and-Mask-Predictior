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

        mainPanel = tk.PanedWindow(self.window)
        mainPanel.grid(row=0, column=0)

        img = Image.open(image.path)
        img.resize((500, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        imgLabel = tk.Label(mainPanel, image=photo, anchor=tk.CENTER)
        imgLabel.image = photo
        self.imgLabel: tk.Label = imgLabel
        imgLabel.place(relx=0.5, rely=0.5, anchor='center')

        transp = tk.PhotoImage(file='../img/transparent.png')
        self.canvas = tk.Canvas(mainPanel, width=400, height=300)
        self.canvas.create_image(200, 150, image=transp)
        self.canvas.image = transp
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.pack()

        # transp = ImageTk.PhotoImage(file='../img/transparent.png')
        # self.canvas.create_image(0, 0, image=transp)

        imgLabel.pack()
        mainPanel.pack()

        self.mainPanel = mainPanel
        self.is_clicked = False
        self.canvas.bind('<Motion>', self.myfunction)
        self.canvas.bind('<Button-1>', self.swap)
        self.canvas.bind('<Button-3>', self.clear)

    def myfunction(self, event):
        if self.is_clicked:
            x, y = event.x, event.y
            canvas = self.canvas
            x1, y1 = self.old_coords
            canvas.create_rectangle(x, y, x1, y1, width=2)
            print(x, y, x1, y1)

    def swap(self, event):
        x, y = event.x, event.y
        self.is_clicked = not self.is_clicked
        if self.is_clicked:
            self.old_coords = (x, y)

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
