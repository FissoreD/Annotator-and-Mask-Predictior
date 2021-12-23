from typing import List
import images

""" 
    This class is a set which additionaly contains all the utilitary/useful methods about a Tags set 
    like when we rename a tag, we have to do it in 'cascade' for all annotations
"""


class Tag(set):
    def __init__(self, imgs: list) -> None:
        self.imgs: List[images.Img] = imgs
        self.tag_panel = None

    def add(self, __object) -> None:
        """ For standardization, we capitalize name when we add it """
        temp = super().add(__object.capitalize())
        self.refresh()
        return temp

    def remove(self, __value):
        if __value not in self:
            return
        super().remove(__value)
        temp = self.image_remove_tag(__value)
        self.refresh()
        return temp

    def rename(self, old_value, value):
        [img.update_tag(old_value, value) for img in self.imgs]
        self.add(value)
        super().remove(old_value)
        self.refresh()

    def image_remove_tag(self, tag: str):
        [img.remove_tag(tag) for img in self.imgs]

    def refresh(self):
        if self.tag_panel != None:
            self.tag_panel.all_tags()
