from src.sprite.cel.cel import Cel


class LinkedCel(Cel):
    def __init__(self):
        super().__init__()

        self.linked_frame: int = 0

    def set_linked_frame(self, linked_frame: int):
        self.linked_frame = linked_frame
