import Objects.Vector


class DbText:
    def __init__(self, data: list):
        self.text: str = data[0]
        self.height: float = float(data[3])
        self.vector: Objects.Vector = Objects.Vector.Vector(start_point=(float(data[1]), float(data[2])),
                                                            end_point=(float(data[1]), float(data[2])))
