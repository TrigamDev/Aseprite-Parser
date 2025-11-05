from PIL import Image

from src.layer.blend_mode import BlendMode

# https://github.com/kennedy0/aseprite-reader/blob/main/src/aseprite_reader/composite.py


def apply_opacity(image: Image.Image, opacity: int) -> None:
    if opacity == 255:
        return

    scaled_opacity: float = float(opacity) / 255.0

    def __multiply_alpha(pixel: int):
        return int(pixel * scaled_opacity)

    alpha = image.getchannel("A")
    alpha = alpha.point(__multiply_alpha)

    image.putalpha(alpha)


def composite(
    background: Image.Image, foreground: Image.Image, blend_mode: BlendMode
) -> Image.Image:
    match blend_mode:
        case BlendMode.Normal:
            image = _blend_normal(background, foreground)
        case _:
            raise NotImplementedError(f"Blend mode {blend_mode} not implemented")

    return image


def _blend_normal(background: Image.Image, foreground: Image.Image) -> Image.Image:
    background.paste(foreground, (0, 0), mask=foreground)
    return background
