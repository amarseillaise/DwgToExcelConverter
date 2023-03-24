from Objects.Vector import Vector
from Objects.Vector import is_in


class Page:
    def __init__(self, lines, dataset):
        if len(lines) != 4:
            raise Exception("Incorrect count of borders")

        for border in lines:
            match border.border_side:
                case "Up":
                    self.up_border = border
                case "Down":
                    self.down_border = border
                case "Left":
                    self.left_border = border
                case "Right":
                    self.right_border = border

        self.vector = Vector(x_start=self.down_border.vector.x_start,
                             y_start=self.down_border.vector.y_start,
                             x_end=self.up_border.vector.x_end,
                             y_end=self.up_border.vector.y_end)
        self.content = []

        for obj in dataset:
            if is_in((self.vector.x_start, self.vector.y_start, self.vector.x_end, self.vector.y_end),
                     (obj.vector.x, obj.vector.y)):
                self.content.append(obj)
