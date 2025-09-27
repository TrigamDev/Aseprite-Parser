from typing import Self

from src.sprite.layer.layer import Layer
from src.util import read_bytes


class TilemapLayer(Layer):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.tileset_index: int = 0

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)

        layer_name_length = read_bytes(chunk_data, 16, 2, "i")
        end_byte = 18 + layer_name_length

        self.tileset_index = read_bytes(chunk_data, end_byte, 4, "i")

        return self
