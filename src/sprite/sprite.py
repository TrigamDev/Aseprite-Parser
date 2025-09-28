from pathlib import Path
from typing import Self

from src.sprite.color.color_depth import ColorDepth
from src.sprite.frame.frame import Frame
from src.sprite.layer.layer import Layer
from src.sprite.palette.palette import Palette
from src.sprite.slice.slice import Slice
from src.sprite.tag.tag import Tag
from src.sprite.tileset.tileset import Tileset
from src.util import read_bytes, has_flag


sprite_header_size: int = 128


class Sprite:
    def __init__(self) -> None:
        self.file_size: int = 0
        self.width: int = 0
        self.height: int = 0

        self.flags: dict[str, bool] = {
            "is_layer_opacity_valid": False,
            "is_layer_valid_for_groups": False,
            "layers_have_uuid": False,
        }

        self.color_depth: ColorDepth = ColorDepth.Unknown
        self.palette: Palette = Palette()

        self.layers: list[Layer] = []
        self.frames: list[Frame] = []
        self.frame_speed: int = 0
        self.tags: list[Tag] = []
        self.tilesets: list[Tileset] = []
        self.slices: list[Slice] = []

        self.pixel_width: int = 0
        self.pixel_height: int = 0

        self.grid_x: int = 0
        self.grid_y: int = 0
        self.grid_width: int = 0
        self.grid_height: int = 0

    def read_from_path(self, path: Path) -> Self:
        with open(path, "rb") as aseprite_file:
            file_header = aseprite_file.read(sprite_header_size)

            self.file_size = read_bytes(file_header, 0, 4, "i")
            self.width = read_bytes(file_header, 8, 2, "i")
            self.height = read_bytes(file_header, 10, 2, "i")

            flags = read_bytes(file_header, 14, 4, "i")
            self.flags["is_layer_opacity_valid"] = has_flag(flags, 0)
            self.flags["is_layer_valid_for_groups"] = has_flag(flags, 1)
            self.flags["layers_have_uuid"] = has_flag(flags, 2)

            self.color_depth = ColorDepth(read_bytes(file_header, 12, 2, "i"))
            self.palette.set_transparent_index(read_bytes(file_header, 24, 1, "i"))
            number_of_colors = read_bytes(file_header, 28, 2, "i")
            if number_of_colors == 0:
                number_of_colors = 256
            self.palette.resize(number_of_colors)

            self.frame_speed = read_bytes(file_header, 18, 2, "i")

            self.pixel_width = read_bytes(file_header, 30, 1, "i")
            self.pixel_height = read_bytes(file_header, 31, 1, "i")

            self.grid_x = read_bytes(file_header, 32, 2, "i")
            self.grid_y = read_bytes(file_header, 34, 2, "i")
            self.grid_width = read_bytes(file_header, 36, 2, "i")
            self.grid_height = read_bytes(file_header, 38, 2, "i")
            if self.grid_width == 0:
                self.grid_width = 16
            if self.grid_height == 0:
                self.grid_height = 16

            # Frames
            number_of_frames = read_bytes(file_header, 6, 2, "i")
            for _ in range(0, number_of_frames):
                Frame(self).read(aseprite_file)

            print(f"Palette: {self.palette}")
            print(f"Frames: {self.frames}")
            print(f"Layers: {self.layers}")
            print(f"Tags: {self.tags}")
            print(f"Tilesets: {self.tilesets}")
            print(f"Slices: {self.slices}")
        return self

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)

    def add_frame(self, frame: Frame) -> None:
        self.frames.append(frame)
