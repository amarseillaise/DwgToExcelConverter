import Objects.Vector


class DbText:
    def __init__(self, data):
        self.text = data[0]
        self.height = float(data[3])
        self.vector = Objects.Vector.Vector(x=float(data[1]), y=float(data[2]))
