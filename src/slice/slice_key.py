class SliceKey:
    def __init__(
        self,
        frame_index: int,
        x: int,
        y: int,
        width: int,
        height: int,
        # 9-patch
        center_x: int,
        center_y: int,
        center_width: int,
        center_height: int,
        # Pivot
        pivot_x: int,
        pivot_y: int,
    ) -> None:
        self.frame_index: int = frame_index

        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

        # 9-patch
        self.center_x: int = center_x
        self.center_y: int = center_y
        self.center_width: int = center_width
        self.center_height: int = center_height

        # Pivot
        self.pivot_x: int = pivot_x
        self.pivot_y: int = pivot_y

    def __repr__(self) -> str:
        return f"SliceKey({self.frame_index}, {self.x}x, {self.y}y, {self.width}x{self.height} {self.x}c_x, {self.y}c_y, {self.center_width}x{self.center_height}, {self.pivot_x}p_x, {self.pivot_y}p_y)"
