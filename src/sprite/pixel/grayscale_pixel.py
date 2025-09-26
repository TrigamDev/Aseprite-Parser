import struct
from io import BytesIO


class GrayscalePixel:
    def __init__(self, value: int, alpha: int):
        self.value = value
        self.alpha = alpha

    def __repr__(self):
        return f"IndexedPixel({self.value}, {self.alpha})"


def parse_grayscale_pixel_stream(stream: bytes) -> list[GrayscalePixel]:
    parsed_pixels: list[GrayscalePixel] = []

    pixel_stream_reader = BytesIO(stream)
    while True:
        read_pixel = pixel_stream_reader.read(2)
        if len(read_pixel) == 0:
            break

        pixel_value = struct.unpack("<i", read_pixel[0:1] + b"\x00\x00\x00")[0]
        pixel_alpha = struct.unpack("<i", read_pixel[1:2] + b"\x00\x00\x00")[0]
        parsed_pixels.append(GrayscalePixel(pixel_value, pixel_alpha))

    return parsed_pixels
