from enum import IntEnum


class CelType(IntEnum):
    Unknown = -1
    RawImageData = 0
    LinkedCel = 1
    CompressedImage = 2
    CompressedTilemap = 3
