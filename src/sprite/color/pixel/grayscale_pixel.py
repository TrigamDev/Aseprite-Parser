from io import BytesIO

from src.sprite.color.pixel.pixel import Pixel
from src.util import read_bytes


class GrayscalePixel(Pixel):
    def __init__(self, value: int, alpha: int) -> None:
        super().__init__()

        self.value = value
        self.alpha = alpha

    def __repr__(self) -> str:
        return f"GrayscalePixel({self.value}, {self.alpha})"

    def to_rgba(self) -> tuple[int, int, int, int]:
        return self.value, self.value, self.value, self.alpha


def parse_grayscale_pixel_stream(stream: bytes) -> list[GrayscalePixel]:
    parsed_pixels: list[GrayscalePixel] = []

    pixel_stream_reader = BytesIO(stream)
    while True:
        read_pixel = pixel_stream_reader.read(2)
        if len(read_pixel) == 0:
            break

        pixel_value = read_bytes(read_pixel, 0, 1, "i")
        pixel_alpha = read_bytes(read_pixel, 1, 1, "i")
        parsed_pixels.append(GrayscalePixel(pixel_value, pixel_alpha))

    return parsed_pixels
