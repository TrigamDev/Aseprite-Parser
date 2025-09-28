from src.sprite.chunk.chunk import Chunk
from src.sprite.tileset.tileset import Tileset


class TilesetChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self):
        tileset: Tileset = Tileset(self.sprite)
        tileset.read_from_chunk(self.chunk_size, self.chunk_data)
        self.sprite.tilesets.append(tileset)
