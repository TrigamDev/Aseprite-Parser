from PIL import Image

from src.cel.cel import Cel
from src.cel.cel_type import CelType
from src.color.pixel.pixel import Pixel
from src.color.color_depth import ColorDepth
from src.frame.frame import Frame
from src.utils.composite import apply_opacity


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
        pixel_data: bytes,
    ):
        super().__init__(cel_type, layer_index, x, y, opacity, z_index, color_depth)

        # Image cel
        self.width: int = width
        self.height: int = height
        self.pixels: list[list[Pixel]] = pixels
        self.pixel_data = pixel_data

    def __repr__(self):
        return f"ImageCel({self.width}x{self.height})"

    def render(self, frame: Frame) -> Image.Image:
        cel_image: Image.Image = Image.frombytes(
            "RGBA", (self.width, self.height), self.pixel_data
        )
        apply_opacity(cel_image, self.opacity)
        return cel_image
