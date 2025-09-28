from src.chunk.chunk import Chunk
from src.layer.layer import Layer
from src.layer.layer_type import LayerType
from src.layer.tilemap_layer import TilemapLayer
from src.util import read_bytes


class LayerChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)

        self.tileset_index: int | None = None

    def read(self) -> Layer | None:
        layer_type = LayerType(read_bytes(self.chunk_data, 2, 2, "i"))

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
