from pathlib import Path

from src.sprite.sprite import Sprite

if __name__ == "__main__":
    aseprite_file = Sprite().read_from_path(Path("test/files/Sillygam!!.ase"))
