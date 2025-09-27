from typing import Self

from src.sprite.blend_mode import BlendMode
from src.sprite.layer.layer_type import LayerType
from src.util import read_string, read_bytes, has_flag

layer_name_byte_start: int = 16
uuid_byte_size: int = 16


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
        return f"Layer({self.layer_index}, {self.layer_name})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        self.layer_name = read_string(chunk_data, layer_name_byte_start)
        self.layer_type = LayerType(read_bytes(chunk_data, 2, 2, "i"))
        self.child_level = read_bytes(chunk_data, 4, 2, "i")

        self.opacity = read_bytes(chunk_data, 12, 1, "i")
        self.blend_mode = BlendMode(read_bytes(chunk_data, 10, 2, "i"))

        self.default_width = read_bytes(chunk_data, 6, 2, "i")
        self.default_height = read_bytes(chunk_data, 8, 2, "i")

        flags = read_bytes(chunk_data, 0, 2, "i")
        self.flags["is_visible"] = has_flag(flags, 0)
        self.flags["is_editable"] = has_flag(flags, 1)
        self.flags["is_movement_locked"] = has_flag(flags, 2)
        self.flags["is_background_layer"] = has_flag(flags, 3)
        self.flags["is_prefer_linked_cells"] = has_flag(flags, 4)
        self.flags["is_layer_group_collapsed"] = has_flag(flags, 5)
        self.flags["is_reference_layer"] = has_flag(flags, 6)

        if self.sprite.flags["layers_have_uuid"]:
            self.uuid = read_bytes(
                chunk_data, chunk_size - uuid_byte_size, uuid_byte_size, "i"
            )

        return self
