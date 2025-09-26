import struct
from io import BytesIO


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

        pixel_red = struct.unpack("<i", read_pixel[0:1] + b"\x00\x00\x00")[0]
        pixel_green = struct.unpack("<i", read_pixel[1:2] + b"\x00\x00\x00")[0]
        pixel_blue = struct.unpack("<i", read_pixel[2:3] + b"\x00\x00\x00")[0]
        pixel_alpha = struct.unpack("<i", read_pixel[3:4] + b"\x00\x00\x00")[0]
        parsed_pixels.append(RGBAPixel(pixel_red, pixel_green, pixel_blue, pixel_alpha))

    return parsed_pixels
