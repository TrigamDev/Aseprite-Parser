from src.sprite.chunk.chunk import Chunk
from src.sprite.chunk.chunk_type import ChunkType


class PaletteChunk(Chunk):
    def __init__(self, sprite, chunk_type: ChunkType, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)
        self.chunk_type = chunk_type

    def read(self):
        match self.chunk_type:
            case ChunkType.Palette:
                self.sprite.palette.read_from_chunk(self.chunk_size, self.chunk_data)
            case ChunkType.OldPalette:
                self.sprite.palette.read_from_old_chunk(self.chunk_size, self.chunk_data)
            case ChunkType.EvenOlderPalette:
                self.sprite.palette.read_from_even_older_chunk(self.chunk_size, self.chunk_data)