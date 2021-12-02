import tkinter as tk


class annotator:
    def __init__(self, frm):
        self.frm = frm

    def openAnnotator(self):
        window = tk.TopLevel(self.frm)
        window.title("Annotator")
        window.geometry("200x200")


def main(frm):
    return annotator(frm).openAnnotator()
