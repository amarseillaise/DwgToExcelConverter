import math


def is_equal_coordinate(first_coordinate: tuple, second_coordinate: tuple, accuracy: float):
    for i in range(len(first_coordinate)):
        if not math.isclose(first_coordinate[i], second_coordinate[i], rel_tol=accuracy):
            return False
    return True


def is_in(square: tuple, point: tuple):
    x = point[0]
    y = point[1]
    x1 = square[0]
    y1 = square[1]
    x2 = square[2]
    y2 = square[3]
    return x1 < x < x2 and y1 < y < y2


class Vector:
    def __init__(self, start_point: tuple, end_point: tuple):
        self.start_point = start_point
        self.end_point = end_point


class VectorLine(Vector):
    def __init__(self, start_point: tuple, end_point: tuple, delta_x: float, delta_y: float):
        super().__init__(start_point, end_point)
        self.delta_x = delta_x
        self.delta_y = delta_y
        
        
class VectorPage(Vector):
    def __init__(self, start_point: tuple, end_point: tuple):
        super().__init__(start_point, end_point)
        self.fields_coordinate = []
        
        
    def get_fields_coordinate(self, kind: str, form: str):
        def get_bo3_fields():
            X_START = self.start_point[0] + 5.291000
            X_END = self.end_point[0] - 5.3652
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 67.8069, X_END, self.end_point[0] - 60.8805))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 75.1951, X_END, self.end_point[0] - 67.8069))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 83.2374, X_END, self.end_point[0] - 75.1951))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 91.2797, X_END, self.end_point[0] - 83.2374))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 99.4567, X_END, self.end_point[0] - 91.2797))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 107.6337, X_END, self.end_point[0] - 99.4567))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 123.9877, X_END, self.end_point[0] - 107.6337))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 132.1647, X_END, self.end_point[0] - 123.9877))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 140.3417, X_END, self.end_point[0] - 132.1647))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 148.5187, X_END, self.end_point[0] - 140.3417))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 156.6957, X_END, self.end_point[0] - 148.5187))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 164.8727, X_END, self.end_point[0] - 156.6957))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 173.0497, X_END, self.end_point[0] - 164.8727))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 181.2267, X_END, self.end_point[0] - 173.0497))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 189.4037, X_END, self.end_point[0] - 181.2267))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 197.4699, X_END, self.end_point[0] - 189.4037))
            
        def get_bo3a_fields():
            X_START = self.start_point[0] + 5.50000
            X_END = self.end_point[0] - 5.50000
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 65.0000, X_END, self.end_point[0] - 56.000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 74.0000, X_END, self.end_point[0] - 65.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 82.5000, X_END, self.end_point[0] - 74.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 91.0000, X_END, self.end_point[0] - 82.5000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 99.5000, X_END, self.end_point[0] - 91.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 108.0000, X_END, self.end_point[0] - 99.5000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 116.5000, X_END, self.end_point[0] - 108.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 125.0000, X_END, self.end_point[0] - 116.5000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 133.5000, X_END, self.end_point[0] - 125.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 142.0000, X_END, self.end_point[0] - 133.5000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 155.5000, X_END, self.end_point[0] - 142.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 159.0000, X_END, self.end_point[0] - 155.5000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 167.5000, X_END, self.end_point[0] - 159.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 176.0000, X_END, self.end_point[0] - 167.5000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 184.9780, X_END, self.end_point[0] - 176.0000))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 192.6254, X_END, self.end_point[0] - 184.9780))
            self.fields_coordinate.append(
                (X_START, self.start_point[0] - 201.1254, X_END, self.end_point[0] - 192.6254))
            
            
        FIELDS_DISTANT = 8.50000
        X_START = self.start_point[0] + 5.50000
        X_END = self.end_point[0] - 5.50000

        # МК
        if kind.lower() == "мк" and form == "2":
            fields = 16
            y_start = self.end_point[1] - 75.50000
            y_end = self.end_point[1] - 68.25000
        elif kind.lower() == "мк" and (form.lower() == "1б" or form.lower() == "2а"):
            fields = 17
            y_start = self.end_point[1] - 65.50000
            y_end = self.end_point[1] - 57.00000
        # ОК
        elif kind.lower() == "ок" and form == "1":
            fields = 13
            y_start = self.end_point[1] - 95.25000
            y_end = self.end_point[1] - 86.75000
        elif kind.lower() == "ок" and form == "1а":
            fields = 17
            y_start = self.end_point[1] - 65.00000
            y_end = self.end_point[1] - 56.00000
        elif kind.lower() == "ок" and form == "2":
            fields = 13
            y_start = self.end_point[1] - 99.50000
            y_end = self.end_point[1] - 91.00000
        elif kind.lower() == "ок" and form == "2а":
            fields = 18
            y_start = self.end_point[1] - 57.00000
            y_end = self.end_point[1] - 48.50000
        # BO
        elif kind.lower() == "во" and form == "3":
            get_bo3_fields()
            return
        elif kind.lower() == "во" and form == "3а":
            get_bo3a_fields()
            return
        # BM and Technologist passport
        elif kind.lower() in ("Undefined", "вм") and form == "2":
            fields = 15
            y_start = self.end_point[1] - 82.50000
            y_end = self.end_point[1] - 74.00000
        elif kind.lower() in ("Undefined", "вм") and form == "2а":
            fields = 16
            y_start = self.end_point[1] - 74.00000
            y_end = self.end_point[1] - 65.50000
        else:
            return Exception("Failed to resolve fields")

        for i in range(fields):
            coefficient = FIELDS_DISTANT * float(i) - 1.50000 if (kind.lower() == "мк" and form == "2") else FIELDS_DISTANT * float(i)

            #  handling case when page is MK2 because there are no standard dist between fields
            if kind.lower() == "мк" and form == "2" and i == 0:
                self.fields_coordinate.append((X_START, y_start, X_END, y_end))
            elif kind.lower() == "мк" and form == "2" and i == 1:
                self.fields_coordinate.append((X_START, y_start - 7.00000, X_END, y_end - 7.25000))
            elif kind.lower() == "мк" and form == "2" and i == 2:
                self.fields_coordinate.append((X_START, y_start - 15.50000, X_END, y_end - 14.25000))
            elif kind.lower() == "мк" and form == "2":
                self.fields_coordinate.append((X_START, y_start - coefficient, X_END, y_end - coefficient + 1.25))
            #
            else:
                self.fields_coordinate.append((X_START, y_start - coefficient, X_END, y_end - coefficient))
                       