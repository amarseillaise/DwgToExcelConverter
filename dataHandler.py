import logging
from Objects.Vector import is_equal_coordinate, is_in
from Objects.ProcessFlow import *
from Objects.Page import Page
from RegularExpressions import *


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

                if is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                       current_line.vector.get_start_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            current_line.vector.get_start_coordinate(), 1e-4):
                    poped_line.border_side = "Left"

                elif is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                         current_line.vector.get_end_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            current_line.vector.get_end_coordinate(), 1e-4):
                    poped_line.border_side = "Right"


            elif poped_line.horizontal and current_line.vertical:  # Case poped line is horizontal

                if is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                       current_line.vector.get_start_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            current_line.vector.get_start_coordinate(), 1e-4):
                    poped_line.border_side = "Down"

                elif is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                         current_line.vector.get_end_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            current_line.vector.get_end_coordinate(), 1e-4):
                    poped_line.border_side = "Up"

            if poped_line.border_side is not None:
                iterations_count = 0
                pre_result.append(poped_line)
                poped_line = lines.pop(l)
                if len(pre_result) == 3:  # Case last line iteration
                    matches_border_sides = pre_result[0].border_side, pre_result[1].border_side, pre_result[
                        2].border_side
                    if "Up" not in matches_border_sides:
                        poped_line.border_side = "Up"
                    elif "Down" not in matches_border_sides:
                        poped_line.border_side = "Down"
                    elif "Right" not in matches_border_sides:
                        poped_line.border_side = "Right"
                    elif "Left" not in matches_border_sides:
                        poped_line.border_side = "Left"
                    else:
                        raise Exception(f"Failed to detect last line in file {poped_line.file_name}")
                    pre_result.append(poped_line)
                    if len(lines) != 0:
                        poped_line = lines.pop(0)
                    result.append(Page(pre_result, content, pre_result[0].file_name))
                    pre_result.clear()
                break

        iterations_count += 1
        if iterations_count == 3:
            raise Exception(f"Incorrect Line in coordinate:\n"
                            f"start point - ({poped_line.vector.x_start}; {poped_line.vector.y_start})\n"
                            f"end point - ({poped_line.vector.x_end}; {poped_line.vector.y_end})"
                            f" in file {poped_line.file_name}")
    return sorted(result, key=lambda i: i.page_number)


def detect_operations(pf, pages):
    #  detect operations dataset in fields via vector's coordinate
    fields = []
    for page in pages:
        if page.kind.lower() == "мк":
            for i in range(len(page.vector.fields_coordinate)):
                temp_list = []
                for text in page.content:
                    if is_in(page.vector.fields_coordinate[i], text.vector.get_coordinate()) \
                            and not is_it_number_of_field(text.text):
                        temp_list.append(text)
                temp_list = sorted(temp_list, key=lambda x: x.vector.x)
                if len(temp_list) > 0:
                    fields.append("".join(x.text + "  " for x in temp_list))

    #  find operations via regexp r"\s[0123]\d\d\s"
    unresolved = ""
    previous_field = None
    for field in fields:
        if is_it_new_item(field, r"\s[0123]\d\d\s"):
            # in case first element of list
            if previous_field is None:
                previous_field = field
                continue
            #
            o = __split_operation_field(previous_field)
            pf.operations[o.number] = o
            previous_field = field
        elif previous_field is not None:
            previous_field += " " + field
        else:
            unresolved += field

    try:
        o = __split_operation_field(previous_field)
        pf.operations[o.number] = o  # in case final element of list
    except TypeError:
        pf.unresolved_text.append(UnresolvedText("Somewhere in MK", unresolved))


def __split_operation_field(string):
    m = re.search(r"\s[0123]\d\d\s", string)

    number = string[m.start():m.end()]
    description = string[m.end():]
    tsekh = string[:m.start()].replace("А", "")
    return Operation((number.strip(), description.strip(), tsekh.strip()))


