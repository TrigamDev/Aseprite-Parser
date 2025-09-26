from typing import Self

from src.sprite.cel.cel import Cel


class LinkedCel(Cel):
    def __init__(self, sprite):
        super().__init__(sprite)

        self.linked_frame: int = 0

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)
        return self
