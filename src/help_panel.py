import tkinter as tk
from tkinter.constants import LEFT
from tkinter import ttk

from read_write import read_file


def left_panel(parent):
    panel_left = ttk.PanedWindow(parent)
    panel_right = ttk.PanedWindow(parent)
    all_img_button = tk.Button(panel_left, text='All images', relief='solid', activebackground='#F9FC77', cursor='hand2',
                               width=20, command=lambda: (right_panel(panel_right)))
    selected_button = tk.Button(panel_left, text='Selected images', relief='solid', activebackground='#F9FC77', cursor='hand2',
                                width=20, command=lambda: (right_panel1(panel_right)))
    tag_button = tk.Button(panel_left, text='Tags', relief='solid', activebackground='#F9FC77', cursor='hand2', width=20, command=lambda: (right_panel2(panel_right)))
    all_img_button.grid(column=0, row=1)
    selected_button.grid(column=0, row=2, pady=10)
    tag_button.grid(column=0, row=3)
    panel_left.pack(side="left")
    panel_right.pack()



def right_empty_panel(parent):
    panel_right_empty = ttk.PanedWindow(parent)
    panel_right_empty.pack()


def clean_panel(panel):
    [i.destroy() for i in panel.winfo_children()]


def right_panel(parent):
    clean_panel(parent)
    T = tk.Text(parent, width=40)
    file = open('text/text_allimg.txt', 'r')
    data = file.read()
    T.pack()
    T.insert(tk.END, data)
    T.configure(state='disabled', background='#F0F0F0', relief='solid', font=("Comic Sans", 10, "italic"))
    file.close()


def right_panel1(parent):
    clean_panel(parent)
    T = tk.Text(parent, width=40)
    file = open('text/text_selectimg.txt', 'r')
    data = file.read()
    T.pack()
    T.insert(tk.END, data) 
    T.configure(state='disabled', background='#F0F0F0', relief='solid',  font=("Comic Sans", 10, "italic"))
    file.close()

def right_panel2(parent):
    clean_panel(parent)
    T = tk.Text(parent, width=40)
    file = open('text/text_tags.txt', 'r')
    data = file.read()
    T.pack()
    T.insert(tk.END, data)
    T.configure(state='disabled', background='#F0F0F0', relief='solid',  font=("Comic Sans", 10, "italic"))
    file.close()



def main(parent):
    left_panel(parent)


#completare i testi
#sistemarli nella finestra di visualizzazione
