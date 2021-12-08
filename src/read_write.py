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


def read_file(list_img: List[img.Img], file_name: str):
    with open("output.json") as fp:
        D = json.load(fp)
        for elt in D:
            img = find_image(elt[0], list_img)
            for tag_name in elt[1]:
                for coor in elt[1][tag_name]:
                    img.add_tag(tag_name, coor[0][0],
                                coor[0][1], coor[1][0], coor[1][1], None)


def write_file(list_img: List[img.Img], file_name: str):
    L = []
    for elt in list_img:
        L.append([elt.path, elt.tag_of_points])
    with open("output.json", "w") as fp:
        json.dump(L, fp)


if __name__ == '__main__':
    tag_list = tags.Tag(img.open_files())
    img_list = tag_list.imgs
    for i in img_list:
        i.set_tag_list(tag_list)
    # img_list[0].add_tag('tipo', 4, 5, 999, 888)
    # img_list[0].add_tag('tipo', 0, 2, 444, 555)
    # img_list[0].add_tag('tipo', 1000, 1000, 2000, 2000)
    # img_list[0].add_tag('t1', 0, 2, 333, 222)
    # img_list[1].add_tag('ffff', 0, 99, 111, 666)
    # write_file(img_list, "file_name")
    # tag_list.remove('tipo')
    # tag_list.remove('ffff')
    # tag_list.remove('t1')
    # read_file('file_name', img_list)
