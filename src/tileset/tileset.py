from src.color.pixel.pixel import Pixel
from src.tileset.tileset_flags import TilesetFlags

tileset_chunk_header_size: int = 32


class Tileset:
    def __init__(
        self,
        tileset_id: int,
        tileset_name: str,
        tile_width: int,
        tile_height: int,
        base_index: int,
        flags: TilesetFlags,
        # External file
        external_file_id: int,
        tileset_id_in_external_file: int,
        external_tileset_pixels: list[list[Pixel]],
    ) -> None:
        self.tileset_id: int = tileset_id
        self.tileset_name: str = tileset_name

        self.tile_width: int = tile_width
        self.tile_height: int = tile_height

        self.base_index: int = base_index

        self.flags: TilesetFlags = flags

        # External file
        self.external_file_id: int = external_file_id
        self.tileset_id_in_external_file: int = tileset_id_in_external_file
        self.external_tileset_pixels: list[list[Pixel]] = external_tileset_pixels

    def __repr__(self) -> str:
        return f"Tileset({self.tileset_id}, {self.tileset_name})"