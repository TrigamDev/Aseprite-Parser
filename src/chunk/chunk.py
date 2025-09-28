from typing import Any

from src.chunk.chunk_type import ChunkType


chunk_header_format: str = (
    "<I"  # Chunk size
    + "H"  # Chunk type
)


class Chunk:
    def __init__(self, size: int, chunk_type: ChunkType, data: bytes) -> None:
        self.size: int = size
        self.type: ChunkType = chunk_type
        self.data: bytes = data

    def read(self) -> Any:
        pass
