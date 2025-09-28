import typing
import zlib
from typing import Self, Type

import numpy

from src.sprite.color.color_depth import ColorDepth
from src.sprite.color.pixel.grayscale_pixel import (
    GrayscalePixel,
    parse_grayscale_pixel_stream,
)
from src.sprite.color.pixel.indexed_pixel import (
    IndexedPixel,
    parse_indexed_pixel_stream,
)
from src.sprite.color.pixel.pixel import Pixel
from src.sprite.color.pixel.rgba_pixel import RGBAPixel, parse_rgba_pixel_stream
from src.util import (
    has_flag,
    read_bytes,
    read_string,
    string_byte_size,
    string_header_size,
)

tileset_chunk_header_size: int = 32


class Tileset:
    def __init__(self, sprite):
        self.sprite = sprite

        self.tileset_id: int = -1
        self.tileset_name: str = ""

        self.num_tiles: int = 0
        self.width: int = 0
        self.height: int = 0

        self.base_index: int = 1

        self.external_file_id: int = -1
        self.tileset_id_in_external_file: int = -1
        self.external_tileset_pixels: list[list[Pixel]]

        self.flags: dict[str, bool] = {
            "include_external_link": False,
            "include_external_tiles": False,
            "tilemaps_use_id_0_as_empty": False,
            "try_matching_tiles_with_horizontal_flip": False,
            "try_matching_tiles_with_vertical_flip": False,
            "try_matching_tiles_with_diagonal_flip": False,
        }

    def __repr__(self):
        return f"Tileset({self.tileset_id}, {self.tileset_name}, {self.width}x{self.height})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        self.tileset_id = read_bytes(chunk_data, 0, 4, "i")

        flags = read_bytes(chunk_data, 4, 4, "i")
        self.flags["include_external_link"] = has_flag(flags, 0)
        self.flags["include_external_tiles"] = has_flag(flags, 1)
        self.flags["tilemaps_use_id_0_as_empty"] = has_flag(flags, 2)
        self.flags["try_matching_tiles_with_horizontal_flip"] = has_flag(flags, 3)
        self.flags["try_matching_tiles_with_vertical_flip"] = has_flag(flags, 4)
        self.flags["try_matching_tiles_with_diagonal_flip"] = has_flag(flags, 5)

        self.num_tiles = read_bytes(chunk_data, 8, 4, "i")
        self.width = read_bytes(chunk_data, 12, 2, "i")
        self.height = read_bytes(chunk_data, 14, 2, "i")

        self.base_index = read_bytes(chunk_data, 16, 2, "i")

        self.tileset_name = read_string(chunk_data, 32)

        byte_offset: int = (
            tileset_chunk_header_size
            + string_byte_size(self.tileset_name)
            + string_header_size
        )

        if self.flags["include_external_link"]:
            self.external_file_id = read_bytes(chunk_data, byte_offset, 4, "i")
            self.tileset_id_in_external_file = read_bytes(
                chunk_data, byte_offset + 4, 4, "i"
            )
            byte_offset += 8

        if self.flags["include_external_tiles"]:
            compressed_tileset_image_length: int = read_bytes(
                chunk_data, byte_offset, 4, "i"
            )
            tileset_pixel_stream: bytes = zlib.decompress(
                chunk_data[
                    byte_offset + 4 : byte_offset + 4 + compressed_tileset_image_length
                ]
            )

            tileset_pixels_list: list[Pixel] = []
            match self.sprite.color_depth:
                case ColorDepth.Indexed:
                    tileset_pixels_list = parse_indexed_pixel_stream(
                        tileset_pixel_stream
                    )
                case ColorDepth.Grayscale:
                    tileset_pixels_list = parse_grayscale_pixel_stream(
                        tileset_pixel_stream
                    )
                case ColorDepth.RGBA:
                    tileset_pixels_list = parse_rgba_pixel_stream(tileset_pixel_stream)

            tileset_pixels_array: list[list[Pixel]] = numpy.reshape(
                tileset_pixels_list, (self.width, self.height * self.num_tiles)
            ).tolist()
            self.external_tileset_pixels = tileset_pixels_array

        return self
