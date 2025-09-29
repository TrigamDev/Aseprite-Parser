from io import BytesIO
from struct import Struct
from src.slice.slice_flags import SliceFlags
from src.slice.slice_key import SliceKey

slice_key_format: str = (
    "<I"  # Frame number
    + "l"  # Bounds X
    + "l"  # Bounds Y
    + "I"  # Width
    + "I"  # Height
)

slice_key_nine_patch_format: str = (
    "l"  # Center X
    + "l"  # Center Y
    + "I"  # Center width
    + "I"  # Center height
)

slice_key_pivot_format: str = (
    "l"  # Pivot X
    + "l"  # Pivot Y
)


class SliceKeyReader:
    def __init__(self, slice_keys_data: BytesIO, slice_flags: SliceFlags) -> None:
        self.slice_keys_data: BytesIO = slice_keys_data
        self.slice_flags: SliceFlags = slice_flags

        self.frame_number: int = 0
        self.slice_x: int = 0
        self.slice_y: int = 0
        self.slice_width: int = 0
        self.slice_height: int = 0

        # Nine-patch
        self.center_x: int = 0
        self.center_y: int = 0
        self.center_width: int = 0
        self.center_height: int = 0

        # Pivot
        self.pivot_x: int = 0
        self.pivot_y: int = 0

    def read(self) -> None:
        slice_key_struct: Struct = Struct(slice_key_format)
        slice_key_data: bytes = self.slice_keys_data.read(slice_key_struct.size)

        (
            self.frame_number,
            self.slice_x,
            self.slice_y,
            self.slice_width,
            self.slice_height,
        ) = slice_key_struct.unpack(slice_key_data)

        if self.slice_flags & SliceFlags.IsNinePatch:
            slice_key_nine_patch_struct: Struct = Struct(slice_key_nine_patch_format)
            nine_patch_data: bytes = self.slice_keys_data.read(
                slice_key_nine_patch_struct.size
            )

            (self.center_x, self.center_y, self.center_width, self.center_height) = (
                slice_key_nine_patch_struct.unpack(nine_patch_data)
            )

        if self.slice_flags & SliceFlags.HasPivot:
            slice_key_pivot_struct: Struct = Struct(slice_key_pivot_format)
            pivot_data: bytes = self.slice_keys_data.read(slice_key_pivot_struct.size)

            (
                self.pivot_x,
                self.pivot_y,
            ) = slice_key_pivot_struct.unpack(pivot_data)

    def to_slice_key(self) -> SliceKey:
        return SliceKey(
            self.frame_number,
            self.slice_x,
            self.slice_y,
            self.slice_width,
            self.slice_height,
            self.center_x,
            self.center_y,
            self.center_width,
            self.center_height,
            self.pivot_x,
            self.pivot_y,
        )
