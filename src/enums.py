from enum import IntEnum


class ChunkType(IntEnum):
    Unknown = -1
    OldPalette1 = 0x0004
    OldPalette2 = 0x00011
    Layer = 0x2004
    Cel = 0x2005
    CelExtra = 0x2006
    ColorProfile = 0x2007
    ExternalFiles = 0x2008
    Mask = 0x2016
    Path = 0x2017
    Tags = 0x2018
    Palette = 0x2019
    UserData = 0x2020
    Slice = 0x2022
    Tileset = 0x2023


class ColorDepth(IntEnum):
    Unknown = -1
    Indexed = 8
    Grayscale = 18
    RGBA = 32


class LayerType(IntEnum):
    Unknown = -1
    Normal = 0
    Group = 1
    Tilemap = 2


class CelType(IntEnum):
    Unknown = -1
    RawImageData = 0
    LinkedCel = 1
    CompressedImage = 2
    CompressedTilemap = 3


class BlendMode(IntEnum):
    Unknown = -1
    Normal = 0
    Multiply = 1
    Screen = 2
    Overlay = 3
    Darken = 4
    Lighten = 5
    ColorDodge = 6
    ColorBurn = 7
    HardLight = 8
    SoftLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15
    Addition = 16
    Subtract = 17
    Divide = 18
