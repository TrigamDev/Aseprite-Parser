import struct
from src.sprite.cel.cel import CelType, Cel
from src.sprite.cel.image_cel import ImageCel
from src.sprite.chunk.chunk import Chunk


class CelChunk(Chunk):
    def __init__(self, frame, chunk_size: int, chunk_data: bytes):
        super().__init__(frame, chunk_size, chunk_data)

    def read(self) -> Cel | None:
        cel_type = CelType(struct.unpack("<i", self.chunk_data[7:9] + b"\x00\x00")[0])

        match cel_type:
            case CelType.RawImageData | CelType.CompressedImage:
                return ImageCel(self.frame.sprite.color_depth).read_from_chunk(
                    self.chunk_size, self.chunk_data
                )
            case CelType.Unknown | _:
                return None
