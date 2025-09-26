import struct
import zlib

import numpy

from src.sprite.cel.image_cel import ImageCel
from src.sprite.chunk.chunk import Chunk
from src.enums import CelType, ColorDepth
from src.sprite.pixel.grayscale_pixel import GrayscalePixel, parse_grayscale_pixel_stream
from src.sprite.pixel.indexed_pixel import parse_indexed_pixel_stream, IndexedPixel
from src.sprite.pixel.rgba_pixel import RGBAPixel, parse_rgba_pixel_stream


class CelChunk(Chunk):
    def __init__(self, frame, chunk_size: int, chunk_data: bytes):
        super().__init__(frame, chunk_size, chunk_data)

        self.cel_type: CelType = CelType.Unknown

        self.layer_index: int = 0

        self.cel_x: int = 0
        self.cel_y: int = 0

        self.opacity: int = 0
        self.z_index: int = 0

    def read(self):
        self.layer_index = struct.unpack("<i", self.chunk_data[0:2] + b"\x00\x00")[0]

        self.cel_x = struct.unpack("<i", self.chunk_data[2:4] + b"\x00\x00")[0]
        self.cel_y = struct.unpack("<i", self.chunk_data[4:6] + b"\x00\x00")[0]

        self.opacity = struct.unpack("<i", self.chunk_data[6:7] + b"\x00\x00\x00")[0]
        self.z_index = struct.unpack("<i", self.chunk_data[9:11] + b"\x00\x00")[0]

        self.cel_type = CelType(
            struct.unpack("<i", self.chunk_data[7:9] + b"\x00\x00")[0]
        )

        match self.cel_type:
            case CelType.CompressedImage:
                self.read_compressed_image_cel()

        print(f"Cel x: {self.cel_x}, Cel y: {self.cel_y}")
        print(f"Cel type: {self.cel_type.name}")

    def read_compressed_image_cel(self) -> ImageCel:
        width = struct.unpack("<i", self.chunk_data[16:18] + b"\x00\x00")[0]
        height = struct.unpack("<i", self.chunk_data[18:20] + b"\x00\x00")[0]

        compressed_pixels_stream: bytes = self.chunk_data[20 : self.chunk_size]
        uncompressed_pixels_stream = zlib.decompress(compressed_pixels_stream)

        pixels_list: list[IndexedPixel | GrayscalePixel | RGBAPixel] = []
        match self.frame.aseprite_file.color_depth:
            case ColorDepth.Indexed:
                pixels_list = parse_indexed_pixel_stream(uncompressed_pixels_stream)
            case ColorDepth.Grayscale:
                pixels_list = parse_grayscale_pixel_stream(uncompressed_pixels_stream)
            case ColorDepth.RGBA:
                pixels_list = parse_rgba_pixel_stream(uncompressed_pixels_stream)

        pixels_array: list[list[IndexedPixel | GrayscalePixel | RGBAPixel]] = (
            numpy.reshape(pixels_list, (width, height)).tolist()
        )

        image_cel = ImageCel()
        image_cel.set_layer_index(self.layer_index)

        image_cel.set_x(self.cel_x)
        image_cel.set_y(self.cel_y)
        image_cel.set_width(width)
        image_cel.set_height(height)

        image_cel.set_opacity(self.opacity)
        image_cel.set_z_index(self.z_index)

        image_cel.set_pixels(pixels_array)

        return image_cel