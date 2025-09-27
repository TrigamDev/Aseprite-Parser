from typing import Self

from src.sprite.cel.cel import Cel
from src.util import read_bytes


class LinkedCel(Cel):
    def __init__(self, sprite):
        super().__init__(sprite)

        self.linked_frame: int = 0

    def __repr__(self):
        return f"LinkedCel({self.linked_frame})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)

        self.linked_frame = read_bytes(chunk_data, 16, 2, "i")

        return self
