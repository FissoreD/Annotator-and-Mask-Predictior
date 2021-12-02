import tkinter as tk
from PIL import Image


class annotator:
    def __init__(self, frm, image):
        self.frm = frm
        self.window = tk.Toplevel(self.frm)
        self.window.title("Annotator")
        self.window.focus()
        self.window.grab_set()
        #self.window.minsize(width=200, height=250)
        l = tk.Label(self.window, text="test")
        l.pack()
        canvas = tk.Canvas(self.window, width=500, height=500)
        canvas.pack()
        #image = Image(image.path)
        img = tk.PhotoImage(file=image.path)

        canvas.create_image(250, 250, image=img)
        canvas.image = img
        # self.photo = tk.ImageTk.PhotoImage(image.img)
        # self.label = tk.Canvas(self.window, image=self.photo, anchor=tk.CENTER)
        # self.label.image = self.photo
        # self.label.pack()
        # self.button = tk.Button(self.window, text="test")
        # self.button.pack()
        # win = tk.Toplevel(frm)
        # win.wm_title("Window")

        # b = tk.Button(win, text="Okay", command=win.destroy)
        # b.pack()

    def open(self):
        self.window.deiconify()

    def close(self):
        self.window.withdraw()


def main(frm, frame):
    annot = annotator(frm, frame)
    return annot.open()
