class AsepriteCel:
    def __init__(self):
        self.layer_index: int = 0

        self.x: int = 0
        self.y: int = 0

        self.opacity: int = 0
        self.z_index: int = 0

    def set_layer_index(self, layer_index: int):
        self.layer_index = layer_index

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_opacity(self, opacity):
        self.opacity = opacity

    def set_z_index(self, z_index: int):
        self.z_index = z_index
