from io import BytesIO

from src.util import read_bytes


class Tile:
    def __init__(self):
        self.tile_id: int = 0
        self.is_horizontally_flipped: bool = False
        self.is_vertically_flipped: bool = False
        self.is_diagonally_flipped: bool = False

    def __repr__(self):
        return f"Tile({self.tile_id})"


def parse_tile_stream(
    stream: bytes,
    bits_per_tile: int,
    tile_id_bitmask: int,
    x_flip_bitmask: int,
    y_flip_bitmask: int,
    diagonal_flip_bitmask: int,
) -> list[Tile]:
    parsed_tiles: list[Tile] = []

    tile_stream_reader = BytesIO(stream)
    while True:
        bytes_per_tile: int = int(bits_per_tile / 8)
        tile_bytes: bytes = tile_stream_reader.read(bytes_per_tile)

        if len(tile_bytes) == 0:
            break
        elif len(tile_bytes) < bytes_per_tile:
            tile_bytes += b"\x00" * (bytes_per_tile - len(tile_bytes))

        read_tile = read_bytes(tile_bytes, 0, bytes_per_tile, "i")

        tile: Tile = Tile()
        tile.tile_id = read_tile & tile_id_bitmask
        tile.is_horizontally_flipped = bool(read_tile & x_flip_bitmask)
        tile.is_vertically_flipped = bool(read_tile & y_flip_bitmask)
        tile.is_diagonally_flipped = bool(read_tile & diagonal_flip_bitmask)

        parsed_tiles.append(tile)

    return parsed_tiles
