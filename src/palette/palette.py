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
