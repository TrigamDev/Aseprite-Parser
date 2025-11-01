from src.color.color_depth import ColorDepth
from src.cel.cel_type import CelType
from src.frame.frame import Frame
from src.layer.layer import Layer
from src.palette.palette import Palette
from src.slice.slice import Slice
from src.sprite.sprite_flags import SpriteFlags
from src.tag.tag import Tag
from src.tileset.tileset import Tileset
from src.layer.layer_flags import LayerFlags
from src.layer.layer_type import LayerType
from PIL import Image

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

    class Target:
        def __init__(self, image: Image, pos: tuple[int, int]):
            self.image: Image = image
            self.pos: tuple[int, int] = pos

    def render(self) -> list[Image]:
        frames: dict[int, dict[int, self.Target]] = {}
        for frame in self.frames:
            targets: dict[int, self.Target] = {}
            for cel in frame.cels:
                match cel.cel_type:
                    case CelType.RawImageData | CelType.CompressedImage:
                        match cel.color_depth:
                            case ColorDepth.Indexed:
                                img = Image.frombytes("P", (cel.width, cel.height), cel.pixeldata)
                                arr = self.palette.packed_array
                                if len(self.palette.packed_array) > 256*4:
                                    arr = arr[:256*4]
                                if not self.layers[cel.layer_index].flags & LayerFlags.Background:
                                    for i in range(4):
                                        arr[i] = 0
                                img.putpalette(data=arr, rawmode="RGBA")
                                if cel.opacity < 256:
                                    img.putalpha(cel.opacity)
                                targets[cel.layer_index] = self.Target(img, (cel.x, cel.y))

                            case ColorDepth.Grayscale:
                                pass

                            case ColorDepth.RGBA:
                                img = Image.frombytes("RGBA", (cel.width, cel.height), cel.pixeldata)
                                if cel.opacity < 256:
                                    img.putalpha(cel.opacity)
                                targets[cel.layer_index] = self.Target(img, (cel.x, cel.y))

                    case CelType.CompressedTilemap:
                        img: Image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
                        layer = self.layers[cel.layer_index]
                        if layer.layer_type & LayerType.Tilemap:
                            tileset: Tileset = self.tilesets[layer.tileset_index]
                            tiles: list[Image] = tileset.render()
                            for y, row in enumerate(cel.tiles_array):
                                for x, tile in enumerate(row):
                                    pos = (y*tileset.tile_height, x*tileset.tile_width)
                                    img.alpha_composite(tiles[tile.tile_id], dest=pos)
                        targets[cel.layer_index] = self.Target(img, (0, 0))

                    case CelType.LinkedCel:
                        # triangulate cel based on frame and layer
                        linked_target: self.Target = frames[cel.linked_frame_index][cel.layer_index]
                        targets[cel.layer_index] = self.Target(linked_target.image, (cel.x, cel.y))

            frames[frame.frame_index] = targets
        # compose frames
        frame_imgs: list[Image] = []
        for i in range(len(frames)):
            frame_img: Image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
            for target in frames[i].values():
                frame_img.paste(target.image, box=target.pos)
            frame_imgs.append(frame_img)
        return frame_imgs

    def print(self) -> None:
        print(f"Palette: {self.palette}")
        print(f"Frames: {self.frames}")
        print(f"Layers: {self.layers}")
        print(f"Tags: {self.tags}")
        print(f"Tilesets: {self.tilesets}")
        print(f"Slices: {self.slices}")
