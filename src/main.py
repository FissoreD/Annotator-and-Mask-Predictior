
import os
import shutil
import images as img
from typing import List
import tkinter as tk
import tags
from ttkthemes import ThemedTk
from sys import argv
from global_vars import *
from window import main_class


def main(themedMode=True):

    def delete(folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)

    def on_closing():
        folder_to_delete = [crop_dir, KERA_PRED_FOLDER]
        map(delete, folder_to_delete)
        root.destroy()
        return

    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs

    for j in img_list:
        j.set_tag_list(tag_list)

    root = ThemedTk() if themedMode else tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    main_class(tag_list, img_list, root)

    root.minsize(980, 500)
    root.mainloop()


if __name__ == '__main__':
    main(themedMode=(not ('-fast' in argv)))
