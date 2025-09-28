from typing import Self
from src.util import read_bytes

slice_key_size: int = 20
slice_key_9_patch_size: int = 16
slice_key_pivot_size: int = 8


class SliceKey:
    def __init__(self) -> None:
        self.frame_index: int = 0

        self.x: int = 0
        self.y: int = 0
        self.width: int = 0
        self.height: int = 0

        self.center_x: int = 0
        self.center_y: int = 0
        self.center_width: int = 0
        self.center_height: int = 0

        self.pivot_x: int = 0
        self.pivot_y: int = 0

    def __repr__(self) -> str:
        return f"SliceKey({self.frame_index}, {self.x}x, {self.y}y, {self.width}x{self.height})"

    def read_from_chunk(
        self,
        slice_key_data: bytes,
        is_9_patch: bool,
        has_pivot: bool,
    ) -> Self:
        self.frame_index = read_bytes(slice_key_data, 0, 4, "i")

        self.x = read_bytes(slice_key_data, 4, 4, "i")
        self.y = read_bytes(slice_key_data, 8, 4, "i")
        self.width = read_bytes(slice_key_data, 12, 4, "i")
        self.height = read_bytes(slice_key_data, 16, 4, "i")

        end_byte: int = slice_key_size

        if is_9_patch:
            self.center_x = read_bytes(slice_key_data, end_byte, 4, "i")
            self.center_y = read_bytes(slice_key_data, end_byte + 4, 4, "i")
            self.center_width = read_bytes(slice_key_data, end_byte + 8, 4, "i")
            self.center_height = read_bytes(slice_key_data, end_byte + 12, 4, "i")
            end_byte += 12

        if has_pivot:
            self.pivot_x = read_bytes(slice_key_data, end_byte, 4, "i")
            self.pivot_y = read_bytes(slice_key_data, end_byte + 4, 4, "i")

        return self
