from src.cel.cel import Cel


frame_header_size: int = 16


class Frame:
    def __init__(
        self, frame_index: int, sprite_frame_duration: int, cels: list[Cel]
    ) -> None:
        self.frame_index: int = frame_index
        self.frame_duration: int = sprite_frame_duration

        self.cels: list[Cel] = cels

    def __repr__(self) -> str:
        return f"Frame({self.frame_index}, Cels: {self.cels})"

    # def read_chunk(self, file_reader: BufferedReader) -> None:
    # chunk_size = read_bytes(file_reader.read(4), 0, 4, "i")
    # chunk_type = ChunkType(read_bytes(file_reader.read(2), 0, 2, "i"))
    # chunk_data = file_reader.read(chunk_size - 6)

    # match chunk_type:

    # Cel Chunk (0x2005)
    # case ChunkType.Cel:
    #    cel_chunk = CelChunk(self.sprite, chunk_size, chunk_data)
    #    cel: Cel | None = cel_chunk.read()
    #    if cel:
    #        self.cels.append(cel)

    # Cel Extra Chunk (0x2006)

    # Tags Chunk (0x2018)
    # case ChunkType.Tags:
    #    tags_chunk = TagsChunk(self.sprite, chunk_size, chunk_data)
    #    tags: list[Tag] = tags_chunk.read()
    #    self.sprite.tags.extend(tags)

    # Color Profile Chunk (0x2007)

    # Palette Chunk (0x2019), Old palette chunk (0x0004), Old palette chunk (0x0011)
    # case ChunkType.Palette | ChunkType.OldPalette | ChunkType.EvenOlderPalette:
    #    palette_chunk = PaletteChunk(
    #        self.sprite, chunk_type, chunk_size, chunk_data
    #    )
    #    palette_chunk.read()

    # Tileset Chunk (0x2023)
    # case ChunkType.Tileset:
    #    tileset_chunk = TilesetChunk(self.sprite, chunk_size, chunk_data)
    #    tileset: Tileset = tileset_chunk.read()
    #    self.sprite.tilesets.append(tileset)

    # Slice Chunk (0x2022)
    # case ChunkType.Slice:
    #    slice_chunk = SliceChunk(self.sprite, chunk_size, chunk_data)
    #    aseprite_slice: Slice = slice_chunk.read()
    #    self.sprite.slices.append(aseprite_slice)

    # Mask Chunk (0x2016)

    # User Data Chunk (0x2020)

    # External Files Chunk (0x2008)

    # Path Chunk (0x2017)
    # case ChunkType.Path:
    #    print("Path Chunk (0x2017) ignored")

    # case ChunkType.Unknown | _:
    #    print(f"Unhandled chunk: {chunk_type.name}, {chunk_size} bytes")
