from pathlib import Path

from src.aseprite_file import AsepriteFile

if __name__ == "__main__":
    aseprite_file = AsepriteFile().read_from_path(Path("test/files/Sillygam!!.ase"))
