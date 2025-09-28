from src.layer.blend_mode import BlendMode
from src.layer.layer import Layer
from src.layer.layer_flags import LayerFlags
from src.layer.layer_type import LayerType


class TilemapLayer(Layer):
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
        # Tileset
        tileset_index: int,
        # Flags
        flags: LayerFlags,
    ) -> None:
        super().__init__(
            uuid,
            name,
            layer_type,
            index,
            child_level,
            default_width,
            default_height,
            opacity,
            blend_mode,
            flags,
        )

        # Tileset
        self.tileset_index: int = tileset_index

    def __repr__(self):
        return f"TilemapLayer({self.index}, {self.name}, {self.tileset_index})"
