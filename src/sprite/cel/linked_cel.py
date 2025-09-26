from typing import Self

from src.sprite.cel.cel import Cel
from src.sprite.color.color_depth import ColorDepth


class LinkedCel(Cel):
    def __init__(self, color_depth: ColorDepth):
        super().__init__(color_depth)

        self.linked_frame: int = 0

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)
        return self
