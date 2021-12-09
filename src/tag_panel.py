import tkinter as tk
from tkinter import Pack, ttk
from typing import List
from tags import Tag
from scrollableframe import create_scrollable_frame


class tag_panel(ttk.Frame):
    def __init__(self, master, tag_list: Tag) -> None:
        super().__init__(master)
        self.mod = 3
        self.main_pane = ttk.PanedWindow(self)
        self.upper_pane = create_scrollable_frame(self.main_pane)
        f1 = tk.Frame(self.upper_pane)
        self.upper_pane.canvas.bind(
            '<Configure>', lambda e: f1.config(width=e.width))
        self.bottom_pane = ttk.PanedWindow(self.main_pane)
        self.tag_list = tag_list
        self.buttons: List[ttk.Button] = []
        self.bottom_pane.pack(fill=tk.BOTH)
        self.main_pane.pack(expand=1, fill=tk.BOTH)
        self.pack(expand=1, fill=tk.BOTH)
        f1.grid(columnspan=self.mod, row=100)
        self.all_tags()
        self.down_menu()

    def all_tags(self):
        def remove_button(e):
            self.buttons.remove(e.widget)
            self.tag_list.remove(e.widget['text'])
            e.widget.grid_forget()
        [i.grid_forget() for i in self.buttons]
        self.buttons = []
        for (pos, elt) in enumerate(sorted(list(self.tag_list - {'&#undefined'}))):
            buttomI = ttk.Button(self.upper_pane, text=elt)
            buttomI.grid(row=pos // self.mod, column=pos %
                         self.mod, sticky='nsew')
            buttomI.bind('<Button>', remove_button)
            self.buttons.append(buttomI)

    def down_menu(self):
        add_tag = ttk.Button(self.bottom_pane, text='Add tag',
                             command=self.add_tag_listener)
        add_tag.pack(expand=1, fill=tk.BOTH)

    def add_tag_listener(self):
        def on_change(e):
            [i.grid_forget() for i in self.buttons]
            self.tag_list.add(e.widget.get())
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
