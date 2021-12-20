import tkinter as tk
from tkinter.constants import BOTH, LEFT
from tkinter import Frame, ttk
from tkhtmlview import HTMLLabel

button_properties = {
    'relief': 'solid',
    'activebackground': '#F9FC77',
    'cursor': 'hand2',
    'width': 20
}

file_path_list = [
    'text/text_allimg.html',
    'text/text_selectimg.html',
    'text/text_tags.html',
    'text/text_others.html'
]

button_title = [
    'All images',
    'Selected images',
    'Tags',
    'Others'
]


def right_empty_panel(parent):
    panel_right_empty = ttk.PanedWindow(parent)
    panel_right_empty.pack()


def clean_panel(panel):
    [i.destroy() for i in panel.winfo_children()]


def right_panel(parent, file_path):
    clean_panel(parent)
    file = open(file_path, 'r')
    data = file.read()
    HTMLLabel(parent, html=data).pack(fill=BOTH, expand=1)
    file.close()


def create_button(panel_left, panel_right, pos):
    return tk.Button(panel_left,
                     **button_properties,
                     text=button_title[pos],
                     command=lambda: right_panel(panel_right, file_path_list[pos]))


def main(parent):
    panel_left = ttk.PanedWindow(parent)
    panel_right = ttk.PanedWindow(parent)
    buttom_list = [create_button(panel_left, panel_right, i) for i in range(4)]
    for pos, buttom in enumerate(buttom_list):
        buttom.grid(column=0, row=pos, pady=5)

    panel_left.pack(side="left")
    panel_right.pack(expand=1, fill=BOTH)
