from PIL import Image
from src.cel.cel_type import CelType
from src.frame.frame import Frame
from src.tileset.tile import Tile
from src.cel.cel import Cel
from src.color.color_depth import ColorDepth


class TilemapCel(Cel):
    def __init__(
        self,
        cel_type: CelType,
        layer_index: int,
        x: int,
        y: int,
        tile_width: int,
        tile_height: int,
        opacity: int,
        z_index: int,
        color_depth: ColorDepth,
        tiles: list[list[Tile]],
    ):
        super().__init__(cel_type, layer_index, x, y, opacity, z_index, color_depth)

        self.tile_width: int = tile_width
        self.tile_height: int = tile_height

        self.tiles_array: list[list[Tile]] = tiles

    def __repr__(self):
        return f"TilemapCel({self.tile_width}x{self.tile_height})"

    def render(self, frame: Frame) -> Image.Image:
        raise NotImplementedError()
