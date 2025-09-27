from typing import Self

from src.sprite.layer.layer import Layer, layer_name_byte_start
from src.util import read_bytes, string_byte_size, string_header_size


class TilemapLayer(Layer):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.tileset_index: int = 0

    def __repr__(self):
        return f"TilemapLayer({self.layer_index}, {self.layer_name})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)

        layer_name_length = string_byte_size(self.layer_name)
        tileset_byte_start = layer_name_byte_start + layer_name_length + string_header_size

        self.tileset_index = read_bytes(chunk_data, tileset_byte_start, 4, "i")

        return self
