from enum import IntFlag


class LayerFlags(IntFlag):
    Visible = 1
    Editable = 2
    LockMovement = 4
    Background = 8
    PreferLinkedCells = 16
    DisplayLayerGroupCollapsed = 32
    ReferenceLayer = 64
