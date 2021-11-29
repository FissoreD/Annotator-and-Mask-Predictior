from tkinter import ttk
import tkinter as tk


def create_scrollable_frame(root):
    c1 = ttk.Frame(root)
    c2 = ttk.Frame(c1)
    canvas = tk.Canvas(c2)
    vertBar = ttk.Scrollbar(
        c2, orient="vertical", command=canvas.yview)
    horBar = ttk.Scrollbar(
        c1, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=vertBar.set,
                     xscrollcommand=horBar.set)

    c2.pack(fill=tk.BOTH, expand=tk.YES)
    c1.pack(fill=tk.BOTH, expand=tk.YES)

    canvas.pack(side="left", fill="both", expand=True)
    vertBar.pack(side="right", fill="y")
    horBar.pack(side="bottom", fill="x")

    return scrollable_frame
