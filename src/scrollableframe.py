from tkinter import ttk
import tkinter as tk


class create_scrollable_frame(ttk.Frame):
    """
        This class is created in order to have a scrollable frame.
        So scrollbar will be disposed on the rigth and bottom to the window, this is
        useful when the content of the window is large.
    """

    def __init__(self, master) -> None:
        c1 = ttk.Frame(master)
        c2 = ttk.Frame(c1)
        canvas = tk.Canvas(c2)
        super().__init__(canvas)
        vertBar = ttk.Scrollbar(
            c2, orient="vertical", command=canvas.yview)
        horBar = ttk.Scrollbar(
            c1, orient="horizontal", command=canvas.xview)

        self.bind(
            "<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(0, 0, window=self, anchor="nw")

        canvas.configure(yscrollcommand=vertBar.set,
                         xscrollcommand=horBar.set)

        c2.pack(fill=tk.BOTH, expand=tk.YES)
        c1.pack(fill=tk.BOTH, expand=tk.YES)

        canvas.pack(side="left", fill="both", expand=True)
        vertBar.pack(side="right", fill="y")
        horBar.pack(side="bottom", fill="x")
        self.canvas = canvas
        self.horBar = c2
