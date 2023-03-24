import math


def is_equal_coordinate(this_coordinate, obj):
    for i in range(len(this_coordinate)):
        if not math.isclose(this_coordinate[i], obj[i], rel_tol=1e-4):
            return False
    return True


def is_in(square, point):
    x = point[0]
    y = point[1]
    x1 = square[0]
    y1 = square[1]
    x2 = square[2]
    y2 = square[3]
    return x1 < x < x2 and y1 < y < y2


class Vector:
    def __init__(self, x=None, y=None, x_start=None, x_end=None, y_start=None, y_end=None, delta_x=None, delta_y=None):
        self.x = x
        self.y = y
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.delta_x = delta_x
        self.delta_y = delta_y

    def get_coordinate(self):
        return self.x, self.y

    def get_start_coordinate(self):
        return self.x_start, self.y_start

    def get_end_coordinate(self):
        return self.x_end, self.y_end
