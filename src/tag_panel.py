import tkinter as tk
from tkinter import Pack, ttk
from typing import List
from tags import Tag
from scrollableframe import create_scrollable_frame


class tag_panel(ttk.Frame):
    def __init__(self, master, tag_list: Tag) -> None:
        super().__init__(master)
        self.main_pane = ttk.PanedWindow(self)
        self.upper_pane = create_scrollable_frame(self.main_pane)
        self.bottom_pane = ttk.PanedWindow(self.main_pane)
        self.tag_list = tag_list
        self.buttons: List[ttk.Button] = []
        self.bottom_pane.pack(expand=1, fill=tk.BOTH)
        self.main_pane.pack(expand=1, fill=tk.BOTH)
        self.pack(expand=1, fill=tk.BOTH)
        self.all_tags()
        self.down_menu()

    def all_tags(self):
        def remove_button(e):
            self.tag_list.remove(e.widget['text'])
            e.widget.grid_forget()
        mod = 8
        [i.grid_forget() for i in self.buttons]
        for (pos, elt) in enumerate(sorted(list(self.tag_list))):
            if elt == "&#undefined":
                continue
            buttomI = ttk.Button(self.upper_pane, text=elt, width=4)
            buttomI.grid(row=pos // mod,
                         column=pos % mod,
                         ipadx=5, ipady=5, sticky='nesw')
            buttomI.bind('<Button>', remove_button)
            self.buttons.append(buttomI)
        self.upper_pane.grid_rowconfigure(0, weight=1)
        self.upper_pane.grid_columnconfigure(0, weight=1)

    def down_menu(self):
        add_tag = ttk.Button(self.bottom_pane, text='Add tag',
                             command=self.add_tag_listener)
        add_tag.pack(expand=1, fill=tk.BOTH)

    def add_tag_listener(self):
        def on_change(e):
            self.tag_list.add(e.widget.get())
            window.destroy()
            [i.grid_forget() for i in self.buttons]
            self.all_tags()
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


def main(parent, tag):
    return tag_panel(parent, tag)
