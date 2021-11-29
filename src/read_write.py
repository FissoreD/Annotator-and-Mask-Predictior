from typing import List
import images as img
import tags
import json


"""
    file apri → open(nome file, modo lettura)
    tue operazioni
    devi sempre chiuderlo alla file .close()
    

"""


def find_image(img_path, list_img: List[img.Img]):
    for i in list_img:
        if img_path == i.path:
            return i


def read_file(file_name: str, list_img: List[img.Img]):

    with open("output.json") as fp:
        D = (json.load(fp))
        for elt in D:
            img = find_image(elt[0], list_img)
            for tag_name in elt[1]:
                print(tag_name, elt[1][tag_name])
                for coor in elt[1][tag_name]:
                    print(coor)
                    img.add_tag(tag_name, coor[0][0],
                                coor[0][1], coor[1][0], coor[1][1])


def write_file(list_img: List[img.Img], file_name: str):
    L = []
    for elt in list_img:
        L.append([elt.path, elt.tag])
    with open("output.json", "w") as fp:
        json.dump(L, fp)


if __name__ == '__main__':
    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs
    img_list[0].add_tag('tipo', 0, 2, 3, 7)
    img_list[0].add_tag('tipo', 0, 2, 999, 7)
    img_list[5].add_tag('ffff', 0, 99, 3, 7)
    print(write_file(img_list, "file_name"))
    tag_list.remove('tipo')
    tag_list.remove('ffff')
    print(img_list)
    print(read_file('file_name', img_list))
