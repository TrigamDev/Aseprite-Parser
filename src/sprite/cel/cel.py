import struct
from typing import Self

from src.sprite.cel.cel_type import CelType


class Cel:
    def __init__(self, sprite):
        self.sprite = sprite
        self.cel_type: CelType = CelType.Unknown
        self.layer_index: int = 0

        self.x: int = 0
        self.y: int = 0

        self.opacity: int = 0
        self.z_index: int = 0

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        self.layer_index = struct.unpack("<i", chunk_data[0:2] + b"\x00\x00")[0]

        self.x = struct.unpack("<i", chunk_data[2:4] + b"\x00\x00")[0]
        self.y = struct.unpack("<i", chunk_data[4:6] + b"\x00\x00")[0]

        self.opacity = struct.unpack("<i", chunk_data[6:7] + b"\x00\x00\x00")[0]
        self.z_index = struct.unpack("<i", chunk_data[9:11] + b"\x00\x00")[0]

        self.cel_type = CelType(struct.unpack("<i", chunk_data[7:9] + b"\x00\x00")[0])

        return self
