class IndexedPixel:
    def __init__(self, index: int):
        self.index = index


class GrayscalePixel:
    def __init__(self, value: int, alpha: int):
        self.value = value
        self.alpha = alpha


class RGBAPixel:
    def __init__(self, red: int, green: int, blue: int, alpha: int):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
