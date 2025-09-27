from src.util import read_bytes, read_string


class Palette:
    def __init__(self):
        self.colors: list[tuple[int, int, int, int] | None] = []
        self.transparent_index: int = 0

    def get_color(self, index: int):
        return self.colors[index]

    def set_color(self, index: int, color):
        self.colors[index] = color

    def get_transparent_index(self):
        return self.transparent_index

    def set_transparent_index(self, index):
        self.transparent_index = index

    def resize(self, new_length: int):
        if len(self.colors) > new_length:
            del self.colors[new_length:]
        else:
            self.colors.extend([None] * (new_length - len(self.colors) + 1))

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes):
        palette_size: int = read_bytes(chunk_data, 0, 4, "i")
        from_index: int = read_bytes(chunk_data, 4, 4, "i")
        to_index: int = read_bytes(chunk_data, 8, 4, "i")

        if palette_size > len(self.colors):
            self.resize(to_index)

        num_changed_entries: int = to_index - from_index + 1
        entry_bytes_start = 20
        for i in range(num_changed_entries):
            entry_flags: int = read_bytes(chunk_data, entry_bytes_start, 2, "i")
            has_name: bool = bool(entry_flags & 1)

            entry_red: int = read_bytes(chunk_data, entry_bytes_start + 2, 1, "i")
            entry_green: int = read_bytes(chunk_data, entry_bytes_start + 3, 1, "i")
            entry_blue: int = read_bytes(chunk_data, entry_bytes_start + 4, 1, "i")
            entry_alpha: int = read_bytes(chunk_data, entry_bytes_start + 5, 1, "i")

            if has_name:
                entry_name: str = read_string(chunk_data, entry_bytes_start + 6)
                entry_bytes_start = (
                    entry_bytes_start + 8 + len(entry_name.encode("utf-8"))
                )
            else:
                entry_bytes_start = entry_bytes_start + 6

            self.set_color(
                from_index + i, (entry_red, entry_green, entry_blue, entry_alpha)
            )

        print(self.colors)
