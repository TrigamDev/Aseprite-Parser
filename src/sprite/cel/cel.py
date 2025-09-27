from typing import Self

from src.sprite.cel.cel_type import CelType
from src.util import read_bytes


class Cel:
    def __init__(self, sprite):
        self.sprite = sprite
        self.cel_type: CelType = CelType.Unknown
        self.layer_index: int = 0

        self.x: int = 0
        self.y: int = 0

        self.opacity: int = 0
        self.z_index: int = 0

    def __repr__(self):
        return f"Cel({self.layer_index})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        self.layer_index = read_bytes(chunk_data, 0, 2, "i")

        self.x = read_bytes(chunk_data, 2, 2, "i")
        self.y = read_bytes(chunk_data, 4, 2, "i")

        self.opacity = read_bytes(chunk_data, 6, 1, "i")
        self.z_index = read_bytes(chunk_data, 9, 2, "i")

        self.cel_type = CelType(read_bytes(chunk_data, 7, 2, "i"))

        return self
