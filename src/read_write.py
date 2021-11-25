from typing import List
import images as img
import tags 
import json


"""
    file apri → open(nome file, modo lettura)
    tue operazioni
    devi sempre chiuderlo alla file .close()
    

"""
def read_file(file_name: str) -> List[img.Img]:
    return


def write_file(list_img : List[img.Img], file_name : str):
    return


tag_list = tags.Tag(img.open_files())
img_list = tag_list.imgs

print(tag_list, img_list)
