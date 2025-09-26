import struct

from src.sprite.chunk.chunk import Chunk
from src.enums import LayerType, BlendMode


class LayerChunk(Chunk):
    def __init__(self, frame, chunk_size: int, chunk_data: bytes):
        super().__init__(frame, chunk_size, chunk_data)

        self.uuid: int | None = None
        self.layer_name: str = ""
        self.layer_type: LayerType = LayerType.Unknown
        self.child_level: int = 0

        self.opacity: int = 0
        self.blend_mode: BlendMode = BlendMode.Unknown

        self.tileset_index: int | None = None

        self.default_width: int = 0
        self.default_height: int = 0

        self.flags: dict[str, bool] = {
            "is_visible": False,
            "is_editable": False,
            "is_movement_locked": False,
            "is_background_layer": False,
            "is_prefer_linked_cells": False,
            "is_layer_group_collapsed": False,
            "is_reference_layer": False,
        }

    def read(self):
        layer_name_length = struct.unpack("<i", self.chunk_data[16:18] + b"\x00\x00")[0]
        end_byte = 18 + layer_name_length
        self.layer_name = self.chunk_data[18:end_byte].decode("utf-8")
        self.layer_type = LayerType(
            struct.unpack("<i", self.chunk_data[2:4] + b"\x00\x00")[0]
        )
        self.child_level = struct.unpack("<i", self.chunk_data[4:6] + b"\x00\x00")[0]

        self.opacity = struct.unpack("<i", self.chunk_data[12:13] + b"\x00\x00\x00")[0]
        self.blend_mode = BlendMode(
            struct.unpack("<i", self.chunk_data[10:12] + b"\x00\x00")[0]
        )

        if self.layer_type == LayerType.Tilemap:
            self.tileset_index = struct.unpack(
                "<i", self.chunk_data[end_byte : end_byte + 4]
            )[0]
            end_byte += 4

        self.default_width = struct.unpack("<i", self.chunk_data[6:8] + b"\x00\x00")[0]
        self.default_height = struct.unpack("<i", self.chunk_data[8:10] + b"\x00\x00")[
            0
        ]

        if self.frame.aseprite_file.flags["layers_have_uuid"]:
            self.uuid = struct.unpack("<i", self.chunk_data[end_byte : end_byte + 16])[
                0
            ]

        flags = struct.unpack("<i", self.chunk_data[0:2] + b"\x00\x00")[0]
        self.flags["is_visible"] = bool(flags & 1)
        self.flags["is_editable"] = bool((flags >> 1) & 1)
        self.flags["is_movement_locked"] = bool((flags >> 2) & 1)
        self.flags["is_background_layer"] = bool((flags >> 3) & 1)
        self.flags["is_prefer_linked_cells"] = bool((flags >> 4) & 1)
        self.flags["is_layer_group_collapsed"] = bool((flags >> 5) & 1)
        self.flags["is_reference_layer"] = bool((flags >> 6) & 1)

        return self
