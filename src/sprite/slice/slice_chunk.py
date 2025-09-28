from src.sprite.chunk import chunk
from src.sprite.slice.slice import Slice


class SliceChunk(chunk.Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self) -> None:
        aseprite_slice: Slice = Slice().read_from_chunk(
            self.chunk_size, self.chunk_data
        )
        self.sprite.slices.append(aseprite_slice)
