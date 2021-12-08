from typing import List
import images


class Tag(set):
    def __init__(self, imgs: list) -> None:
        self.imgs: List[images.Img] = imgs

    def add(self, __object) -> None:
        print('addin', __object)
        return super().add(__object)

    def remove(self, __value):
        if __value not in self:
            return
        super().remove(__value)
        return self.image_remove_tag(__value)

    def rename(self, old_value, value):
        [img.update_tag(old_value, value) for img in self.imgs]
        self.add(value)
        super().remove(old_value)

    def image_remove_tag(self, tag: str):
        [img.remove_tag(tag) for img in self.imgs]
