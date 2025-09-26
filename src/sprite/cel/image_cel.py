from src.sprite.cel.cel import Cel
from src.sprite.pixel.grayscale_pixel import GrayscalePixel
from src.sprite.pixel.indexed_pixel import IndexedPixel
from src.sprite.pixel.rgba_pixel import RGBAPixel


class ImageCel(Cel):
    def __init__(self):
        super().__init__()

        self.width: int = 0
        self.height: int = 0

        self.pixels: list[list[IndexedPixel | GrayscalePixel | RGBAPixel]] = []

    def set_width(self, width: int):
        self.width = width

    def set_height(self, height: int):
        self.height = height

    def set_pixels(self, pixels: list[list[IndexedPixel | GrayscalePixel | RGBAPixel]]):
        self.pixels = pixels
