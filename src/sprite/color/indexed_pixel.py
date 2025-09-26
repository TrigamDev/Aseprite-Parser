import struct
from io import BytesIO


class IndexedPixel:
    def __init__(self, index: int):
        self.index = index

    def __repr__(self):
        return f"IndexedPixel({self.index})"


def parse_indexed_pixel_stream(stream: bytes) -> list[IndexedPixel]:
    parsed_pixels: list[IndexedPixel] = []

    pixel_stream_reader = BytesIO(stream)
    while True:
        read_pixel = pixel_stream_reader.read(1)
        if len(read_pixel) == 0:
            break

        pixel_index = struct.unpack("<i", read_pixel + b"\x00\x00\x00")[0]
        parsed_pixels.append(IndexedPixel(pixel_index))

    return parsed_pixels
