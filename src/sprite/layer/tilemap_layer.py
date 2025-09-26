import struct
from typing import Self

from src.sprite.layer.layer import Layer


class TilemapLayer(Layer):
    def __init__(self):
        super().__init__()
        self.tileset_index: int = 0

    def read_from_chunk(
        self, chunk_size: int, chunk_data: bytes, layers_have_uuid: bool
    ) -> Self:
        layer_name_length = struct.unpack("<i", chunk_data[16:18] + b"\x00\x00")[0]
        end_byte = 18 + layer_name_length

        self.tileset_index = struct.unpack("<i", chunk_data[end_byte : end_byte + 4])[0]
