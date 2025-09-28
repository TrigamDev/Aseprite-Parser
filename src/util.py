import math
import struct
from typing import Any


def bytes_to_binary_string(byte_data: bytes) -> str:
    """
    Converts byte data to a binary string.

    Args:
        byte_data (bytes): The byte data to convert.

    Returns:
        str: The binary string.

    Examples:
        >>> bytes_to_binary_string(b"\xfa")
        11111010

        >>> bytes_to_binary_string(b"\x05")
        00000101
    """
    return "".join(format(byte, "08b") for byte in byte_data)


def has_flag(value: int, flag_place: int) -> bool:
    """
    Checks if the value of a binary place of an int is `1`.

    Args:
        value (int): The integer value to check.
        flag_place (int): The binary place to check.

    Returns:
        bool: True if the value has the flag place, False otherwise.

    Example:
        >>> has_flag(3, 1)
        True

    """
    return bool((value >> flag_place) & 1)


def read_bytes(
    byte_data: bytes, byte_start: int, number_of_bytes: int, data_format: str
) -> Any:
    """
    Reads and parses bytes from byte data.

    Args:
        byte_data (bytes): The byte data to read from.
        byte_start (int): The byte offset to start reading from.
        number_of_bytes (int): The number of bytes to read.
        data_format (str): The data format to parse to.

    Returns:
        Any: The parsed data.

    Examples:
        >>> read_bytes(b"\xfa", 0, 2, "i")
        250

        >>> read_bytes(b"\x2a\xb7", 0, 2, "i")
        46890
    """
    num_byte_groups = math.ceil(number_of_bytes / 4)

    struct_format: str = f"<{data_format * num_byte_groups}"
    padding = b"\x00" * ((num_byte_groups * 4) - number_of_bytes)

    return struct.unpack(
        struct_format, byte_data[byte_start : byte_start + number_of_bytes] + padding
    )[0]


string_header_size: int = 2


def read_string(byte_data: bytes, byte_start: int) -> str:
    """
    Reads a string from byte data.

    Note: This only applies to Aseprite's string data,
    which includes the string's length as the first two bytes.

    Args:
        byte_data (bytes): The byte data to read from.
        byte_start (int): The byte offset to start reading from.

    Returns:
        str: The parsed string.

    Examples:
        >>> read_string(b"\x0b\x00\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64", 0)
        "Hello world"
    """
    string_byte_length = read_bytes(byte_data, byte_start, 2, "i")

    from_byte: int = byte_start + string_header_size
    to_byte: int = from_byte + string_byte_length

    string_bytes = byte_data[from_byte:to_byte]
    return string_bytes.decode("utf-8")


def string_byte_size(string: str) -> int:
    """
    Returns the number of bytes in a string.

    Args:
        string (str): The string to get the size of.

    Returns:
        int: The number of bytes in the string.

    Examples:
        >>> string_byte_size("A")
        1

        >>> string_byte_size("Hello world")
        11
    """
    return len(string.encode("utf-8"))
