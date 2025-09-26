import struct
import zlib
from typing import Self

import numpy

from src.sprite.tileset.tile import Tile, parse_tile_stream
from src.sprite.cel.cel import Cel


class TilesetCel(Cel):
    def __init__(self, sprite):
        super().__init__(sprite)

        self.tile_width: int = 0
        self.tile_height: int = 0

        self.tiles_array: list[list[Tile]] = []

    def __repr__(self):
        return f"TilesetCel({self.tile_width}x{self.tile_height})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)

        self.tile_width = struct.unpack("<i", chunk_data[16:18] + b"\x00\x00")[0]
        self.tile_height = struct.unpack("<i", chunk_data[18:20] + b"\x00\x00")[0]

        bits_per_tile = struct.unpack("<i", chunk_data[20:22] + b"\x00\x00")[0]
        tile_id_bitmask = struct.unpack("<i", chunk_data[22:26])[0]
        x_flip_bitmask = struct.unpack("<i", chunk_data[26:30])[0]
        y_flip_bitmask = struct.unpack("<i", chunk_data[30:34])[0]
        diagonal_flip_bitmask = struct.unpack("<i", chunk_data[34:38])[0]

        compressed_tiles_stream: bytes = chunk_data[48:chunk_size]
        tiles_stream = zlib.decompress(compressed_tiles_stream)

        tiles_list = parse_tile_stream(
            tiles_stream,
            bits_per_tile,
            tile_id_bitmask,
            x_flip_bitmask,
            y_flip_bitmask,
            diagonal_flip_bitmask,
        )

        tiles_array: list[list[Tile]] = numpy.reshape(
            tiles_list, (self.tile_width, self.tile_height)
        ).tolist()
        self.tiles_array = tiles_array

        return self
