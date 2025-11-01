from src.color.pixel.pixel import Pixel
from src.tileset.tileset_flags import TilesetFlags
from PIL import Image

tileset_chunk_header_size: int = 32


class Tileset:
    def __init__(
        self,
        tileset_id: int,
        num_tiles: int,
        tileset_name: str,
        tile_width: int,
        tile_height: int,
        base_index: int,
        flags: TilesetFlags,
        # External file
        external_file_id: int,
        tileset_id_in_external_file: int,
        external_tileset_pixels: list[list[Pixel]],
        pixeldata: bytes,
    ) -> None:
        self.tileset_id: int = tileset_id
        self.num_tiles: int = num_tiles
        self.tileset_name: str = tileset_name

        self.tile_width: int = tile_width
        self.tile_height: int = tile_height

        self.base_index: int = base_index

        self.flags: TilesetFlags = flags

        # External file
        self.external_file_id: int = external_file_id
        self.tileset_id_in_external_file: int = tileset_id_in_external_file
        self.external_tileset_pixels: list[list[Pixel]] = external_tileset_pixels
        self.pixeldata: bytes = pixeldata

    def __repr__(self) -> str:
        return f"Tileset({self.tileset_id}, {self.tileset_name})"

    def render(self) -> list[Image]:
        tiles: list[Image] = []
        bytes_per_tile = self.tile_width*self.tile_height*4
        for i in range(self.num_tiles):
            pixel_slice: bytes = self.pixeldata[bytes_per_tile*(i):bytes_per_tile*(i+1)]
            # TODO: determine mode
            tiles.append(Image.frombytes("RGBA", (self.tile_width, self.tile_height), pixel_slice))
        return tiles
