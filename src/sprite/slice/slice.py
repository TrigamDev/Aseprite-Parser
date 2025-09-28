from typing import Self
from src.sprite.slice.slice_key import (
    SliceKey,
    slice_key_size,
    slice_key_9_patch_size,
    slice_key_pivot_size,
)
from src.util import (
    has_flag,
    read_bytes,
    read_string,
    string_byte_size,
    string_header_size,
)

slice_chunk_header_size: int = 12


class Slice:
    def __init__(self) -> None:
        self.name: str = ""

        self.num_slice_keys: int = 0
        self.slice_keys: list[SliceKey] = []

        self.flags: dict[str, bool] = {
            "is_9_patch_slice": False,
            "has_pivot_information": False,
        }

    def __repr__(self) -> str:
        return f"Slice({self.name}, {self.slice_keys})"

    def read_from_chunk(self, chunk_data: bytes) -> Self:
        self.num_slice_keys = read_bytes(chunk_data, 0, 4, "i")

        flags: int = read_bytes(chunk_data, 4, 4, "i")
        self.flags["is_9_patch_slice"] = has_flag(flags, 0)
        self.flags["has_pivot_information"] = has_flag(flags, 1)

        self.name = read_string(chunk_data, 12)

        actual_slice_key_size: int = slice_key_size
        if self.flags["is_9_patch_slice"]:
            actual_slice_key_size += slice_key_9_patch_size
        if self.flags["has_pivot_information"]:
            actual_slice_key_size += slice_key_pivot_size

        for slice_key_num in range(self.num_slice_keys):
            byte_offset: int = (
                slice_chunk_header_size
                + string_byte_size(self.name)
                + string_header_size
                + (actual_slice_key_size * slice_key_num)
            )
            slice_key_data: bytes = chunk_data[
                byte_offset : byte_offset + actual_slice_key_size
            ]

            slice_key: SliceKey = SliceKey().read_from_chunk(
                slice_key_data,
                self.flags["is_9_patch_slice"],
                self.flags["has_pivot_information"],
            )
            self.slice_keys.append(slice_key)

        return self
