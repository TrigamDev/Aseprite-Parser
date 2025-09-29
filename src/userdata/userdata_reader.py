
from src.util import read_string
import struct

from src.chunk.chunk import Chunk
from src.userdata.userdata import UserData
from enum import IntEnum
from struct import Struct
from typing import Any
from enum import IntFlag

color_format: str = (
    "<B"     # r
    + "B"   # g
    + "B"   # b
    + "B"   # a
)
color_struct: Struct = Struct(color_format)

class UserDataPropertyType(IntEnum):
    Unknown = 0x0000
    Bool = 0x0001           # 1 byte
    Int8 = 0x0002           # 1 byte
    Uint8 = 0x0003          # 1 byte
    Int16 = 0x0004          # 2 bytes
    Uint16 = 0x0005         # 2 bytes
    Int32 = 0x0006          # 4 bytes
    Uint32 = 0x0007         # 4 bytes
    Int64 = 0x0008          # 8 bytes
    Uint64 = 0x0009         # 8 bytes
    Fixed = 0x000A          # 4 bytes
    Float = 0x000B          # 4 bytes
    Double = 0x000C         # 8 bytes
    String = 0x000D         # n bytes
    Point = 0x000E          # 16 bytes
    Size = 0x000F           # 16 bytes
    Rect = 0x0010           # 32 bytes
    Vector = 0x0011         # n bytes
    NestedMap = 0x0012      # n bytes
    Uuid = 0x0013           # 16 bytes

class UserDataFlags(IntFlag):
    HasText = 1
    HasColor = 2
    HasPropertyMap = 4

class UserDataReader:
    def __init__(self, chunk: Chunk):
        self.chunk: Chunk = chunk
        self.string: str | None = None
        self.color: tuple[int, int, int, int] | None = None
        self.property_maps: list[dict[str, Any]] | None = None

    def _read_property_value(self, type: UserDataPropertyType) -> Any:
        match type:
            case UserDataPropertyType.Bool:
                return bool(self.chunk.data.read(1))
            case UserDataPropertyType.Int8:
                return struct.unpack("b", self.chunk.data.read(1))[0]
            case UserDataPropertyType.Uint8:
                return struct.unpack("B", self.chunk.data.read(1))[0]
            case UserDataPropertyType.Int16:
                return struct.unpack("<h", self.chunk.data.read(2))[0]
            case UserDataPropertyType.Uint16:
                return struct.unpack("<H", self.chunk.data.read(2))[0]
            case UserDataPropertyType.Int32:
                return struct.unpack("<i", self.chunk.data.read(4))[0]
            case UserDataPropertyType.Uint32:
                return struct.unpack("<I", self.chunk.data.read(4))[0]
            case UserDataPropertyType.Int64:
                # TODO: needs to be 64bit
                return struct.unpack("<q", self.chunk.data.read(8))[0]
            case UserDataPropertyType.Uint64:
                # TODO: needs to be 64bit
                return struct.unpack("<Q", self.chunk.data.read(8))[0]
            case UserDataPropertyType.Fixed:
                print("fixed point value not implemented")
                self.chunk.data.read(4)
                return None
            case UserDataPropertyType.Float:
                return struct.unpack("<f", self.chunk.data.read(4))[0]
            case UserDataPropertyType.Double:
                # TODO: float needs to be double precision
                return struct.unpack("<d", self.chunk.data.read(8))[0]
            case UserDataPropertyType.String:
                return read_string(self.chunk.data)
            case UserDataPropertyType.Point:
                x = struct.unpack("<i", self.chunk.data.read(4))[0]
                y = struct.unpack("<i", self.chunk.data.read(4))[0]
                return {"x": x, "y": y}
            case UserDataPropertyType.Size:
                w = struct.unpack("<i", self.chunk.data.read(4))[0]
                h = struct.unpack("<i", self.chunk.data.read(4))[0]
                return {"w": w, "h": h}
            case UserDataPropertyType.Rect:
                x = struct.unpack("<i", self.chunk.data.read(4))[0]
                y = struct.unpack("<i", self.chunk.data.read(4))[0]
                w = struct.unpack("<i", self.chunk.data.read(4))[0]
                h = struct.unpack("<i", self.chunk.data.read(4))[0]
                return {"x": x, "y": y, "w": w, "h": h}
            case UserDataPropertyType.Vector:
                n_elems = struct.unpack("<I", self.chunk.data.read(4))[0]
                vec_type = UserDataPropertyType(struct.unpack("<H", self.chunk.data.read(2))[0])
                values = []
                # each value has a different type
                if vec_type == UserDataPropertyType.Unknown:
                    for _ in range(n_elems):
                        current_type = UserDataPropertyType(struct.unpack("<H", self.chunk.data.read(2))[0])
                        values.append(self._read_property_value(current_type))
                # all values are the same type
                else:
                    for _ in range(n_elem):
                        values.append(self._read_property_value(vec_type))
                return values
            case UserDataPropertyType.NestedMap:
                return self._read_property_map()
            case UserDataPropertyType.Uuid:
                return self.chunk.data.read(16)

    def _read_property(self) -> tuple[str, Any]:
        name = read_string(self.chunk.data)
        type = UserDataPropertyType(struct.unpack("<H", self.chunk.data.read(2))[0])
        value = self._read_property_value(type)
        return (name, value)

    def _read_property_map(self) -> dict[str, Any]:
        n_properties = struct.unpack("<I", self.chunk.data.read(4))[0]
        map = {}
        for _ in range(n_properties):
            name, value = self._read_property()
            map[name] = value
        return map

    def read(self) -> None:
        content_flags = struct.unpack("<I", self.chunk.data.read(4))[0]
        if content_flags & UserDataFlags.HasText:
            self.string = read_string(self.chunk.data)
        if content_flags & UserDataFlags.HasColor:
            (
                red,
                green,
                blue,
                alpha,
            ) = color_struct.unpack(self.chunk.data.read(color_struct.size))
            self.color = (red, green, blue, alpha)
        if content_flags & UserDataFlags.HasPropertyMap:
            _size = struct.unpack("<I", self.chunk.data.read(4))[0]
            n_maps = struct.unpack("<I", self.chunk.data.read(4))[0]
            self.property_maps = []
            for i in range(n_maps):
                # TODO : 0 or extension entry id
                _key = struct.unpack("<I", self.chunk.data.read(4))[0]
                map = self._read_property_map()
                self.property_maps.append(map)

    def to_userdata(self) -> UserData:
        return UserData(
            self.string,
            self.color,
            self.property_maps
        )

