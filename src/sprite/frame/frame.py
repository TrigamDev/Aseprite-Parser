from io import BufferedReader
import struct

from src.sprite.cel.cel import Cel
from src.sprite.chunk.cel_chunk import CelChunk
from src.sprite.chunk.chunk_type import ChunkType
from src.sprite.chunk.layer_chunk import LayerChunk
from src.sprite.layer.layer import Layer


class Frame:
    def __init__(self, sprite):
        self.sprite = sprite
        self.frame_index: int = len(sprite.frames)
        self.frame_duration: int = 0

        self.cels: list[Cel] = []

    def __repr__(self):
        return f"Frame({self.frame_index}, Cels: {self.cels})"

    def read(self, file_reader: BufferedReader) -> None:
        frame_header = file_reader.read(16)

        frame_duration = struct.unpack("<i", frame_header[4:6] + b"\x00\x00")[0]
        if frame_duration > 0:
            self.frame_duration = frame_duration
        else:
            self.frame_duration = self.sprite.frame_speed

        chunks_in_frame = struct.unpack("<i", frame_header[12:16])[0]
        print(f"Chunks in frame: {chunks_in_frame}")
        if chunks_in_frame == 0:
            chunks_in_frame = struct.unpack("<i", frame_header[6:8] + b"\x00\x00")[0]

        for i in range(chunks_in_frame):
            self.read_chunk(file_reader)

        self.sprite.add_frame(self)

    def read_chunk(self, file_reader: BufferedReader) -> None:
        chunk_size = struct.unpack("<i", file_reader.read(4))[0]
        chunk_type = ChunkType(
            struct.unpack("<i", file_reader.read(2) + b"\x00\x00")[0]
        )
        chunk_data = file_reader.read(chunk_size - 6)

        print(f"Chunk size: {chunk_size} bytes, Chunk type: {chunk_type.name}")

        match chunk_type:
            case ChunkType.Layer:
                chunk = LayerChunk(self.sprite, chunk_size, chunk_data)
                layer: Layer | None = chunk.read()
                self.sprite.add_layer(layer)
            case ChunkType.Cel:
                chunk = CelChunk(self.sprite, chunk_size, chunk_data)
                cel: Cel | None = chunk.read()
                if cel:
                    self.cels.append(cel)
