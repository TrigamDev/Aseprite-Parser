from io import BytesIO

from src.util import read_bytes


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

        pixel_index = read_bytes(read_pixel, 0, 1, "i")
        parsed_pixels.append(IndexedPixel(pixel_index))

    return parsed_pixels
