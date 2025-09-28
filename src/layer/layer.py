from src.layer.blend_mode import BlendMode
from src.layer.layer_flags import LayerFlags
from src.layer.layer_type import LayerType

layer_name_byte_start: int = 16
uuid_byte_size: int = 16


class Layer:
    def __init__(
        self,
        uuid: int | None,
        name: str,
        layer_type: LayerType,
        index: int,
        child_level: int,
        # Default dimensions
        default_width: int,
        default_height: int,
        # Display
        opacity: int,
        blend_mode: BlendMode,
        # Flags
        flags: LayerFlags,
    ) -> None:
        self.uuid: int | None = uuid
        self.name: str = name
        self.layer_type: LayerType = layer_type
        self.index: int = index
        self.child_level: int = child_level

        # Default dimensions
        self.default_width: int = default_width
        self.default_height: int = default_height

        # Display
        self.opacity: int = opacity
        self.blend_mode: BlendMode = blend_mode

        # Flags
        self.flags: LayerFlags = flags

    def __repr__(self):
        return f"Layer({self.index}, {self.name})"
