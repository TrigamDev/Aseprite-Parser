from src.chunk.chunk import Chunk
from src.tag.tag import Tag
from src.util import read_bytes, string_byte_size, string_header_size

tag_chunk_header_size: int = 10
tag_size: int = 17


class TagsChunk(Chunk):
    def __init__(self, sprite, chunk_size: int, chunk_data: bytes) -> None:
        super().__init__(sprite, chunk_size, chunk_data)

    def read(self) -> list[Tag]:
        num_tags: int = read_bytes(self.chunk_data, 0, 2, "i")
        tags: list[Tag] = []

        next_tag_start: int = tag_chunk_header_size
        for _ in range(num_tags):
            # Tags can be a variable length due to the tag name,
            # so include the entire rest of the chunk in case
            tag_data: bytes = self.chunk_data[next_tag_start : self.chunk_size]
            tag = Tag().read_from_chunk(tag_data)

            tags.append(tag)
            next_tag_start += (
                tag_size + string_byte_size(tag.tag_name) + string_header_size
            )

        return tags
