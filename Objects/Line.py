import logging
import Objects.Vector
import math


class Line:
    def __init__(self, points: list, file_name: str):
        self.border_side: str = ""
        self.file_name = file_name
        self.vertical: bool
        
        self.vector = Objects.Vector.VectorLine(start_point=(float(points[1]), float(points[3])),
                                                end_point=(float(points[2]), float(points[4])),
                                                delta_x=float(points[5]),
                                                delta_y=float(points[6]))


        if math.isclose(self.vector.start_point[0], self.vector.end_point[0], rel_tol=1e-4):
            self.vertical = True
            if self.vector.delta_y < 0:
                temp = self.vector.start_point[1]
                self.vector.start_point = (self.vector.start_point[0], self.vector.end_point[1])
                self.vector.end_point = (self.vector.end_point[0], temp)

        elif math.isclose(self.vector.start_point[1], self.vector.end_point[1], rel_tol=1e-4):
            self.vertical = False
            if self.vector.delta_x < 0:
                temp = self.vector.start_point[0]
                self.vector.start_point = (self.vector.end_point[0], self.vector.start_point[1])
                self.vector.end_point = (temp, self.vector.end_point[1])
        else:
            logging.warning(f"Failed resolve kind of the line (vertical/horizontal) on\n"
                            f"{self.vector.get_start_coordinate()};\n"
                            f"{self.vector.get_end_coordinate()}\n"
                            f"in file {self.file_name}\n")


    def get_border_side(self):
        return self.border_side


    def set_border_side(self, value):
        self.border_side = value
