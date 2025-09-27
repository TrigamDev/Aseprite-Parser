from src.sprite.chunk.chunk import Chunk


class PaletteChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self):
        self.sprite.palette.read_from_chunk(self.chunk_size, self.chunk_data)
