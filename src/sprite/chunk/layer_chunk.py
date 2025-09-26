import struct

from src.sprite.chunk.chunk import Chunk
from src.sprite.layer.layer import Layer
from src.sprite.layer.layer_type import LayerType
from src.sprite.layer.tilemap_layer import TilemapLayer


class LayerChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)

        self.tileset_index: int | None = None

    def read(self) -> Layer | None:
        layer_type = LayerType(
            struct.unpack("<i", self.chunk_data[2:4] + b"\x00\x00")[0]
        )

        match layer_type:
            case LayerType.Normal:
                return Layer(self.sprite).read_from_chunk(
                    self.chunk_size, self.chunk_data
                )
            case LayerType.Tilemap:
                return TilemapLayer(self.sprite).read_from_chunk(
                    self.chunk_size, self.chunk_data
                )
            case LayerType.Unknown | _:
                return None
