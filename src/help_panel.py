import tkinter as tk


def main(parent):
    panel = tk.PanedWindow(parent)
    b = tk.Entry(panel, text='test')
    b.pack()
    panel.pack()
    return
