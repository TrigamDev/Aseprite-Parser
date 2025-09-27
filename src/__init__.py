from pathlib import Path

from src.sprite.sprite import Sprite

if __name__ == "__main__":
    sprite = Sprite().read_from_path(Path("test/files/large-palette-test.aseprite"))
