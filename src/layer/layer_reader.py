from struct import Struct
from src.chunk.chunk import Chunk
from src.layer.blend_mode import BlendMode
from src.layer.layer import Layer
from src.layer.layer_flags import LayerFlags
from src.layer.layer_type import LayerType
from src.layer.tilemap_layer import TilemapLayer
from src.util import read_string

layer_chunk_format: str = (
    "<H"  # Flags
    + "H"  # Layer type
    + "H"  # Layer child level
    + "H"  # Default layer width (pixels)
    + "H"  # Default layer height (pixels)
    + "H"  # Blend mode
    + "B"  # Opacity
    + "3x"  # For future
)
tilemap_layer_chunk_format: str = "<I"
layer_chunk_uuid_format: str = "<QQ"


class LayerReader:
    def __init__(self, chunk: Chunk, layer_index: int, layers_have_uuid: bool):
        self.chunk: Chunk = chunk
        self.layer_index: int = layer_index
        self.layers_have_uuid: bool = layers_have_uuid

        self.flags: LayerFlags = LayerFlags(0)
        self.layer_type: LayerType = LayerType.Unknown
        self.layer_child_level: int = 0
        self.default_layer_width: int = 0
        self.default_layer_height: int = 0
        self.blend_mode: BlendMode = BlendMode.Unknown
        self.opacity: int = 0
        self.layer_name: str = ""

        self.tileset_index: int = 0

        self.uuid: int | None = None

    def read(self) -> None:
        layer_chunk_struct: Struct = Struct(layer_chunk_format)
        (
            flags,
            layer_type,
            self.layer_child_level,
            self.default_layer_width,
            self.default_layer_height,
            blend_mode,
            self.opacity,
        ) = layer_chunk_struct.unpack(self.chunk.data.read(layer_chunk_struct.size))

        self.flags |= flags
        self.layer_type = LayerType(layer_type)
        self.blend_mode = BlendMode(blend_mode)

        self.layer_name = read_string(self.chunk.data)

        # Get tileset index, if layer is a tilemap layer
        if self.layer_type is LayerType.Tilemap:
            tilemap_layer_chunk_struct: Struct = Struct(tilemap_layer_chunk_format)

            self.tileset_index = tilemap_layer_chunk_struct.unpack(
                self.chunk.data.read(tilemap_layer_chunk_struct.size)
            )[0]

        # Get layer UUID, if layers have UUIDs
        if self.layers_have_uuid:
            layer_chunk_uuid_struct: Struct = Struct(layer_chunk_uuid_format)

            self.uuid = layer_chunk_uuid_struct.unpack(
                self.chunk.data.read(layer_chunk_uuid_struct.size)
            )[0]

    def to_layer(self) -> Layer | TilemapLayer | None:
        match self.layer_type:
            case LayerType.Normal:
                return Layer(
                    self.uuid,
                    self.layer_name,
                    self.layer_type,
                    self.layer_index,
                    self.layer_child_level,
                    self.default_layer_width,
                    self.default_layer_height,
                    self.opacity,
                    self.blend_mode,
                    self.flags,
                )
            case LayerType.Tilemap:
                return TilemapLayer(
                    self.uuid,
                    self.layer_name,
                    self.layer_type,
                    self.layer_index,
                    self.layer_child_level,
                    self.default_layer_width,
                    self.default_layer_height,
                    self.opacity,
                    self.blend_mode,
                    self.tileset_index,
                    self.flags,
                )
            case _:
                return None
