from src.cel.cel import Cel
from src.cel.cel_type import CelType
from src.color.pixel.pixel import Pixel


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
        pixels: list[list[Pixel]],
    ):
        super().__init__(cel_type, layer_index, x, y, opacity, z_index)

        # Image cel
        self.width: int = width
        self.height: int = height

        self.pixels: list[list[Pixel]] = pixels

    def __repr__(self):
        return f"ImageCel({self.width}x{self.height})"
