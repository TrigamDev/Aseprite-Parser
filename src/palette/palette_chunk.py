from src.chunk.chunk import Chunk
from src.chunk.chunk_type import ChunkType


class PaletteChunk(Chunk):
    def __init__(
        self, sprite, chunk_type: ChunkType, chunk_size: int, chunk_data: bytes
    ) -> None:
        super().__init__(sprite, chunk_size, chunk_data)
        self.chunk_type = chunk_type

    def read(self) -> None:
        match self.chunk_type:
            case ChunkType.Palette:
                self.sprite.palette.read_from_chunk(self.chunk_data)
            case ChunkType.OldPalette | ChunkType.EvenOlderPalette:
                is_even_older_palette = self.chunk_type == ChunkType.EvenOlderPalette
                self.sprite.palette.read_from_old_chunk(
                    self.chunk_data, is_even_older_palette
                )
