from sre_parse import expand_template
from textwrap import fill
import tkinter as tk
from tkinter import BOTH, LEFT, ttk
from typing import List
from tags import Tag
from scrollableframe import create_scrollable_frame


class tag_panel(ttk.Frame):
    """This class corresponds to the 'Tags' tab """

    def __init__(self, master, tag_list: Tag) -> None:
        super().__init__(master)
        self.mod = 3
        self.main_pane = ttk.PanedWindow(self)
        self.scroll_pane = ttk.PanedWindow(self)
        self.upper_pane = create_scrollable_frame(self.scroll_pane)
        f1 = tk.Frame(self.upper_pane)
        self.upper_pane.canvas.bind(
            '<Configure>', lambda e: f1.config(width=e.width))
        self.scroll_pane.pack(fill=tk.BOTH, expand=1, side=LEFT)
        self.bottom_pane = ttk.PanedWindow(self.main_pane)
        self.tag_list = tag_list
        self.buttons: List[ttk.Button] = []
        self.bottom_pane.pack(expand=1)
        self.main_pane.pack(expand=1, fill=tk.BOTH)
        self.pack(expand=1, fill=tk.BOTH)
        f1.grid(columnspan=self.mod, row=100)
        self.all_tags()
        self.down_menu()

        self.m = tk.Menu(self, tearoff=0)
        self.original_background = ttk.Label().cget("background")

    def popup(self, event):
        """ When we rigth-click on a tag, we can delete or rename it """
        try:
            self.m.delete("Delete")
            self.m.delete("Rename")
        except:
            pass

        self.m.add_command(
            label="Rename", command=lambda: self.add_tag_listener(isRenaming=event.widget["text"]))

        self.m.add_command(
            label="Delete", command=lambda: self.remove_button(event))

        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def remove_button(self, e):
        """ Method to remove a tag (it remove it also from tag_list) """
        self.buttons.remove(e.widget)
        self.tag_list.remove(e.widget['text'])
        e.widget.grid_forget()

    def all_tags(self):
        """ For all tags, we create the respective label with its corresponding binds """

        [i.grid_forget() for i in self.buttons]
        self.buttons = []
        for (pos, elt) in enumerate(sorted(list(self.tag_list - {'&#undefined'}))):
            buttomI = ttk.Label(self.upper_pane, text=elt,
                                anchor=tk.CENTER, borderwidth=1, relief="solid")
            buttomI.bind('<Button-2>', self.popup)
            buttomI.bind('<Enter>', lambda e: self.hover(e, True))
            buttomI.bind('<Leave>', lambda e: self.hover(e))
            buttomI.grid(row=pos // self.mod, column=pos %
                         self.mod, sticky='nsew', padx=1, pady=1, ipady=3)
            self.buttons.append(buttomI)

    def hover(self, button, isEntering=False):
        """ At tag's overflight, highlighting of it """
        button.widget.config(
            background="white" if isEntering else self.original_background)

    def down_menu(self):
        """ Creation of the button wich allows us create new tag """
        add_tag = ttk.Button(self.bottom_pane, text='Add tag',
                             command=self.add_tag_listener)

        text = tk.Text(self.bottom_pane, width=20, height=20,
                       wrap='word', fg='blue')
        text.insert(
            tk.END, "HELP : \n"
            "To remove or rename tag right-click on it\n\n"
            "NOTE : \n"
            "Ff you delete a tag, this same tag will be removed "
            "from every images having it")
        text.config(state=tk.DISABLED)
        add_tag.pack(expand=1, fill=BOTH)
        text.pack()

    def add_tag_listener(self, isRenaming=None):
        """ Opening of a window wich allows us to enter a name and valid it by pressing 'Enter' key """
        def on_change(e):
            [i.grid_forget() for i in self.buttons]
            self.new_tag = e.widget.get()
            if isRenaming != None:
                self.tag_list.rename(isRenaming, self.new_tag)
            else:
                self.tag_list.add(self.new_tag)
            window.destroy()
        window = tk.Toplevel(self)
        window.title("Add tag")
        window.focus()
        window.grab_set()
        window.wm_resizable(False, False)
        label = ttk.Label(window, text='Write new label')
        entry = ttk.Entry(window)
        label.pack()
        entry.pack()
        entry.focus()
        entry.bind("<Return>", on_change)
