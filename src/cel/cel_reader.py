from typing import Sequence
import zlib
from struct import Struct

import numpy

from src.cel.cel import Cel
from src.cel.cel_type import CelType
from src.cel.image_cel import ImageCel
from src.cel.linked_cel import LinkedCel
from src.cel.tilemap_cel import TilemapCel
from src.chunk.chunk import Chunk
from src.color.color_depth import ColorDepth
from src.color.pixel.grayscale_pixel import parse_grayscale_pixel_stream
from src.color.pixel.indexed_pixel import parse_indexed_pixel_stream
from src.color.pixel.pixel import Pixel
from src.color.pixel.rgba_pixel import parse_rgba_pixel_stream
from src.tileset.tile import Tile, parse_tile_stream

cel_chunk_format: str = (
    "<H"  # Layer index
    + "h"  # X position
    + "h"  # Y position
    + "B"  # Opacity
    + "H"  # Cel type
    + "h"  # Z-index
    + "5x"  # For future
)
cel_chunk_struct: Struct = Struct(cel_chunk_format)

image_cel_chunk_format: str = (
    "<H"  # Width
    + "H"  # Height
)
image_cel_chunk_struct: Struct = Struct(image_cel_chunk_format)

linked_cel_chunk_format: str = "<H"  # Linked frame index
linked_cel_chunk_struct: Struct = Struct(linked_cel_chunk_format)

tilemap_cel_chunk_format: str = (
    "<H"  # Width (tiles)
    + "H"  # Height (tiles)
    + "H"  # Bits per tile
    + "I"  # Tile ID bitmask
    + "I"  # Horizontal flip bitmask
    + "I"  # Vertical flip bitmask
    + "I"  # Diagonal flip bitmask
    + "10x"  # Reserved
)
tilemap_cel_chunk_struct: Struct = Struct(tilemap_cel_chunk_format)


class CelReader:
    def __init__(self, chunk: Chunk, color_depth: ColorDepth) -> None:
        self.chunk: Chunk = chunk
        self.color_depth: ColorDepth = color_depth

        # Cel
        self.layer_index: int = 0
        self.x: int = 0
        self.y: int = 0
        self.opacity: int = 0
        self.cel_type: CelType = CelType.Unknown
        self.z_index: int = 0

        # Image cel
        self.width: int = 0
        self.height: int = 0
        self.pixels: list[list[Pixel]] = []
        self.pixel_data: bytes = bytes()

        # Linked cel
        self.linked_frame_index: int = 0

        # Tilemap cel
        self.tile_width: int = 0
        self.tile_height: int = 0
        self.bits_per_tile: int = 0
        self.tile_id_bitmask: int = 0
        self.horizontal_flip_bitmask: int = 0
        self.vertical_flip_bitmask: int = 0
        self.diagonal_flip_bitmask: int = 0
        self.tiles: list[list[Tile]] = []

    def read(self) -> None:
        (self.layer_index, self.x, self.y, self.opacity, cel_type, self.z_index) = (
            cel_chunk_struct.unpack(self.chunk.data.read(cel_chunk_struct.size))
        )
        self.cel_type = CelType(cel_type)

        match self.cel_type:
            case CelType.RawImageData | CelType.CompressedImage:
                self.read_image_cel()
            case CelType.LinkedCel:
                self.read_linked_cel()
            case CelType.CompressedTilemap:
                self.read_tilemap_cel()

    def read_image_cel(self) -> None:
        (self.width, self.height) = image_cel_chunk_struct.unpack(
            self.chunk.data.read(image_cel_chunk_struct.size)
        )

        # Get stream of pixels, uncompress if needed
        if self.cel_type is CelType.CompressedImage:
            compressed_pixel_stream = self.chunk.data.read()
            self.pixel_data = zlib.decompress(compressed_pixel_stream)
        else:
            self.pixel_data = self.chunk.data.read()

        # Parse pixels stream into 1D list
        pixels_list: Sequence[Pixel] = []
        match self.color_depth:
            case ColorDepth.Indexed:
                pixels_list = parse_indexed_pixel_stream(self.pixel_data)
            case ColorDepth.Grayscale:
                pixels_list = parse_grayscale_pixel_stream(self.pixel_data)
            case ColorDepth.RGBA:
                pixels_list = parse_rgba_pixel_stream(self.pixel_data)

        # Reshape 1D list to 2D list
        pixels_array: list[list[Pixel]] = (
            numpy.asarray(pixels_list).reshape((self.width, self.height)).tolist()
        )
        self.pixels = pixels_array

    def read_linked_cel(self) -> None:
        self.linked_frame_index = linked_cel_chunk_struct.unpack(
            self.chunk.data.read(linked_cel_chunk_struct.size)
        )[0]

    def read_tilemap_cel(self) -> None:
        (
            self.tile_width,
            self.tile_height,
            self.bits_per_tile,
            self.tile_id_bitmask,
            self.horizontal_flip_bitmask,
            self.vertical_flip_bitmask,
            self.diagonal_flip_bitmask,
        ) = tilemap_cel_chunk_struct.unpack(
            self.chunk.data.read(tilemap_cel_chunk_struct.size)
        )

        # Get and uncompress tiles stream
        compressed_tiles_stream = self.chunk.data.read()
        tiles_stream: bytes = zlib.decompress(compressed_tiles_stream)

        # Parse tiles stream into 1D list
        tiles_list: list[Tile] = parse_tile_stream(
            tiles_stream,
            self.bits_per_tile,
            self.tile_id_bitmask,
            self.horizontal_flip_bitmask,
            self.vertical_flip_bitmask,
            self.diagonal_flip_bitmask,
        )

        # Reshape 1D list to 2D list
        tiles_array: list[list[Tile]] = (
            numpy.asarray(tiles_list)
            .reshape((self.tile_width, self.tile_height))
            .tolist()
        )
        self.tiles = tiles_array

    def to_cel(self) -> Cel:
        match self.cel_type:
            # Image cel
            case CelType.RawImageData | CelType.CompressedImage:
                return ImageCel(
                    self.cel_type,
                    self.layer_index,
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    self.opacity,
                    self.z_index,
                    self.color_depth,
                    self.pixels,
                    self.pixel_data,
                )

            # Linked cel
            case CelType.LinkedCel:
                return LinkedCel(
                    self.cel_type,
                    self.layer_index,
                    self.x,
                    self.y,
                    self.opacity,
                    self.z_index,
                    self.color_depth,
                    self.linked_frame_index,
                )

            # Tilemap cel
            case CelType.CompressedTilemap:
                return TilemapCel(
                    self.cel_type,
                    self.layer_index,
                    self.x,
                    self.y,
                    self.tile_width,
                    self.tile_height,
                    self.opacity,
                    self.z_index,
                    self.color_depth,
                    self.tiles,
                )

            # Unknown cel
            case CelType.Unknown | _:
                return Cel(
                    self.cel_type,
                    self.layer_index,
                    self.x,
                    self.y,
                    self.opacity,
                    self.z_index,
                    self.color_depth,
                )
