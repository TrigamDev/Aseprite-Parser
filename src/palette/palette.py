class Palette:
    def __init__(
        self,
        colors: list[tuple[int, int, int, int] | None],
        transparent_entry_index: int,
        packed_array: list[int]
    ) -> None:
        self.colors: list[tuple[int, int, int, int] | None] = colors
        self.transparent_entry_index: int = transparent_entry_index
        self.packed_array: list[int] = packed_array

    def __repr__(self) -> str:
        return f"Palette({self.colors}, {self.transparent_entry_index})"

    def get_color(self, index: int) -> tuple[int, int, int, int] | None:
        return self.colors[index]

    def get_transparent_entry_index(self) -> int:
        return self.transparent_entry_index
