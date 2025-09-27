from typing import Self

from src.sprite.tag.loop_animation_direction import LoopAnimationDirection
from src.util import read_bytes, read_string, string_byte_size


class Tag:
    def __init__(self):
        self.sprite = None

        self.tag_name: str = ""

        self.from_frame: int = 0
        self.to_frame: int = 0

        self.loop_animation_direction: LoopAnimationDirection = (
            LoopAnimationDirection.Unknown
        )
        self.repeat_times: int = 0

        self.tag_color: tuple[int, int, int] = (0, 0, 0)

    def __repr__(self):
        return f"Tag({self.tag_name}, {self.from_frame}-{self.to_frame})"

    def read_from_chunk(self, chunk_size: int, chunk_data: bytes) -> Self:
        self.from_frame = read_bytes(chunk_data, 0, 2, "i")
        self.to_frame = read_bytes(chunk_data, 2, 2, "i")

        self.loop_animation_direction = LoopAnimationDirection(
            read_bytes(chunk_data, 4, 1, "i")
        )
        self.repeat_times = read_bytes(chunk_data, 5, 2, "i")

        tag_red = read_bytes(chunk_data, 13, 1, "i")
        tag_green = read_bytes(chunk_data, 14, 1, "i")
        tag_blue = read_bytes(chunk_data, 15, 1, "i")
        self.tag_color = (tag_red, tag_green, tag_blue)

        self.tag_name = read_string(chunk_data, 17)

        return self
