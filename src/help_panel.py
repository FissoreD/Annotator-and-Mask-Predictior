import tkinter as tk
from tkinter.constants import BOTH
from tkinter import ttk
from global_vars import *
from tkhtmlview import HTMLLabel

""" This file aims to manage the tag 'Help' """

button_properties = {
    'relief': 'solid',
    'activebackground': '#F9FC77',
    'cursor': 'hand2',
    'width': 20
}

file_path_list = [
    ('All images', 'text_allimg.html'),
    ('Selected images', 'text_selectimg.html'),
    ('Tags', 'text_tags.html'),
    ('Others', 'text_others.html')
]


def right_empty_panel(parent):
    panel_right_empty = ttk.PanedWindow(parent)
    panel_right_empty.pack()


def clean_panel(panel):
    """ To clean the panel, we loop over all the children of it, and destroy them """
    [i.destroy() for i in panel.winfo_children()]


def right_panel(parent, file_path):
    """ To display information, we clean the old panel, read the corresponding file wich contains help info and show it """
    clean_panel(parent)
    file = open(file_path, 'r')
    data = file.read()
    HTMLLabel(parent, html=data).pack(fill=BOTH, expand=1)
    file.close()


def create_button(panel_left, panel_right, pos):
    """ Create a button with panel_left as parent and the rigth_panel method as effect """
    return tk.Button(panel_left,
                     **button_properties,
                     text=file_path_list[pos][0],
                     command=lambda: right_panel(panel_right, test_for_help + file_path_list[pos][1]))


def main(parent):
    """
        panel_left contains the buttons stored in button_list
        panel_rigth will display the corresponding information
    """
    panel_left = ttk.PanedWindow(parent)
    panel_right = ttk.PanedWindow(parent)
    button_list = [create_button(panel_left, panel_right, i) for i in range(4)]
    for pos, button in enumerate(button_list):
        button.grid(column=0, row=pos, pady=5)

    panel_left.pack(side="left")
    panel_right.pack(expand=1, fill=BOTH)
