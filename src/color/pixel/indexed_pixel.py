from io import BytesIO

from src.color.pixel.pixel import Pixel
from src.util import read_bytes


class IndexedPixel(Pixel):
    def __init__(self, index: int) -> None:
        super().__init__()

        self.index = index

    def __repr__(self) -> str:
        return f"IndexedPixel({self.index})"

    # TODO: Implement logic for getting the RGBA value
    # of an indexed pixel
    def to_rgba(self) -> tuple[int, int, int, int]:
        return 255, 0, 0, 255


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
