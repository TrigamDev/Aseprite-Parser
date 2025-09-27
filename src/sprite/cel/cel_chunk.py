from src.sprite.cel.cel import CelType, Cel
from src.sprite.cel.image_cel import ImageCel
from src.sprite.cel.linked_cel import LinkedCel
from src.sprite.cel.tileset_cel import TilesetCel
from src.sprite.chunk.chunk import Chunk
from src.util import read_bytes


class CelChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes):
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self) -> Cel | None:
        cel_type = CelType(read_bytes(self.chunk_data, 7, 2, "i"))

        match cel_type:
            case CelType.RawImageData | CelType.CompressedImage:
                return ImageCel(self.sprite).read_from_chunk(
                    self.chunk_size, self.chunk_data
                )
            case CelType.LinkedCel:
                return LinkedCel(self.sprite).read_from_chunk(
                    self.chunk_size, self.chunk_data
                )
            case CelType.CompressedTilemap:
                return TilesetCel(self.sprite).read_from_chunk(
                    self.chunk_size, self.chunk_data
                )
            case CelType.Unknown | _:
                return None
