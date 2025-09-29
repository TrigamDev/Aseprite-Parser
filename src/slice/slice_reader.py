from io import BytesIO
from struct import Struct
from src.chunk.chunk import Chunk
from src.slice.slice import Slice
from src.slice.slice_flags import SliceFlags
from src.slice.slice_key import SliceKey
from src.slice.slice_key_reader import SliceKeyReader
from src.util import read_string, string_byte_size, string_header_size

slice_chunk_format: str = (
    "<I"  # Number of slice keys
    + "I"  # Flags
    + "4x"  # Reserved
)
slice_chunk_struct: Struct = Struct(slice_chunk_format)


class SliceReader:
    def __init__(self, chunk: Chunk) -> None:
        self.chunk: Chunk = chunk

        self.num_slice_keys: int = 0
        self.flags: SliceFlags = SliceFlags(0)
        self.name: str = ""

        self.slice_keys: list[SliceKey] = []

    def read(self) -> None:
        (self.num_slice_keys, flags) = slice_chunk_struct.unpack(
            self.chunk.data[: slice_chunk_struct.size]
        )
        self.flags |= flags

        self.name = read_string(self.chunk.data, slice_chunk_struct.size)
        self.read_slice_keys()

    def read_slice_keys(self) -> None:
        slice_keys_start: int = (
            slice_chunk_struct.size + string_byte_size(self.name) + string_header_size
        )
        slice_keys_data: BytesIO = BytesIO(self.chunk.data[slice_keys_start:])

        for _ in range(0, self.num_slice_keys):
            slice_key_reader: SliceKeyReader = SliceKeyReader(
                slice_keys_data, self.flags
            )
            slice_key_reader.read()

            slice_key: SliceKey = slice_key_reader.to_slice_key()
            self.slice_keys.append(slice_key)

    def to_slice(self) -> Slice:
        return Slice(self.name, self.slice_keys, self.flags)
