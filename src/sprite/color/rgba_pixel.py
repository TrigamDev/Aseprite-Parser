from io import BytesIO

from src.util import read_bytes


class RGBAPixel:
    def __init__(self, red: int, green: int, blue: int, alpha: int):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __repr__(self):
        return f"RGBAPixel({self.red}, {self.green}, {self.blue}, {self.alpha})"


def parse_rgba_pixel_stream(stream: bytes) -> list[RGBAPixel]:
    parsed_pixels: list[RGBAPixel] = []

    pixel_stream_reader = BytesIO(stream)
    while True:
        read_pixel = pixel_stream_reader.read(4)
        if len(read_pixel) == 0:
            break

        pixel_red = read_bytes(read_pixel, 0, 1, "i")
        pixel_green = read_bytes(read_pixel, 1, 1, "i")
        pixel_blue = read_bytes(read_pixel, 2, 1, "i")
        pixel_alpha = read_bytes(read_pixel, 3, 1, "i")
        parsed_pixels.append(RGBAPixel(pixel_red, pixel_green, pixel_blue, pixel_alpha))

    return parsed_pixels
