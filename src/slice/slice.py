from src.slice.slice_flags import SliceFlags
from src.slice.slice_key import SliceKey


class Slice:
    def __init__(
        self, name: str, slice_keys: list[SliceKey], flags: SliceFlags
    ) -> None:
        self.name: str = name
        self.slice_keys: list[SliceKey] = slice_keys
        self.flags: SliceFlags = flags

    def __repr__(self) -> str:
        return f"Slice({self.name}, {self.slice_keys})"
