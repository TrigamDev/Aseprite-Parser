from io import BytesIO
from struct import Struct

from src.cel.cel import Cel
from src.chunk.chunk import Chunk, chunk_header_format
from src.chunk.chunk_type import ChunkType
from src.frame.frame import Frame
from src.frame.frame_header import frame_header_size, frame_header_struct


class FrameReader:
    def __init__(
        self, frame_data: bytes, frame_index: int, sprite_frame_duration: int
    ) -> None:
        self.frame_data: bytes = frame_data
        self.frame_index: int = frame_index
        self.sprite_frame_duration: int = sprite_frame_duration

        self.bytes_in_frame: int = 0
        self.magic_number: int = 0
        self.old_num_chunks: int = 0
        self.frame_duration: int = 0
        self.num_chunks: int = 0

        self.cels: list[Cel] = []

    def read(self) -> None:
        header_data: bytes = self.frame_data[:frame_header_size]

        (
            self.bytes_in_frame,
            self.magic_number,
            self.old_num_chunks,
            self.frame_duration,
            self.num_chunks,
        ) = frame_header_struct.unpack(header_data)

        if self.magic_number != 0xF1FA:
            raise ValueError(
                f"Incorrect frame magic number, expected {0xF1FA}, got {self.magic_number}"
            )

        if self.frame_duration == 0:
            self.frame_duration = self.sprite_frame_duration

    def get_chunks(self) -> list[Chunk]:
        chunks_in_frame = self.num_chunks
        if chunks_in_frame == 0:
            chunks_in_frame = self.old_num_chunks

        # Create chunks
        chunks: list[Chunk] = []
        chunks_data: BytesIO = BytesIO(
            self.frame_data[frame_header_size : self.bytes_in_frame]
        )
        chunk_header_struct: Struct = Struct(chunk_header_format)

        for _ in range(chunks_in_frame):
            # Unpack chunk header
            chunk_header_data: bytes = chunks_data.read(chunk_header_struct.size)
            (chunk_size, chunk_type) = chunk_header_struct.unpack(chunk_header_data)

            # Get chunk data
            chunk_data: bytes = chunks_data.read(chunk_size - chunk_header_struct.size)

            chunk: Chunk = Chunk(chunk_size, ChunkType(chunk_type), chunk_data)
            chunks.append(chunk)

        return chunks

    def to_frame(self) -> Frame:
        return Frame(self.frame_index, self.frame_duration, self.cels)
