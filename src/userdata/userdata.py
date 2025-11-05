from typing import Any


class UserData:
    def __init__(
        self,
        string: str | None,
        color: tuple[int, int, int, int] | None,
        property_maps: list[dict[str, Any]] | None,
    ):
        self.string = string
        self.color = color
        self.property_maps = property_maps

    def __repr__(self):
        string_str = f'"{self.string}"' if self.string else "None"
        color_str = f"{self.color}" if self.color else "None"
        property_maps_str = f"{self.property_maps}" if self.property_maps else "None"
        return f"UserData(string:{string_str} color:{color_str} property_maps:{property_maps_str})"
