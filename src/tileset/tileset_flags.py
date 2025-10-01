from enum import IntFlag


class TilesetFlags(IntFlag):
    LinksToExternalFile = 1
    IncludeTilesFromExternalFile = 2
    UseID0AsEmptyTile = 4
    MatchModifiedTilesWithHorizontalFlippedVersion = 8
    MatchModifiedTilesWithVerticalFlippedVersion = 16
    MatchModifiedTilesWithDiagonalFlippedVersion = 32
