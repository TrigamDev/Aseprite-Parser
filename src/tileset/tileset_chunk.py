from src.chunk.chunk import Chunk
from src.tileset.tileset import Tileset


class TilesetChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes) -> None:
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self) -> Tileset:
        tileset: Tileset = Tileset(self.sprite)
        tileset.read_from_chunk(self.chunk_data)
        return tileset
