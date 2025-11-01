from struct import Struct
from typing import Sequence
import zlib

import numpy

from src.chunk.chunk import Chunk
from src.color.color_depth import ColorDepth
from src.color.pixel.grayscale_pixel import parse_grayscale_pixel_stream
from src.color.pixel.indexed_pixel import parse_indexed_pixel_stream
from src.color.pixel.pixel import Pixel
from src.color.pixel.rgba_pixel import parse_rgba_pixel_stream
from src.tileset.tileset import Tileset
from src.tileset.tileset_flags import TilesetFlags
from src.util import read_string

tileset_chunk_format: str = (
    "<I"  # Tileset ID
    + "I"  # Tileset flags
    + "I"  # Number of tiles
    + "H"  # Tile width
    + "H"  # Tile height
    + "h"  # Base index
    + "14x"  # Reserved
)
tileset_chunk_struct: Struct = Struct(tileset_chunk_format)

external_file_format: str = (
    "<I"  # External file ID
    + "I"  # Tileset ID in external file
)
external_file_struct: Struct = Struct(external_file_format)

external_tileset_format: str = "<I"  # External tileset image length
external_tileset_struct: Struct = Struct(external_tileset_format)


class TilesetReader:
    def __init__(self, chunk: Chunk, color_depth: ColorDepth) -> None:
        self.chunk: Chunk = chunk
        self.color_depth: ColorDepth = color_depth

        self.tileset_id: int = -1
        self.tileset_flags: TilesetFlags = TilesetFlags(0)
        self.num_tiles: int = 0
        self.tile_width: int = 0
        self.tile_height: int = 0
        self.base_index: int = 0
        self.tileset_name: str = ""

        # External file
        self.external_file_id: int = -1
        self.external_tileset_id: int = -1

        # External tileset
        self.external_tileset_pixels: list[list[Pixel]] = []
        self.pixeldata: bytes

    def read(self) -> None:
        (
            self.tileset_id,
            tileset_flags,
            self.num_tiles,
            self.tile_width,
            self.tile_height,
            self.base_index,
        ) = tileset_chunk_struct.unpack(self.chunk.data.read(tileset_chunk_struct.size))

        self.tileset_flags = TilesetFlags(tileset_flags)

        self.tileset_name = read_string(self.chunk.data)

        if self.tileset_flags & TilesetFlags.LinksToExternalFile:
            (self.external_file_id, self.external_tileset_id) = (
                external_file_struct.unpack(
                    self.chunk.data.read(external_file_struct.size)
                )
            )

        if self.tileset_flags & TilesetFlags.IncludeTilesFromExternalFile:
            compressed_tileset_image_size: int = external_tileset_struct.unpack(
                self.chunk.data.read(external_tileset_struct.size)
            )[0]

            self.pixeldata: bytes = zlib.decompress(
                self.chunk.data.read(compressed_tileset_image_size)
            )

            # Parse pixels stream into 1D list
            pixels_list: Sequence[Pixel] = []
            match self.color_depth:
                case ColorDepth.Indexed:
                    pixels_list = parse_indexed_pixel_stream(self.pixeldata)
                case ColorDepth.Grayscale:
                    pixels_list = parse_grayscale_pixel_stream(self.pixeldata)
                case ColorDepth.RGBA:
                    pixels_list = parse_rgba_pixel_stream(self.pixeldata)

            # Reshape 1D list to 2D list
            pixels_array: list[list[Pixel]] = (
                numpy.asarray(pixels_list)
                .reshape((self.tile_width, self.tile_height * self.num_tiles))
                .tolist()
            )
            self.external_tileset_pixels = pixels_array

    def to_tileset(self) -> Tileset:
        return Tileset(
            self.tileset_id,
            self.num_tiles,
            self.tileset_name,
            self.tile_width,
            self.tile_height,
            self.base_index,
            self.tileset_flags,
            self.external_file_id,
            self.external_tileset_id,
            self.external_tileset_pixels,
            self.pixeldata
        )