def detect_shifts(pf, pages):  # Очень плохой код - спагетии. Переписать
    #  detect operations dataset in fields via vector's coordinate
    fields = []
    previous_page = pages[0]
    for page in pages:
        if page.kind.lower() == "ок":
            if previous_page.page_number != pages[0].page_number \
                    and page.number_of_operation != previous_page.number_of_operation:

                #  find operations via regexp r"(?:^|О) +\d{1,2}\.? "
                unresolved = ""
                previous_field = None
                for field in fields:
                    if is_it_new_item(field, r"(?:^|(?: |^)[оО])(?: +|^)\d{1,2}\.? "):
                        # in case first element of list
                        if previous_field is None:
                            previous_field = field
                            continue
                        #
                        s = __split_shift_field(previous_field)
                        try:
                            pf.operations[previous_page.number_of_operation].shifts.append(s)
                        except KeyError:
                            pf.operations[previous_page.number_of_operation] = Operation(
                                (previous_page.number_of_operation, previous_page.name_of_operation, ""))
                            logging.warning(
                                f"In file {pf.file_name} operation #{previous_page.number_of_operation} not found in MK")
                            operation = pf.operations[previous_page.number_of_operation]
                            operation.IOT = previous_page.IOT
                            operation.ammo = previous_page.ammo
                            pf.operations[previous_page.number_of_operation].shifts.append(s)
                        previous_field = field
                    elif previous_field is not None:
                        previous_field += " " + field
                    else:
                        unresolved += field

                s = __split_shift_field(previous_field)
                pf.operations[previous_page.number_of_operation].shifts.append(s)  # in case final element of list

                if unresolved != "":
                    pf.unresolved_text.append(UnresolvedText(previous_page.number_of_operation, unresolved))

                fields.clear()

            # in case it's first page of operation we get headers
            if page.form in ("1", "2"):
                try:
                    operation = pf.operations[page.number_of_operation]
                except KeyError:
                    pf.operations[page.number_of_operation] = Operation((page.number_of_operation, page.name_of_operation, ""))
                    logging.warning(f"In file {pf.file_name} operation #{page.number_of_operation} not found in MK")
                    operation = pf.operations[page.number_of_operation]
                operation.IOT = page.IOT
                operation.ammo = page.ammo
            #

            for i in range(len(page.vector.fields_coordinate)):
                temp_list = []
                for text in page.content:
                    if is_in(page.vector.fields_coordinate[i], text.vector.get_coordinate()) \
                            and not is_it_number_of_field(text.text):
                        temp_list.append(text)
                temp_list = sorted(temp_list, key=lambda x: x.vector.x)
                if len(temp_list) > 0:
                    fields.append("".join(x.text + "  " for x in temp_list))

            previous_page = page

    previous_field = None
    for field in fields:  # repeat for the last operation
        if is_it_new_item(field, r"(?:^|(?: |^)[оО])(?: +|^)\d{1,2}\.? "):
            # in case first element of list
            if previous_field is None:
                previous_field = field
                continue
            #
            s = __split_shift_field(previous_field)
            try:
                pf.operations[previous_page.number_of_operation].shifts.append(s)
            except KeyError:
                pf.operations[previous_page.number_of_operation] = Operation(
                    (previous_page.number_of_operation, previous_page.name_of_operation, ""))
                logging.warning(
                    f"In file {pf.file_name} operation #{previous_page.number_of_operation} not found in MK")
                operation = pf.operations[previous_page.number_of_operation]
                operation.IOT = previous_page.IOT
                operation.ammo = previous_page.ammo
                pf.operations[previous_page.number_of_operation].shifts.append(s)
            previous_field = field
        elif previous_field is not None:
            previous_field += " " + field
        else:
            unresolved += field

    s = __split_shift_field(previous_field)
    pf.operations[previous_page.number_of_operation].shifts.append(s)  # in case final element of list

    if unresolved != "":
        pf.unresolved_text.append(UnresolvedText(previous_page.number_of_operation, unresolved))

    fields.clear()


def __split_shift_field(string):
    s = re.search(r"(?:^|(?: |^)[оО])(?: +|^)\d{1,2}\.? ", string)

    # trying to detect tools
    tools = []

    tool_matches = re.finditer(r" {2,}[ТМБPР] {2,}\S", s.string)
    start_end_positions = [(x.start(), x.end()) for x in tool_matches]
    start_about_tools_pos = -1 if len(start_end_positions) == 0 else start_end_positions[0][0]

    for i in range(len(start_end_positions)):
        try:
            start_pos_of_next_kind = start_end_positions[i + 1][0]
        except IndexError:
            start_pos_of_next_kind = -1
        iterating_string = string[start_end_positions[i][1] - 1:start_pos_of_next_kind]
        for tool in iterating_string.strip().split(";"):
            if len(tool) > 2:
                tools.append(Tool(tool.strip()))
    #

    # trying to detect control percent
    percent_match = re.search(r"\d{1,3} *%", string)
    percent = string[percent_match.start():percent_match.end()].replace(" ", "") if percent_match is not None else None
    #

    number = string[s.start():s.end()]
    try:
        description = string[s.end():start_about_tools_pos]
    except AttributeError:
        description = string[s.end():]
    return Shift(number.replace(".", "").replace("О", "").strip(), description.strip(), tools, percent)
