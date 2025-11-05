from pathlib import Path

from src.sprite.sprite import Sprite
from src.sprite.sprite_reader import SpriteReader

if __name__ == "__main__":
    file_path: Path = Path("test/files/Sillygam!!.ase")
    with open(file_path, "rb") as aseprite_file:
        sprite_reader: SpriteReader = SpriteReader(aseprite_file.read())
        sprite_reader.read()

        sprite: Sprite = sprite_reader.to_sprite()
        # sprite.print()

        sprite.render()
        # for index, frame in enumerate(rendered_sprite):
        # frame.save(f"./out/frame_{index}.png")
