from pathlib import Path

from src.sprite.sprite import Sprite
from src.sprite.sprite_reader import SpriteReader

if __name__ == "__main__":
    file_path: Path = Path("test/files/read-test.aseprite")
    with open(file_path, "rb") as aseprite_file:
        sprite_reader: SpriteReader = SpriteReader(aseprite_file.read())
        sprite_reader.read()

        sprite: Sprite = sprite_reader.to_sprite()
        sprite.print()
