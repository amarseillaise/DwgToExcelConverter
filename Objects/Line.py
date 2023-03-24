import Objects.Vector
import math


class Line:
    def __init__(self, points):
        self.vector = Objects.Vector.Vector(x_start=float(points[1]),
                                            x_end=float(points[2]),
                                            y_start=float(points[3]),
                                            y_end=float(points[4]),
                                            delta_x=float(points[5]),
                                            delta_y=float(points[6]))
        self.border_side = None
        self.horizontal = False
        self.vertical = False

        if math.isclose(self.vector.x_start, self.vector.x_end, rel_tol=1e-4):
            self.vertical = True
            if self.vector.delta_y < 0:
                temp = self.vector.y_start
                self.vector.y_start = self.vector.y_end
                self.vector.y_end = temp

        elif math.isclose(self.vector.y_start, self.vector.y_end, rel_tol=1e-4):
            self.horizontal = True
            if self.vector.delta_x < 0:
                temp = self.vector.x_start
                self.vector.x_start = self.vector.x_end
                self.vector.x_end = temp
