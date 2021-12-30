import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox

""" Default tag's name before its real attributed name """
invalid_word = "&#undefined"


def window_parametrize(window):
    window.focus()
    window.grab_set()


class annotator(tk.Toplevel):

    """ This class manages the windows which appears when we click on a selected image to make annotations """

    def __init__(self, frm, image):
        super().__init__(frm)
        self.tag_list = image.tag_list
        self.frm = frm
        self.title("Annotator")
        window_parametrize(self)
        self.wm_resizable(False, False)

        self.rect_list = []

        self.image = image

        mainPanel = ttk.PanedWindow(self)
        mainPanel.grid(row=0, column=0)

        im1: Image = image.big_image
        im = ImageTk.PhotoImage(im1)
        self.canvas = tk.Canvas(mainPanel,
                                height=im1.size[1], width=im1.size[0])
        self.canvas.create_image(im.width()/2, im.height()/2, image=im)
        self.canvas.image = im
        self.canvas.pack()

        """ For all images, we create the corresponding saved annotations """
        for tag_name in image.tag_of_rect:
            rects = image.tag_of_points[tag_name]
            for pos, rec in enumerate(rects):
                rec_id = self.create_rec(*rec)
                image.tag_of_rect[tag_name][pos][1] = rec_id

        mainPanel.pack(fill=tk.BOTH, expand=1)

        self.mainPanel = mainPanel
        self.is_clicked = False

        self.canvas.bind('<Motion>', self.draw_rect_on_motion)
        self.canvas.bind('<Button-1>', self.swap)
        self.bind('<Escape>', self.escape)

        self.m = tk.Menu(self, tearoff=0)

    def popup(self, event, r):
        """ Create and display the contextual menu at left-click mouse event on an annotation """
        try:
            self.m.delete("Delete")
            self.m.delete("Rename")
        except:
            pass

        self.m.add_command(
            label="Delete", command=lambda: self.delete_elt(r, ""))

        self.m.add_command(
            label="Rename", command=lambda: self.set_tag_for_annotation((True, r)))
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def deleteCurrent(self):
        """ Delete the current drawn rectangle """
        try:
            self.canvas.delete(self.r[0])
            self.canvas.delete(self.r[1])
        except AttributeError:
            pass

    def escape(self, event):
        """ When we press 'Escape' key, we cancel the current annotation """
        if self.is_clicked:
            self.is_clicked = not self.is_clicked
            self.deleteCurrent()

    def draw_rect_on_motion(self, event):
        """ To see the rectangle taking shape in real time """
        if self.is_clicked:
            self.deleteCurrent()
            x, y = event.x, event.y
            self.r = self.create_rec(x, y, *self.old_coords)

    def swap(self, event):
        """
            When the rectangle (the area corresponding to the annotation) is drawn,
            we make sure that it is conform (not too small, not overriding an existing one, etc.)
            If it isn't, we delete it before display an adverting message else we open the
            window which manage the newly created annotation name's
        """
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
                invalid_word, *self.old_coords, event.x, event.y, self.r)
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
        """ Delete a rectangle passed in parameter and display an error message """
        self.canvas.delete(r[0])
        self.canvas.delete(r[1])
        self.image.delete_from_id(r)
        if errorMsg != "":
            messagebox.showinfo("Warning", errorMsg)

    def create_rec(self, x, y, x1, y1):
        """
            Create a rectangle with 3 binds :
                - rigth-click mouse : open the contextual menu
                - the cursor is over the rectangle : we display it name on the left-bottom window's corner
                - the cursor is outside it : we un-display name
        """
        r = self.create_rectangle(
            x, y, x1, y1, width=2, fill='green', alpha=.5)
        self.canvas.tag_bind(r[0], '<Button-3>',
                             lambda e: self.popup(e, r))
        self.canvas.tag_bind(
            r[0], '<Motion>', lambda e: self.create_tooltip(e, r, True))
        self.canvas.tag_bind(
            r[0], '<Leave>', lambda e: self.create_tooltip(e, r, False))
        return r

    def create_tooltip(self, _, r, isEntering):
        """
            Creation of the tooltip which appears on rectangle's overring
            This is a canvas text unboxed in an canvas rectangle
            isEntering : boolean which indicate us if the cursor is out or inside
        """
        try:
            self.canvas.delete(self.idtooltip)
            self.canvas.delete(self.idtooltip2)
        except AttributeError:
            pass

        if isEntering and not self.is_clicked:
            self.idtooltip2 = self.canvas.create_text(4, self.canvas.winfo_height() - 4,
                                                      text=self.image.find_tag_by_rect_id(
                                                          r)[0],
                                                      anchor='sw')
            self.idtooltip = self.canvas.create_rectangle(
                self.canvas.bbox(self.idtooltip2), fill="white")
            self.canvas.tag_lower(self.idtooltip, self.idtooltip2)
            self.canvas.update()

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        """
            At the creation of a rectangle, this method is called to correctly set all the option, parameters
            of it (colors, opacity, etc.). And we make sure to save it on the rectangles list
        """
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.frm.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (abs(x2-x1), abs(y2-y1)), fill)
            self.rect_list.append(ImageTk.PhotoImage(image))
            img = self.canvas.create_image(
                min(x1, x2), min(y1, y2), image=self.rect_list[-1], anchor='nw')
        return img, self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def set_tag_for_annotation(self, is_renaming=(False, 0)):
        """
            After creating the area, we ask to the user to name it.
            The window is open.
            If there are already tag names, a scrolling menu is proposed in which he can choose the wanted name
            else, in all cases, we propose to user to create one on the fly
        """
        window = tk.Toplevel(self)
        window.title("Set tag")
        window_parametrize(window)
        panel = tk.PanedWindow(window)
        panel.pack(padx=10, pady=10)

        L = [i for i in self.image.tag_list if i != invalid_word]

        def do_rename(x):
            if is_renaming[0]:
                self.image.rename_tag_of_rect(is_renaming[1], x.capitalize())
            else:
                self.tag_list.rename(invalid_word, x.capitalize())

        """ Check if the user have existing tags, if so, we create the option menu """
        if len(L) != 0:
            x = L[0]

            variable = tk.StringVar(panel)
            variable.set(x)

            opt = ttk.OptionMenu(panel, variable, L[0], *L)
            opt.pack(expand=1, fill=BOTH)

            def on_change():
                """ We get chosen name and rename the current annotation"""
                x = variable.get()
                window.destroy()
                window_parametrize(self)
                do_rename(x)
            butt = ttk.Button(panel, text='Send', command=on_change)
            butt.pack(expand=1, fill=tk.BOTH)
            ttk.Separator(panel, orient='horizontal').pack(fill='x', pady=7)

        """ Entry field """
        entry = ttk.Entry(panel)

        def create_tag():
            """
                If the entry is the empty string or the invalid_word, we display an warning message, else
                we correctly rename the current annotation, add the tag in the tag list and close the window. 
            """
            x = entry.get()
            if x == "" or x.capitalize() == invalid_word:
                messagebox.showinfo("Error", "Invalid Tag name")
                return
            self.tag_list.add(x)
            do_rename(x)
            window.destroy()
            window_parametrize(self)

        entry.bind("<Return>", lambda _: create_tag())
        entry.pack(expand=1, fill=tk.BOTH)

        creator = ttk.Button(
            panel, text="Create And Send", command=create_tag)
        creator.pack(expand=1, fill=tk.BOTH)


def main(frm, frame):
    """ Create an instance of the class annotator """
    annotator(frm, frame)
