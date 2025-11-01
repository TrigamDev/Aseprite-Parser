from src.cel.cel import Cel
from src.cel.cel_type import CelType
from src.color.pixel.pixel import Pixel
from src.color.color_depth import ColorDepth

class ImageCel(Cel):
    def __init__(
        self,
        cel_type: CelType,
        layer_index: int,
        x: int,
        y: int,
        width: int,
        height: int,
        opacity: int,
        z_index: int,
        color_depth: ColorDepth,
        pixels: list[list[Pixel]],
        pixeldata: bytes
    ):
        super().__init__(cel_type, layer_index, x, y, opacity, z_index, color_depth)

        # Image cel
        self.width: int = width
        self.height: int = height
        self.pixels: list[list[Pixel]] = pixels
        self.pixeldata = pixeldata

    def __repr__(self):
        return f"ImageCel({self.width}x{self.height})"
