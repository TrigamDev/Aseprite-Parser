from io import BufferedReader
import struct

from src.sprite.cel.cel import Cel
from src.sprite.cel.cel_chunk import CelChunk
from src.sprite.chunk.chunk_type import ChunkType
from src.sprite.layer.layer_chunk import LayerChunk
from src.sprite.palette.palette_chunk import PaletteChunk
from src.sprite.layer.layer import Layer
from src.sprite.slice.slice import Slice
from src.sprite.slice.slice_chunk import SliceChunk
from src.sprite.tag.tag import Tag
from src.sprite.tag.tags_chunk import TagsChunk
from src.sprite.tileset.tileset import Tileset
from src.sprite.tileset.tileset_chunk import TilesetChunk
from src.util import read_bytes


frame_header_size: int = 16


class Frame:
    def __init__(self, sprite):
        self.sprite = sprite
        self.frame_index: int = len(sprite.frames)
        self.frame_duration: int = 0

        self.cels: list[Cel] = []

    def __repr__(self):
        return f"Frame({self.frame_index}, Cels: {self.cels})"

    def read(self, file_reader: BufferedReader) -> None:
        frame_header = file_reader.read(frame_header_size)

        frame_duration = struct.unpack("<i", frame_header[4:6] + b"\x00\x00")[0]
        if frame_duration > 0:
            self.frame_duration = frame_duration
        else:
            self.frame_duration = self.sprite.frame_speed

        chunks_in_frame = struct.unpack("<i", frame_header[12:16])[0]

        if chunks_in_frame == 0:
            chunks_in_frame = struct.unpack("<i", frame_header[6:8] + b"\x00\x00")[0]

        for _ in range(chunks_in_frame):
            self.read_chunk(file_reader)

        self.sprite.add_frame(self)

    def read_chunk(self, file_reader: BufferedReader) -> None:
        chunk_size = read_bytes(file_reader.read(4), 0, 4, "i")
        chunk_type = ChunkType(read_bytes(file_reader.read(2), 0, 2, "i"))
        chunk_data = file_reader.read(chunk_size - 6)

        match chunk_type:
            # Layer Chunk (0x2004)
            case ChunkType.Layer:
                layer_chunk = LayerChunk(self.sprite, chunk_size, chunk_data)
                layer: Layer | None = layer_chunk.read()
                if layer:
                    self.sprite.add_layer(layer)

            # Cel Chunk (0x2005)
            case ChunkType.Cel:
                cel_chunk = CelChunk(self.sprite, chunk_size, chunk_data)
                cel: Cel | None = cel_chunk.read()
                if cel:
                    self.cels.append(cel)

            # Cel Extra Chunk (0x2006)

            # Tags Chunk (0x2018)
            case ChunkType.Tags:
                tags_chunk = TagsChunk(self.sprite, chunk_size, chunk_data)
                tags: list[Tag] = tags_chunk.read()
                self.sprite.tags.extend(tags)

            # Color Profile Chunk (0x2007)

            # Palette Chunk (0x2019), Old palette chunk (0x0004), Old palette chunk (0x0011)
            case ChunkType.Palette | ChunkType.OldPalette | ChunkType.EvenOlderPalette:
                palette_chunk = PaletteChunk(
                    self.sprite, chunk_type, chunk_size, chunk_data
                )
                palette_chunk.read()

            # Tileset Chunk (0x2023)
            case ChunkType.Tileset:
                tileset_chunk = TilesetChunk(self.sprite, chunk_size, chunk_data)
                tileset: Tileset = tileset_chunk.read()
                self.sprite.tilesets.append(tileset)

            # Slice Chunk (0x2022)
            case ChunkType.Slice:
                slice_chunk = SliceChunk(self.sprite, chunk_size, chunk_data)
                aseprite_slice: Slice = slice_chunk.read()
                self.sprite.slices.append(aseprite_slice)

            # Mask Chunk (0x2016)

            # User Data Chunk (0x2020)

            # External Files Chunk (0x2008)

            # Path Chunk (0x2017)
            case ChunkType.Path:
                print("Path Chunk (0x2017) ignored")

            case ChunkType.Unknown | _:
                print(f"Unhandled chunk: {chunk_type.name}, {chunk_size} bytes")
