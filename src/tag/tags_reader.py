from struct import Struct

from src.chunk.chunk import Chunk
from src.tag.loop_animation_direction import LoopAnimationDirection
from src.tag.tag import Tag
from src.util import read_string

tags_chunk_format: str = (
    "<H"  # Number of tags
    + "8x"  # For future
)
tags_chunk_struct: Struct = Struct(tags_chunk_format)

tag_format: str = (
    "<H"  # From frame
    + "H"  # To frame
    + "B"  # Loop animation direction
    + "H"  # Repeat N times
    + "6x"  # For future
    + "B"  # Tag red
    + "B"  # Tag green
    + "B"  # Tag blue
    + "1x"  # Extra byte
)
tag_struct: Struct = Struct(tag_format)


class TagsReader:
    def __init__(self, chunk: Chunk) -> None:
        self.chunk: Chunk = chunk

        self.num_tags: int = 0
        self.tags: list[Tag] = []

    def read(self) -> None:
        self.num_tags = tags_chunk_struct.unpack(
            self.chunk.data.read(tags_chunk_struct.size)
        )[0]

        for _ in range(self.num_tags):
            (
                from_frame,
                to_frame,
                loop_animation_direction,
                repeat_n_times,
                tag_red,
                tag_green,
                tag_blue,
            ) = tag_struct.unpack(self.chunk.data.read(tag_struct.size))

            tag_name: str = read_string(self.chunk.data)

            tag: Tag = Tag(
                tag_name,
                from_frame,
                to_frame,
                LoopAnimationDirection(loop_animation_direction),
                repeat_n_times,
                (tag_red, tag_green, tag_blue),
            )
            self.tags.append(tag)

    def to_tags(self) -> list[Tag]:
        return self.tags
