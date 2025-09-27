import zlib
from typing import Self

import numpy

from src.sprite.cel.cel import Cel
from src.sprite.cel.cel_type import CelType
from src.sprite.color.grayscale_pixel import (
    GrayscalePixel,
    parse_grayscale_pixel_stream,
)
from src.sprite.color.indexed_pixel import IndexedPixel, parse_indexed_pixel_stream
from src.sprite.color.rgba_pixel import RGBAPixel, parse_rgba_pixel_stream
from src.sprite.sprite import ColorDepth
from src.util import read_bytes


class ImageCel(Cel):
    def __init__(self, sprite):
        super().__init__(sprite)

        self.width: int = 0
        self.height: int = 0

        self.pixels: list[list[IndexedPixel | GrayscalePixel | RGBAPixel]] = []

    def __repr__(self):
        return f"ImageCel({self.width}x{self.height})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        super().read_from_chunk(chunk_size, chunk_data)

        self.width = read_bytes(chunk_data, 16, 2, "i")
        self.height = read_bytes(chunk_data, 18, 2, "i")

        pixels_stream: bytes = chunk_data[20:chunk_size]
        if self.cel_type == CelType.CompressedImage:
            pixels_stream = zlib.decompress(pixels_stream)

        pixels_list: list[IndexedPixel | GrayscalePixel | RGBAPixel] = []
        match self.sprite.color_depth:
            case ColorDepth.Indexed:
                pixels_list = parse_indexed_pixel_stream(pixels_stream)
            case ColorDepth.Grayscale:
                pixels_list = parse_grayscale_pixel_stream(pixels_stream)
            case ColorDepth.RGBA:
                pixels_list = parse_rgba_pixel_stream(pixels_stream)

        pixels_array: list[list[IndexedPixel | GrayscalePixel | RGBAPixel]] = (
            numpy.reshape(pixels_list, (self.width, self.height)).tolist()
        )
        self.pixels = pixels_array

        return self
