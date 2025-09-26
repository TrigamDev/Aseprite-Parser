import struct
from typing import Self

from src.sprite.blend_mode import BlendMode
from src.sprite.layer.layer_type import LayerType


class Layer:
    def __init__(self, sprite):
        self.sprite = sprite

        self.uuid: int | None = None
        self.layer_name: str = ""
        self.layer_type: LayerType = LayerType.Unknown
        self.layer_index: int = len(self.sprite.layers)
        self.child_level: int = 0

        self.opacity: int = 0
        self.blend_mode: BlendMode = BlendMode.Unknown

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

    def __repr__(self):
        return f"Layer({self.layer_name}, {self.layer_index})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        layer_name_length = struct.unpack("<i", chunk_data[16:18] + b"\x00\x00")[0]
        end_byte = 18 + layer_name_length
        self.layer_name = chunk_data[18:end_byte].decode("utf-8")
        self.layer_type = LayerType(
            struct.unpack("<i", chunk_data[2:4] + b"\x00\x00")[0]
        )
        self.child_level = struct.unpack("<i", chunk_data[4:6] + b"\x00\x00")[0]

        self.opacity = struct.unpack("<i", chunk_data[12:13] + b"\x00\x00\x00")[0]
        self.blend_mode = BlendMode(
            struct.unpack("<i", chunk_data[10:12] + b"\x00\x00")[0]
        )

        self.default_width = struct.unpack("<i", chunk_data[6:8] + b"\x00\x00")[0]
        self.default_height = struct.unpack("<i", chunk_data[8:10] + b"\x00\x00")[0]

        flags = struct.unpack("<i", chunk_data[0:2] + b"\x00\x00")[0]
        self.flags["is_visible"] = bool(flags & 1)
        self.flags["is_editable"] = bool((flags >> 1) & 1)
        self.flags["is_movement_locked"] = bool((flags >> 2) & 1)
        self.flags["is_background_layer"] = bool((flags >> 3) & 1)
        self.flags["is_prefer_linked_cells"] = bool((flags >> 4) & 1)
        self.flags["is_layer_group_collapsed"] = bool((flags >> 5) & 1)
        self.flags["is_reference_layer"] = bool((flags >> 6) & 1)

        if self.sprite.flags["layers_have_uuid"]:
            self.uuid = struct.unpack(
                "<iiii", chunk_data[chunk_size - 16 : chunk_size]
            )[0]

        return self
