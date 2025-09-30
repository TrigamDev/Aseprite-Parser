from struct import Struct

from src.chunk.chunk import Chunk
from src.chunk.chunk_type import ChunkType
from src.palette.palette import Palette
from src.palette.palette_entry_flags import PaletteEntryFlags
from src.util import read_string

palette_chunk_format: str = (
    "<I"  # New palette size
    + "I"  # From index
    + "I"  # To index
    + "8x"  # For future
)
palette_chunk_struct: Struct = Struct(palette_chunk_format)

palette_chunk_entry_format: str = (
    "<H"  # Flags
    + "B"  # Red
    + "B"  # Green
    + "B"  # Blue
    + "B"  # Alpha
)
palette_chunk_entry_struct: Struct = Struct(palette_chunk_entry_format)

old_palette_chunk_format: str = "<H"  # Number of packets
old_palette_chunk_struct: Struct = Struct(old_palette_chunk_format)

old_palette_packet_format: str = (
    "B"  # Number of palette entries to skip
    + "B"  # Number of colors in packet
)
old_palette_packet_struct: Struct = Struct(old_palette_packet_format)

old_palette_color_format: str = (
    "B"  # Red
    + "B"  # Green
    + "B"  # Blue
)
old_palette_color_struct: Struct = Struct(old_palette_color_format)


class PaletteReader:
    def __init__(self, chunk: Chunk, palette: Palette) -> None:
        self.chunk: Chunk = chunk
        self.palette: Palette = palette

        self.new_palette_size: int = 0
        self.from_index: int = 0
        self.to_index: int = 0

        self.num_packets: int = 0

    def read(self) -> None:
        match self.chunk.type:
            case ChunkType.Palette:
                self.read_palette()
            case ChunkType.OldPalette | ChunkType.EvenOlderPalette:
                self.read_old_palette()

    def read_palette(self) -> None:
        (
            self.new_palette_size,
            self.from_index,
            self.to_index,
        ) = palette_chunk_struct.unpack(self.chunk.data.read(palette_chunk_struct.size))

        self.palette.resize(self.new_palette_size)

        for entry_num in range(self.from_index, self.to_index):
            (flags, red, green, blue, alpha) = palette_chunk_entry_struct.unpack(
                self.chunk.data.read(palette_chunk_entry_struct.size)
            )
            entry_flags: PaletteEntryFlags = PaletteEntryFlags(flags)
            self.palette.set_color(entry_num, (red, green, blue, alpha))

            if entry_flags & PaletteEntryFlags.HasName:
                read_string(self.chunk.data)

    def read_old_palette(self) -> None:
        self.num_packets = old_palette_packet_struct.unpack(
            self.chunk.data.read(old_palette_packet_struct.size)
        )[0]

        num_entries_to_skip: int = 0

        for _ in range(self.num_packets):
            (skip_entries, num_colors) = old_palette_packet_struct.unpack(
                self.chunk.data.read(old_palette_packet_struct.size)
            )

            num_entries_to_skip += skip_entries

            for color_num in range(num_entries_to_skip, num_colors):
                (red, green, blue) = old_palette_color_struct.unpack(
                    self.chunk.data.read(old_palette_color_struct.size)
                )

                # Chunk stores colors in six-bit values (0-63)
                # and needs to be expanded to eight-bit values
                if self.chunk.type is ChunkType.EvenOlderPalette:
                    red = (red << 2) | (red >> 4)
                    green = (green << 2) | (green >> 4)
                    blue = (blue << 2) | (blue >> 4)

                self.palette.set_color(color_num, (red, green, blue))
