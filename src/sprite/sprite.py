from src.color.color_depth import ColorDepth
from src.frame.frame import Frame
from src.layer.layer import Layer
from src.palette.palette import Palette
from src.slice.slice import Slice
from src.sprite.sprite_flags import SpriteFlags
from src.tag.tag import Tag
from src.tileset.tileset import Tileset


class Sprite:
    def __init__(
        self,
        file_size: int,
        width: int,
        height: int,
        # Pixel ratio
        pixel_width: int,
        pixel_height: int,
        # Grid
        grid_x: int,
        grid_y: int,
        grid_width: int,
        grid_height: int,
        # Colors
        color_depth: ColorDepth,
        palette: Palette,
        # Layers
        layers: list[Layer],
        tilesets: list[Tileset],
        slices: list[Slice],
        # Frames
        frames: list[Frame],
        frame_duration: int,
        tags: list[Tag],
        # Flags
        flags: SpriteFlags,
    ) -> None:
        self.file_size: int = file_size

        self.width: int = width
        self.height: int = height

        # Pixel ratio
        self.pixel_width: int = pixel_width
        self.pixel_height: int = pixel_height

        # Grid
        self.grid_x: int = grid_x
        self.grid_y: int = grid_y
        self.grid_width: int = grid_width
        self.grid_height: int = grid_height

        # Colors
        self.color_depth: ColorDepth = color_depth
        self.palette: Palette = palette

        # Layers
        self.layers: list[Layer] = layers
        self.tilesets: list[Tileset] = tilesets
        self.slices: list[Slice] = slices

        # Frames
        self.frames: list[Frame] = frames
        self.frame_duration: int = frame_duration
        self.tags: list[Tag] = tags

        # Flags
        self.flags: SpriteFlags = flags

    def print(self) -> None:
        print(f"Palette: {self.palette}")
        print(f"Frames: {self.frames}")
        print(f"Layers: {self.layers}")
        # print(f"Tags: {self.tags}")
        # print(f"Tilesets: {self.tilesets}")
        # print(f"Slices: {self.slices}")
