from pathlib import Path
import struct
from typing import Self

from src.sprite.color.color_depth import ColorDepth
from src.sprite.frame.frame import Frame
from src.sprite.layer.layer import Layer


class Sprite:
    def __init__(self):
        self.file_size: int = 0
        self.width: int = 0
        self.height: int = 0

        self.flags: dict[str, bool] = {
            "is_layer_opacity_valid": False,
            "is_layer_valid_for_groups": False,
            "layers_have_uuid": False,
        }

        self.color_depth: ColorDepth = ColorDepth.Unknown
        self.transparent_palette_index: int = 0
        self.number_of_colors: int = 0

        self.layers: list[Layer] = []
        self.frames: list[Frame] = []
        self.frame_speed: int = 0

        self.pixel_width: int = 0
        self.pixel_height: int = 0

        self.grid_x: int = 0
        self.grid_y: int = 0
        self.grid_width: int = 0
        self.grid_height: int = 0

    def read_from_path(self, path: Path) -> Self:
        with open(path, "rb") as aseprite_file:
            file_header = aseprite_file.read(128)

            self.file_size = struct.unpack("<i", file_header[0:4])[0]
            self.width = struct.unpack("<i", file_header[8:10] + b"\x00\x00")[0]
            self.height = struct.unpack("<i", file_header[10:12] + b"\x00\x00")[0]

            flags = struct.unpack("<i", file_header[14:18])[0]
            self.flags["is_layer_opacity_valid"] = bool(flags & 1)
            self.flags["is_layer_valid_for_groups"] = bool((flags >> 1) & 1)
            self.flags["layers_have_uuid"] = bool((flags >> 2) & 1)

            self.color_depth = ColorDepth(
                struct.unpack("<i", file_header[12:14] + b"\x00\x00")[0]
            )
            self.transparent_palette_index = struct.unpack(
                "<i", file_header[24:25] + b"\x00\x00\x00"
            )[0]
            self.number_of_colors = struct.unpack(
                "<i", file_header[28:30] + b"\x00\x00"
            )[0]
            if self.number_of_colors == 0:
                self.number_of_colors = 256

            self.frame_speed = struct.unpack("<i", file_header[18:20] + b"\x00\x00")[0]

            self.pixel_width = struct.unpack(
                "<i", file_header[30:31] + b"\x00\x00\x00"
            )[0]
            self.pixel_height = struct.unpack(
                "<i", file_header[31:32] + b"\x00\x00\x00"
            )[0]

            self.grid_x = struct.unpack("<i", file_header[32:34] + b"\x00\x00")[0]
            self.grid_y = struct.unpack("<i", file_header[34:36] + b"\x00\x00")[0]
            self.grid_width = struct.unpack("<i", file_header[36:38] + b"\x00\x00")[0]
            self.grid_height = struct.unpack("<i", file_header[38:40] + b"\x00\x00")[0]
            if self.grid_width == 0:
                self.grid_width = 16
            if self.grid_height == 0:
                self.grid_height = 16

            # Frames
            number_of_frames = struct.unpack("<i", file_header[6:8] + b"\x00\x00")[0]
            for frame in range(0, number_of_frames):
                Frame(self).read(aseprite_file)

            print(f"Frames: {self.frames}")
            print(f"Layers: {self.layers}")
        return self

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def add_frame(self, frame: Frame) -> None:
        self.frames.append(frame)
