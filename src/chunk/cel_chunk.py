import struct

from src.chunk.aseprite_chunk import AsepriteChunk
from src.enums import CelType


class CelChunk(AsepriteChunk):
    def __init__(self, frame, chunk_size: int, chunk_data: bytes):
        AsepriteChunk.__init__(self, frame, chunk_size, chunk_data)

        self.cel_type: CelType = CelType.Unknown

    def read(self):
        layer_index = struct.unpack("<i", self.chunk_data[0:2] + b"\x00\x00")[0]

        cel_x = struct.unpack("<i", self.chunk_data[2:4] + b"\x00\x00")[0]
        cel_y = struct.unpack("<i", self.chunk_data[4:6] + b"\x00\x00")[0]

        opacity = struct.unpack("<i", self.chunk_data[6:7] + b"\x00\x00\x00")[0]
        z_index = struct.unpack("<i", self.chunk_data[9:11] + b"\x00\x00")[0]

        cel_type = CelType(struct.unpack("<i", self.chunk_data[7:9] + b"\x00\x00")[0])

        print(f"Layer index: {layer_index}")
        print(f"Cel x: {cel_x}, Cel y: {cel_y}")
        print(f"Opacity: {opacity}")
        print(f"Z index: {z_index}")
        print(f"Cel type: {cel_type.name}")
