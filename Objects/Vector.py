import math


def is_equal_coordinate(this_coordinate, obj, accuracy):
    for i in range(len(this_coordinate)):
        if not math.isclose(this_coordinate[i], obj[i], rel_tol=accuracy):
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
        self.fields_coordinate = []

    def get_fields_coordinate(self, kind, form):
        FIELDS_DISTANT = 8.50000
        X_START = self.x_start + 5.50000
        X_END = self.x_end - 5.50000

        # МК
        if kind.lower() == "мк" and form == "2":
            fields = 16
            y_start = self.y_end - 75.50000
            y_end = self.y_end - 68.25000
        elif kind.lower() == "мк" and (form.lower() == "1б" or form.lower() == "2а"):
            fields = 17
            y_start = self.y_end - 65.50000
            y_end = self.y_end - 57.00000
        # ОК
        elif kind.lower() == "ок" and form == "1":
            fields = 13
            y_start = self.y_end - 95.25000
            y_end = self.y_end - 86.75000
        elif kind.lower() == "ок" and form == "1а":
            fields = 17
            y_start = self.y_end - 65.00000
            y_end = self.y_end - 56.00000
        elif kind.lower() == "ок" and form == "2":
            fields = 13
            y_start = self.y_end - 99.50000
            y_end = self.y_end - 91.00000
        elif kind.lower() == "ок" and form == "2а":
            fields = 18
            y_start = self.y_end - 57.00000
            y_end = self.y_end - 48.50000
        # BO
        elif kind.lower() == "во" and form == "3":
            self.__get_bo3_fields()
            return
        elif kind.lower() == "во" and form == "3а":
            self.__get_bo3a_fields()
            return
        # BM and Technologist passport
        elif kind.lower() in ("Undefined", "вм") and form == "2":
            fields = 15
            y_start = self.y_end - 82.50000
            y_end = self.y_end - 74.00000
        elif kind.lower() in ("Undefined", "вм") and form == "2а":
            fields = 16
            y_start = self.y_end - 74.00000
            y_end = self.y_end - 65.50000
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



    def get_coordinate(self):
        return self.x, self.y

    def get_start_coordinate(self):
        return self.x_start, self.y_start

    def get_end_coordinate(self):
        return self.x_end, self.y_end

    def __get_bo3_fields(self):
        X_START = self.x_start + 5.291000
        X_END = self.x_end - 5.3652
        self.fields_coordinate.append((X_START, self.x_start - 67.8069, X_END, self.x_end - 60.8805))
        self.fields_coordinate.append((X_START, self.x_start - 75.1951, X_END, self.x_end - 67.8069))
        self.fields_coordinate.append((X_START, self.x_start - 83.2374, X_END, self.x_end - 75.1951))
        self.fields_coordinate.append((X_START, self.x_start - 91.2797, X_END, self.x_end - 83.2374))
        self.fields_coordinate.append((X_START, self.x_start - 99.4567, X_END, self.x_end - 91.2797))
        self.fields_coordinate.append((X_START, self.x_start - 107.6337, X_END, self.x_end - 99.4567))
        self.fields_coordinate.append((X_START, self.x_start - 123.9877, X_END, self.x_end - 107.6337))
        self.fields_coordinate.append((X_START, self.x_start - 132.1647, X_END, self.x_end - 123.9877))
        self.fields_coordinate.append((X_START, self.x_start - 140.3417, X_END, self.x_end - 132.1647))
        self.fields_coordinate.append((X_START, self.x_start - 148.5187, X_END, self.x_end - 140.3417))
        self.fields_coordinate.append((X_START, self.x_start - 156.6957, X_END, self.x_end - 148.5187))
        self.fields_coordinate.append((X_START, self.x_start - 164.8727, X_END, self.x_end - 156.6957))
        self.fields_coordinate.append((X_START, self.x_start - 173.0497, X_END, self.x_end - 164.8727))
        self.fields_coordinate.append((X_START, self.x_start - 181.2267, X_END, self.x_end - 173.0497))
        self.fields_coordinate.append((X_START, self.x_start - 189.4037, X_END, self.x_end - 181.2267))
        self.fields_coordinate.append((X_START, self.x_start - 197.4699, X_END, self.x_end - 189.4037))

    def __get_bo3a_fields(self):
        X_START = self.x_start + 5.50000
        X_END = self.x_end - 5.50000
        self.fields_coordinate.append((X_START, self.x_start - 65.0000, X_END, self.x_end - 56.000))
        self.fields_coordinate.append((X_START, self.x_start - 74.0000, X_END, self.x_end - 65.0000))
        self.fields_coordinate.append((X_START, self.x_start - 82.5000, X_END, self.x_end - 74.0000))
        self.fields_coordinate.append((X_START, self.x_start - 91.0000, X_END, self.x_end - 82.5000))
        self.fields_coordinate.append((X_START, self.x_start - 99.5000, X_END, self.x_end - 91.0000))
        self.fields_coordinate.append((X_START, self.x_start - 108.0000, X_END, self.x_end - 99.5000))
        self.fields_coordinate.append((X_START, self.x_start - 116.5000, X_END, self.x_end - 108.0000))
        self.fields_coordinate.append((X_START, self.x_start - 125.0000, X_END, self.x_end - 116.5000))
        self.fields_coordinate.append((X_START, self.x_start - 133.5000, X_END, self.x_end - 125.0000))
        self.fields_coordinate.append((X_START, self.x_start - 142.0000, X_END, self.x_end - 133.5000))
        self.fields_coordinate.append((X_START, self.x_start - 155.5000, X_END, self.x_end - 142.0000))
        self.fields_coordinate.append((X_START, self.x_start - 159.0000, X_END, self.x_end - 155.5000))
        self.fields_coordinate.append((X_START, self.x_start - 167.5000, X_END, self.x_end - 159.0000))
        self.fields_coordinate.append((X_START, self.x_start - 176.0000, X_END, self.x_end - 167.5000))
        self.fields_coordinate.append((X_START, self.x_start - 184.9780, X_END, self.x_end - 176.0000))
        self.fields_coordinate.append((X_START, self.x_start - 192.6254, X_END, self.x_end - 184.9780))
        self.fields_coordinate.append((X_START, self.x_start - 201.1254, X_END, self.x_end - 192.6254))
