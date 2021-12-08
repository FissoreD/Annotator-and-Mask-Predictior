import tkinter as tk
from tkinter.constants import LEFT

from read_write import read_file


def left_panel(parent):
    panel_left = tk.PanedWindow(parent)
    panel_right = tk.PanedWindow(parent)
    all_img_button = tk.Button(panel_left, text='All images',
                               width=20, command=lambda: (right_panel(panel_right)))
    selected_button = tk.Button(panel_left, text='Selected images',
                                width=20, command=lambda: (right_panel1(panel_right)))
    tag_button = tk.Button(panel_left, text='Tags', width=20)
    all_img_button.grid(column=0, row=1)
    selected_button.grid(column=0, row=2, pady=10)
    tag_button.grid(column=0, row=3)
    panel_left.pack(side="left")
    panel_right.pack()


def right_empty_panel(parent):
    panel_right_empty = tk.PanedWindow(parent)
    panel_right_empty.pack()


def clean_panel(panel):
    [i.destroy() for i in panel.winfo_children()]


def right_panel(parent):
    clean_panel(parent)
    T = tk.Text(parent, width=30)
    file = open('text/panel_text.txt', 'r')
    data = file.read()
    T.pack()
    T.insert(tk.END, data)
    file.close()


def right_panel1(parent):
    clean_panel(parent)
    T = tk.Text(parent, width=30)
    file = open('text/panel_text1.txt', 'r')
    data = file.read()
    T.pack()
    T.insert(tk.END, data)
    file.close()

# distruggere il panel prima di aprire quello nuovo cliccando sul bottone
# inserire i testi
# collegarli ai diversi bottoni
# abbellire tutto, inserendo anche immagini
# se non trovo come pulire il panel, creo un panel in quello più grande che poi verrà distrutto


def main(parent):
    left_panel(parent)
