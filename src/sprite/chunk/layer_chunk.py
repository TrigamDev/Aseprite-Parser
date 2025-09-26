import struct

from src.sprite.chunk.chunk import Chunk
from src.sprite.layer.layer import Layer
from src.sprite.layer.layer_type import LayerType
from src.sprite.layer.tilemap_layer import TilemapLayer


class LayerChunk(Chunk):
    def __init__(self, frame, chunk_size: int, chunk_data: bytes):
        super().__init__(frame, chunk_size, chunk_data)

        self.tileset_index: int | None = None

    def read(self) -> Layer | None:
        layer_type = LayerType(
            struct.unpack("<i", self.chunk_data[2:4] + b"\x00\x00")[0]
        )

        match layer_type:
            case LayerType.Normal:
                return Layer().read_from_chunk(
                    self.chunk_size,
                    self.chunk_data,
                    self.frame.sprite.flags["layers_have_uuid"],
                )
            case LayerType.Tilemap:
                return TilemapLayer().read_from_chunk(
                    self.chunk_size,
                    self.chunk_data,
                    self.frame.sprite.flags["layers_have_uuid"],
                )
            case LayerType.Unknown | _:
                return None
