def bytes_to_binary_string(byte_data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in byte_data)


def has_flag(value: int, flag: int) -> bool:
    return (value & flag) != 0
