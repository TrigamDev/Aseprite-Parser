import math
import struct


def bytes_to_binary_string(byte_data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in byte_data)


def has_flag(value: int, flag_place: int) -> bool:
    return bool((value >> flag_place) & 1)


def read_bytes(
    byte_data: bytes, byte_start: int, number_of_bytes: int, data_format: str
):
    number_of_byte_groups = math.ceil(number_of_bytes / 4)
    struct_format: str = f"<{data_format * number_of_byte_groups}"
    padding = b"\x00" * ((number_of_byte_groups * 4) - number_of_bytes)
    return struct.unpack(
        struct_format, byte_data[byte_start : byte_start + number_of_bytes] + padding
    )[0]


def read_string(byte_data: bytes, byte_start: int) -> str:
    string_byte_length = read_bytes(byte_data, byte_start, 2, "i")
    string_bytes = byte_data[byte_start + 2 : byte_start + 2 + string_byte_length]
    return string_bytes.decode("utf-8")
