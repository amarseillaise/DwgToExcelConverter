from Objects.Vector import is_equal_coordinate
from Objects.Page import Page


def detect_pages(dataset):
    lines = dataset[0]
    content = dataset[1]
    result = []
    pre_result = []
    iterations_count = 0

    try:
        poped_line = lines.pop(0)
    except IndexError:
        return []

    while len(lines) != 0:
        for l in range(len(lines)):
            current_line = lines[l]

            if poped_line.vertical and current_line.horizontal:  # Case poped line is vertical

                if is_equal_coordinate(poped_line.vector.get_start_coordinate(), current_line.vector.get_start_coordinate()) or \
                    is_equal_coordinate(poped_line.vector.get_end_coordinate(), current_line.vector.get_start_coordinate()):
                    poped_line.border_side = "Left"

                elif is_equal_coordinate(poped_line.vector.get_start_coordinate(), current_line.vector.get_end_coordinate()) or \
                    is_equal_coordinate(poped_line.vector.get_end_coordinate(), current_line.vector.get_end_coordinate()):
                    poped_line.border_side = "Right"


            elif poped_line.horizontal and current_line.vertical:  # Case poped line is horizontal

                if is_equal_coordinate(poped_line.vector.get_start_coordinate(), current_line.vector.get_start_coordinate()) or \
                    is_equal_coordinate(poped_line.vector.get_end_coordinate(), current_line.vector.get_start_coordinate()):
                    poped_line.border_side = "Down"

                elif is_equal_coordinate(poped_line.vector.get_start_coordinate(), current_line.vector.get_end_coordinate()) or \
                    is_equal_coordinate(poped_line.vector.get_end_coordinate(), current_line.vector.get_end_coordinate()):
                    poped_line.border_side = "Up"

            if poped_line.border_side is not None:
                iterations_count = 0
                pre_result.append(poped_line)
                poped_line = lines.pop(l)
                if len(pre_result) == 3:  # Case last line iteration
                    matches_border_sides = pre_result[0].border_side, pre_result[1].border_side, pre_result[2].border_side
                    if "Up" not in matches_border_sides:
                        poped_line.border_side = "Up"
                    elif "Down" not in matches_border_sides:
                        poped_line.border_side = "Down"
                    elif "Right" not in matches_border_sides:
                        poped_line.border_side = "Right"
                    elif "Left" not in matches_border_sides:
                        poped_line.border_side = "Left"
                    else:
                        raise Exception("Failed to detect last line")
                    pre_result.append(poped_line)
                    if len(lines) != 0:
                        poped_line = lines.pop(0)
                    result.append(Page(pre_result, content))
                    pre_result.clear()
                break

        iterations_count += 1
        if iterations_count == 3:
            raise Exception(f"Incorrect Line in coordinate:\n"
                            f"start point - ({poped_line.vector.x_start}; {poped_line.vector.y_start})\n"
                            f"end point - ({poped_line.vector.x_end}; {poped_line.vector.y_end})")
    print(len(result))
    return result
