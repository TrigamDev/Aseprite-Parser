from src.tag.loop_animation_direction import LoopAnimationDirection


class Tag:
    def __init__(
        self,
        tag_name: str,
        from_frame: int,
        to_frame: int,
        loop_animation_direction: LoopAnimationDirection,
        repeat_times: int,
        tag_color: tuple[int, int, int],
    ) -> None:
        self.tag_name: str = tag_name

        self.from_frame: int = from_frame
        self.to_frame: int = to_frame

        self.loop_animation_direction: LoopAnimationDirection = loop_animation_direction
        self.repeat_times: int = repeat_times

        self.tag_color: tuple[int, int, int] = tag_color

    def __repr__(self) -> str:
        return f"Tag({self.tag_name}, {self.from_frame}-{self.to_frame})"
