from enum import IntFlag


class SpriteFlags(IntFlag):
    LayerOpacityHasValidValue = 1
    LayerBlendIsValidForGroups = 2
    LayersHaveUUID = 4
    HasGrid = 8
