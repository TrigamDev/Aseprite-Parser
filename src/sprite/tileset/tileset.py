from typing import Self

from src.util import has_flag, read_bytes, read_string


class Tileset:
    def __init__(self):
        self.tileset_id: int = -1
        self.tileset_name: str = ""

        self.num_tiles: int = 0
        self.width: int = 0
        self.height: int = 0

        self.base_index: int = 1

        self.flags: dict[str, bool] = {
            "include_external_link": False,
            "include_external_tiles": False,
            "tilemaps_use_id_0_as_empty": False,
            "try_matching_tiles_with_horizontal_flip": False,
            "try_matching_tiles_with_vertical_flip": False,
            "try_matching_tiles_with_diagonal_flip": False,
        }

    def __repr__(self):
        return f"Tileset({self.tileset_id}, {self.tileset_name}, {self.width}x{self.height})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        self.tileset_id = read_bytes(chunk_data, 0, 4, "i")

        flags = read_bytes(chunk_data, 4, 4, "i")
        self.flags["include_external_link"] = has_flag(flags, 0)
        self.flags["include_external_tiles"] = has_flag(flags, 1)
        self.flags["tilemaps_use_id_0_as_empty"] = has_flag(flags, 2)
        self.flags["try_matching_tiles_with_horizontal_flip"] = has_flag(flags, 3)
        self.flags["try_matching_tiles_with_vertical_flip"] = has_flag(flags, 4)
        self.flags["try_matching_tiles_with_diagonal_flip"] = has_flag(flags, 5)

        self.num_tiles = read_bytes(chunk_data, 8, 4, "i")
        self.width = read_bytes(chunk_data, 12, 2, "i")
        self.height = read_bytes(chunk_data, 14, 2, "i")

        self.base_index = read_bytes(chunk_data, 16, 2, "i")

        self.tileset_name = read_string(chunk_data, 32)

        return self