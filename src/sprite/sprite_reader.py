from io import BytesIO

from src.cel.cel import Cel
from src.cel.cel_reader import CelReader
from src.chunk.chunk import Chunk
from src.chunk.chunk_type import ChunkType
from src.color.color_depth import ColorDepth
from src.frame.frame import Frame
from src.frame.frame_header import frame_bytes_struct
from src.frame.frame_reader import FrameReader
from src.layer.layer import Layer
from src.layer.layer_reader import LayerReader
from src.layer.tilemap_layer import TilemapLayer
from src.palette.palette import Palette
from src.palette.palette_reader import PaletteReader
from src.slice.slice import Slice
from src.slice.slice_reader import SliceReader
from src.sprite.sprite import Sprite
from src.sprite.sprite_flags import SpriteFlags
from src.sprite.sprite_header import sprite_header_struct
from src.tag.tags_reader import TagsReader
from src.tag.tag import Tag
from src.tileset.tileset import Tileset
from src.tileset.tileset_reader import TilesetReader
from src.userdata.userdata import UserData
from src.userdata.userdata_reader import UserDataReader

class SpriteReader:
    def __init__(self, sprite_data: bytes) -> None:
        self.sprite_data: BytesIO = BytesIO(sprite_data)

        self.file_size: int = 0
        self.magic_number: int = 0
        self.num_frames: int = 0
        self.width: int = 0
        self.height: int = 0
        self.color_depth: ColorDepth = ColorDepth.Unknown
        self.flags: SpriteFlags = SpriteFlags.HasGrid
        self.speed: int = 0
        self.transparent_palette_entry_index: int = 0
        self.num_colors: int = 0
        self.pixel_width: int = 0
        self.pixel_height: int = 0
        self.grid_x: int = 0
        self.grid_y: int = 0
        self.grid_width: int = 0
        self.grid_height: int = 0

        self.palette: Palette = Palette()
        self.layers: list[Layer | TilemapLayer] = []
        self.tilesets: list[Tileset] = []
        self.slices: list[Slice] = []
        self.frames: list[Frame] = []
        self.tags: list[Tag] = []
        self.userdata: list[UserData] = []

    def read(self) -> None:
        self.read_header()
        self.read_frames()

    def read_header(self) -> None:
        header_data: bytes = self.sprite_data.read(sprite_header_struct.size)
        (
            self.file_size,
            self.magic_number,
            self.num_frames,
            self.width,
            self.height,
            color_depth,
            flags,
            self.speed,
            self.transparent_palette_entry_index,
            self.num_colors,
            self.pixel_width,
            self.pixel_height,
            self.grid_x,
            self.grid_y,
            self.grid_width,
            self.grid_height,
        ) = sprite_header_struct.unpack_from(header_data)

        if self.magic_number != 0xA5E0:
            raise ValueError(
                f"Incorrect sprite magic number, expected {0xA5E0}, got {self.magic_number}"
            )

        # Pixel ratio
        if self.pixel_width == 0 or self.pixel_height == 0:
            self.pixel_width = 1
            self.pixel_height = 1

        # Grid
        if self.grid_width == 0 and self.grid_height == 0:
            self.flags &= ~SpriteFlags.HasGrid

        # Colors
        self.color_depth = ColorDepth(color_depth)
        self.palette.resize(self.num_colors)
        self.palette.set_transparent_entry_index(self.transparent_palette_entry_index)

        # Flags
        self.flags |= flags

    def read_frames(self) -> None:
        for frame_num in range(0, self.num_frames):
            # Get size of frame data
            bytes_in_frame: int = frame_bytes_struct.unpack(
                self.sprite_data.read(frame_bytes_struct.size)
            )[0]
            self.sprite_data.seek(self.sprite_data.tell() - frame_bytes_struct.size)

            # Get frame data
            frame_data: BytesIO = BytesIO(self.sprite_data.read(bytes_in_frame))

            # Read frame
            frame_reader: FrameReader = FrameReader(frame_data, frame_num, self.speed)
            frame_reader.read()

            self.read_chunks(frame_reader, frame_reader.get_chunks())

            self.frames.append(frame_reader.to_frame())

    def read_chunks(self, frame_reader: FrameReader, chunks: list[Chunk]) -> None:
        # Track previously read data
        previous_chunk: Chunk | None = None
        previous_cel: Cel | None = None
        previous_tags: list[Tag] | None = None
        previous_tileset: Tileset | None = None

        # Read chunks
        for chunk in chunks:
            match chunk.type:
                # Layer Chunk (0x2004)
                case ChunkType.Layer:
                    layer_index: int = len(self.layers)
                    layers_have_uuid: bool = bool(
                        self.flags & SpriteFlags.LayersHaveUUID
                    )

                    # Read layer chunk
                    layer_reader: LayerReader = LayerReader(
                        chunk, layer_index, layers_have_uuid
                    )
                    layer_reader.read()

                    # Get as layer
                    layer: Layer | TilemapLayer | None = layer_reader.to_layer()
                    if layer:
                        self.layers.append(layer)

                # Cel Chunk (0x2005)
                case ChunkType.Cel:
                    # Read cel chunk
                    cel_reader: CelReader = CelReader(chunk, self.color_depth)
                    cel_reader.read()

                    # Get as cel
                    cel: Cel = cel_reader.to_cel()
                    frame_reader.add_cel(cel)
                    previous_cel = cel

                # Cel Extra Chunk (0x2006)

                # Color Profile Chunk (0x2007)

                # External Files Chunk (0x2008)

                # Mask Chunk (0x2016) DEPRECATED

                # Path Chunk (0x2017)

                # Tags Chunk (0x2018)
                case ChunkType.Tags:
                    tags_reader: TagsReader = TagsReader(chunk)
                    tags_reader.read()

                    # Get as tags
                    tags: list[Tag] = tags_reader.to_tags()
                    self.tags.extend(tags)
                    previous_tags = tags

                # Palette Chunk (0x2019), Old palette chunk (0x0004), Old palette chunk (0x0011)
                case (
                    ChunkType.Palette
                    | ChunkType.OldPalette
                    | ChunkType.EvenOlderPalette
                ):
                    palette_reader: PaletteReader = PaletteReader(chunk, self.palette)
                    palette_reader.read()

                # User Data Chunk (0x2020)
                case ChunkType.UserData:
                    userdata_reader: UserDataReader = UserDataReader(chunk)
                    userdata_reader.read()
                    userdata: UserData = userdata_reader.to_userdata()
                    self.userdata.append(userdata)

                # Slice Chunk (0x2022)
                case ChunkType.Slice:
                    # Read slice chunk
                    slice_reader: SliceReader = SliceReader(chunk)
                    slice_reader.read()

                    # Get as slice
                    sprite_slice: Slice = slice_reader.to_slice()
                    self.slices.append(sprite_slice)

                # Tileset Chunk (0x2023)
                case ChunkType.Tileset:
                    tileset_reader: TilesetReader = TilesetReader(
                        chunk, self.color_depth
                    )
                    tileset_reader.read()

                    # Get as tileset
                    tileset: Tileset = tileset_reader.to_tileset()
                    self.tilesets.append(tileset)
                    previous_tileset = tileset

                case _:
                    print(
                        f"Unhandled chunk in frame: #{frame_reader.frame_index}, of type: {chunk.type.name}"
                    )

            previous_chunk = chunk

    def to_sprite(self) -> Sprite:
        return Sprite(
            self.file_size,
            self.width,
            self.height,
            self.pixel_width,
            self.pixel_height,
            self.grid_x,
            self.grid_y,
            self.grid_width,
            self.grid_height,
            ColorDepth(self.color_depth),
            self.palette,
            self.layers,
            self.tilesets,
            self.slices,
            self.frames,
            self.speed,
            self.tags,
            self.flags,
        )
