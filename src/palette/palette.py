from src.util import read_bytes, read_string, string_byte_size, string_header_size

palette_chunk_header_size: int = 20
palette_entry_size: int = 6
old_palette_chunk_header_size: int = 2
old_palette_color_size: int = 3


class Palette:
    def __init__(self) -> None:
        self.colors: list[tuple[int, int, int, int] | None] = []
        self.transparent_entry_index: int = 0

    def __repr__(self) -> str:
        return f"Palette({self.colors}, {self.transparent_entry_index})"

    def get_color(self, index: int) -> tuple[int, int, int, int] | None:
        return self.colors[index]

    def set_color(self, index: int, color) -> None:
        self.colors[index] = color

    def get_transparent_entry_index(self) -> int:
        return self.transparent_entry_index

    def set_transparent_entry_index(self, index) -> None:
        self.transparent_entry_index = index

    def resize(self, new_length: int) -> None:
        if len(self.colors) > new_length:
            del self.colors[new_length:]
        else:
            self.colors.extend([None] * (new_length - len(self.colors)))

    def read_from_chunk(self, chunk_data: bytes) -> None:
        palette_size: int = read_bytes(chunk_data, 0, 4, "i")
        from_index: int = read_bytes(chunk_data, 4, 4, "i")
        to_index: int = read_bytes(chunk_data, 8, 4, "i")

        self.resize(palette_size)

        num_changed_entries: int = to_index - from_index + 1
        entry_bytes_start: int = palette_chunk_header_size
        for changed_entry_num in range(num_changed_entries):
            entry_flags: int = read_bytes(chunk_data, entry_bytes_start, 2, "i")
            has_name: bool = bool(entry_flags & 1)

            entry_red: int = read_bytes(chunk_data, entry_bytes_start + 2, 1, "i")
            entry_green: int = read_bytes(chunk_data, entry_bytes_start + 3, 1, "i")
            entry_blue: int = read_bytes(chunk_data, entry_bytes_start + 4, 1, "i")
            entry_alpha: int = read_bytes(chunk_data, entry_bytes_start + 5, 1, "i")

            if has_name:
                entry_name: str = read_string(chunk_data, entry_bytes_start + 6)
                entry_bytes_start += (
                    palette_entry_size
                    + string_byte_size(entry_name)
                    + string_header_size
                )
            else:
                entry_bytes_start += palette_entry_size

            self.set_color(
                from_index + changed_entry_num,
                (entry_red, entry_green, entry_blue, entry_alpha),
            )

    def read_from_old_chunk(self, chunk_data: bytes, is_even_older_chunk: bool):
        num_packets: int = read_bytes(chunk_data, 0, 2, "i")
        num_entries_to_skip: int = 0

        packet_bytes_start: int = old_palette_chunk_header_size
        for _ in range(num_packets):
            num_entries_to_skip += read_bytes(chunk_data, packet_bytes_start, 1, "i")

            num_colors_in_packet: int = read_bytes(
                chunk_data, packet_bytes_start + 1, 1, "i"
            )
            if num_colors_in_packet == 0:
                num_colors_in_packet = 256

            self.resize(num_colors_in_packet)

            color_bytes_start: int = packet_bytes_start + 2
            for color_num in range(
                num_entries_to_skip, num_colors_in_packet + num_entries_to_skip
            ):
                color_red: int = read_bytes(chunk_data, color_bytes_start, 1, "i")
                color_green: int = read_bytes(chunk_data, color_bytes_start + 1, 1, "i")
                color_blue: int = read_bytes(chunk_data, color_bytes_start + 2, 1, "i")

                # Chunk stores colors in six-bit values (0-63)
                # and needs to be expanded to eight-bit values
                if is_even_older_chunk:
                    color_red = (color_red << 2) | (color_red >> 4)
                    color_green = (color_green << 2) | (color_green >> 4)
                    color_blue = (color_blue << 2) | (color_blue >> 4)

                self.set_color(color_num, (color_red, color_green, color_blue, 255))

                color_bytes_start += old_palette_color_size

            packet_bytes_start = color_bytes_start
