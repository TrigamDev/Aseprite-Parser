import zlib
from typing import Self

import numpy

from src.tileset.tile import Tile, parse_tile_stream
from src.cel.cel import Cel
from src.util import read_bytes


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

        self.tile_width = read_bytes(chunk_data, 16, 2, "i")
        self.tile_height = read_bytes(chunk_data, 18, 2, "i")

        bits_per_tile = read_bytes(chunk_data, 20, 2, "i")
        tile_id_bitmask = read_bytes(chunk_data, 22, 4, "i")
        x_flip_bitmask = read_bytes(chunk_data, 26, 4, "i")
        y_flip_bitmask = read_bytes(chunk_data, 30, 4, "i")
        diagonal_flip_bitmask = read_bytes(chunk_data, 34, 4, "i")

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
