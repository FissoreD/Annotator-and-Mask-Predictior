"""
    A few list of "constant" variables used by others files
"""
from typing import List
from tags import Tag
import images as img

tag_list = Tag(img.open_files())
img_list = tag_list.imgs
for i in img_list:
    i.set_tag_list(tag_list)

if __name__ == '__main__':
    print(tag_list)
    print(img_list)
    tag_list.add('tipoff')
    print(tag_list)
    print(img_list)
    img_list[0].add_tag('tipo', 0, 2, 3, 7)
    print(tag_list)
    print(img_list)
    tag_list.rename('tipo', 'bb')
    print(tag_list)
    print(img_list)
    tag_list.remove('bb')
    print(tag_list)
    print(img_list)

"""
    TODO : 
        - sauvegarder un fichier en json (csv ?) avec les annotations 
        - ouvrir un fichier json ou ?csv:=pour les categories? pour pouvoir lire son contenu
        - penser à l'interface graphique
        - implèm interface graphique
        - base de données (100 images)
        - shapes qui se chevaucent avec ?shapely?
        - methode pour supprimer une shape de la liste de shapes d'une image
        - extraire les images en png ! (mandatory)
        - bonus : help panel, configuration du programme ...
        - shape limits : 
            [Area < 40 px] 
            [height > 5 px and width > 5 px] 
            [if A cover >= 20 % of other existing shape]
"""
