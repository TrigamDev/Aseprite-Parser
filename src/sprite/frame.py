from io import BufferedReader
import struct

from src.sprite.chunk.cel_chunk import CelChunk
from src.sprite.chunk.layer_chunk import LayerChunk
from src.enums import ChunkType


class Frame:
    def __init__(self, aseprite_file):
        self.frame_duration: int = 0
        self.aseprite_file = aseprite_file

    def read(self, file_reader: BufferedReader):
        frame_header = file_reader.read(16)
        # bytes_in_frame = struct.unpack( "<i", frame_header[0:4] )[ 0 ]

        frame_duration = struct.unpack("<i", frame_header[4:6] + b"\x00\x00")[0]
        if frame_duration > 0:
            self.frame_duration = frame_duration
        else:
            self.frame_duration = self.aseprite_file.frame_speed

        chunks_in_frame = struct.unpack("<i", frame_header[12:16])[0]
        print(f"Chunks in frame: {chunks_in_frame}")
        if chunks_in_frame == 0:
            chunks_in_frame = struct.unpack("<i", frame_header[6:8] + b"\x00\x00")[0]

        for i in range(chunks_in_frame):
            self.read_chunk(file_reader)

        return self

    def read_chunk(self, file_reader: BufferedReader):
        chunk_size = struct.unpack("<i", file_reader.read(4))[0]
        chunk_type = ChunkType(
            struct.unpack("<i", file_reader.read(2) + b"\x00\x00")[0]
        )
        chunk_data = file_reader.read(chunk_size - 6)

        print(f"Chunk size: {chunk_size} bytes, Chunk type: {chunk_type.name}")

        match chunk_type:
            case ChunkType.Layer:
                chunk = LayerChunk(self, chunk_size, chunk_data)
                chunk.read()
            case ChunkType.Cel:
                chunk = CelChunk(self, chunk_size, chunk_data)
                chunk.read()
