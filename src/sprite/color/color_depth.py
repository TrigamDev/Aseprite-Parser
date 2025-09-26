from enum import IntEnum


class ColorDepth(IntEnum):
    Unknown = -1
    Indexed = 8
    Grayscale = 16
    RGBA = 32
