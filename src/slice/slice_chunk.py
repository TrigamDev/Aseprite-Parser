from src.chunk import chunk
from src.slice.slice import Slice


class SliceChunk(chunk.Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes) -> None:
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self) -> Slice:
        aseprite_slice: Slice = Slice()
        aseprite_slice.read_from_chunk(self.chunk_data)
        return aseprite_slice
