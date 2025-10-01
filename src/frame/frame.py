from src.cel.cel import Cel


class Frame:
    def __init__(
        self, frame_index: int, sprite_frame_duration: int, cels: list[Cel]
    ) -> None:
        self.frame_index: int = frame_index
        self.frame_duration: int = sprite_frame_duration

        self.cels: list[Cel] = cels

    def __repr__(self) -> str:
        return f"Frame({self.frame_index}, Cels: {self.cels})"