from src.aseprite_pixel import IndexedPixel, GrayscalePixel, RGBAPixel
from src.cel.aseprite_cel import AsepriteCel


class RawImageCel(AsepriteCel):
    def __init__(self):
        super().__init__()

        self.width: int = 0
        self.height: int = 0

        self.pixels: list[IndexedPixel | GrayscalePixel | RGBAPixel] = []
