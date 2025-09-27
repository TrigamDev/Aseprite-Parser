from enum import IntEnum


class ChunkType(IntEnum):
    Unknown = -1
    OldPalette = 0x0004
    EvenOlderPalette = 0x00011
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
