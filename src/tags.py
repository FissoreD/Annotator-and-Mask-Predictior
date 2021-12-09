from typing import List
import images


class Tag(set):
    def __init__(self, imgs: list) -> None:
        self.imgs: List[images.Img] = imgs
        self.tag_panel = None

    def add(self, __object) -> None:
        temp = super().add(__object)
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
