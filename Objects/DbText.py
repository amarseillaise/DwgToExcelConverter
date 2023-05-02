import Objects.Vector


class DbText:
    def __init__(self, data):
        self.text = data[0]
        self.height = float(data[3])
        self.vector = Objects.Vector.Vector(start_point=(float(data[1]), float(data[1])),
                                            end_point=(float(data[2]), float(data[2])))
