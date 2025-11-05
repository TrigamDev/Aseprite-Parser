from typing import TYPE_CHECKING
from PIL import Image
from src.cel.cel import Cel
from src.layer.blend_mode import BlendMode
from src.utils.composite import apply_opacity, composite


if TYPE_CHECKING:
    from src.sprite.sprite import Sprite


class Frame:
    def __init__(
        self, frame_index: int, sprite_frame_duration: int, cels: list[Cel]
    ) -> None:
        self.frame_index: int = frame_index
        self.frame_duration: int = sprite_frame_duration

        self.cels: list[Cel] = cels

    def __repr__(self) -> str:
        return f"Frame({self.frame_index}, Cels: {self.cels})"

    def render(self, sprite: "Sprite") -> Image.Image:
        frame_image = Image.new("RGBA", (sprite.width, sprite.height))
        sorted_cels = sorted(self.cels, key=lambda cel: cel.layer_index)

        for index, cel in enumerate(sorted_cels):
            cel_image: Image.Image = Image.new("RGBA", (sprite.width, sprite.height))
            cel_image.paste(cel.render(self), (cel.x, cel.y))

            cel_image.save(f"./out/frame_{self.frame_index}_cel_{index}.png")

            layer_image = cel_image.copy()
            layer = sprite.layers[cel.layer_index]
            apply_opacity(layer_image, layer.opacity)

            layer_image.save(f"./out/frame_{self.frame_index}_layer_{index}.png")

            composite(frame_image, layer_image, BlendMode.Normal)

        frame_image.save(f"./out/frame_{self.frame_index}.png")

        return frame_image
