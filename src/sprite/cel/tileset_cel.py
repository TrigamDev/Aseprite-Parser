from src.sprite.color.color_depth import ColorDepth
from src.sprite.tile import Tile
from src.sprite.cel.cel import Cel


class TilesetCel(Cel):
    def __init__(self, color_depth: ColorDepth):
        super().__init__(color_depth)

        self.tile_width: int = 0
        self.tile_height: int = 0

        self.tiles: list[Tile] = []
