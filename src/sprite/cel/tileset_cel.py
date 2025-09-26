from src.sprite.tile import Tile
from src.sprite.cel.cel import Cel


class TilesetCel(Cel):
    def __init__(self):
        super().__init__()

        self.tile_width: int = 0
        self.tile_height: int = 0

        self.tiles: list[Tile] = []
