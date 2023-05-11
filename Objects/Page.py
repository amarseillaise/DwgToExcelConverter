import logging
import math

from Objects.Line import Line
from Objects.Vector import VectorPage, is_equal_coordinate
from Objects.Vector import is_in
from regularExpressions import is_it_form_of_page


def detect_pages(dataset: list[{}, []]):
    lines = list(dataset[0].values())
    content = dataset[1]
    result = []
    iterations_count = 0
    count_of_matched_lines = 0
    matches_border_sides = {
        "left": None,
        "right": None,
        "up": None,
        "down": None,
    }

    try:
        poped_line: Line = lines.pop()
    except IndexError:
        raise Exception("Failed to detect lines")

    while len(lines) != 0:
        for l in range(len(lines)):

            if poped_line.vertical and not lines[l].vertical:  # Case poped line is vertical

                if is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                       lines[l].vector.get_start_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            lines[l].vector.get_start_coordinate(), 1e-4):
                    poped_line.set_border_side("left")

                elif is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                         lines[l].vector.get_end_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            lines[l].vector.get_end_coordinate(), 1e-4):
                    poped_line.set_border_side("right")


            elif not poped_line.vertical and lines[l].vertical:  # Case poped line is horizontal

                if is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                       lines[l].vector.get_start_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            lines[l].vector.get_start_coordinate(), 1e-4):
                    poped_line.set_border_side("down")


                elif is_equal_coordinate(poped_line.vector.get_start_coordinate(),
                                         lines[l].vector.get_end_coordinate(), 1e-4) or \
                        is_equal_coordinate(poped_line.vector.get_end_coordinate(),
                                            lines[l].vector.get_end_coordinate(), 1e-4):
                    poped_line.set_border_side("up")

            if poped_line.get_border_side():
                # if math.isclose(poped_line.vector.get_x1(), 176234, rel_tol=1e-4):
                #     print(1)
                iterations_count = 0
                matches_border_sides[poped_line.get_border_side()] = poped_line
                count_of_matched_lines += len([v for v in matches_border_sides.values() if v])
                poped_line = lines.pop(l)
                if count_of_matched_lines == 3:  # Case last line iteration
                    # if math.isclose(poped_line.vector.get_x1(), 176234, rel_tol=1e-4):
                    #     print(1)
                    for matched_line in matches_border_sides.keys():
                        if not matches_border_sides.get(matched_line):
                            matches_border_sides[matched_line] = poped_line
                            matches_border_sides[matched_line].border_side = matched_line

                    if len(lines) != 0:
                        poped_line = lines.pop(0)
                    result.append(Page(matches_border_sides, content, poped_line.file_name))
                    [matches_border_sides.update({x: None}) for x in matches_border_sides.keys()]  # reset values
                    count_of_matched_lines = 0
                break

        iterations_count += 1
        if iterations_count == 3:
            logging.error(f"Incorrect Line in coordinate:\n"
                          f"start point - ({poped_line.vector.get_start_coordinate()});\n"
                          f"end point - ({poped_line.vector.get_end_coordinate()})\n"
                          f"in file {poped_line.file_name}\n")
            poped_line = lines.pop(0)
            [matches_border_sides.update({x: None}) for x in matches_border_sides.keys()]
            count_of_matched_lines = 0
    return sorted(result, key=lambda i: i.page_number)


class Page:  # I should make a child classes
    def __init__(self, lines: dict, dataset: list, filename: str):

        if len(lines) != 4:
            raise Exception(f"Incorrect count of borders in file {filename}")

        self.borders: dict = lines
        self.vector = VectorPage(start_point=self.borders.get("down").vector.start_point,
                                 end_point=self.borders.get("up").vector.end_point
                                 )
        self.file_name: str = filename
        self.content: list = []
        self.page_number: int = 0
        self.kind: str = ""
        self.additional_info: str = ""
        self.form: str = ""
        self.name: str = ""
        self.name_tech: str = ""
        self.liter: str = ""
        # humans МК
        self.description: str = ""
        self.developer: str = ""
        self.checker: str = ""
        self.approver: str = ""
        self.normalizator: str = ""
        # operations OK
        self.number_of_operation: str = ""
        self.IOT: str = ""
        self.name_of_operation: str = ""
        self.ammo: str = ""

        for obj in dataset:
            if is_in((self.vector.get_x1(), self.vector.get_y1(), self.vector.get_x2(), self.vector.get_y2()),
                     (obj.vector.get_x1(), obj.vector.get_y1())):
                self.content.append(obj)
        self.__detect_headers()
        self.vector.get_fields_coordinate(self.kind, self.form)

    def __detect_headers(self):
        for text in self.content:

            # Searching kind of page
            if is_in((self.borders.get("down").vector.get_x1(), self.borders.get("down").vector.get_y1(),
                      self.borders.get("down").vector.get_x1() + 28, self.borders.get("down").vector.get_y1() + 8.3),
                     (text.vector.get_x1(), text.vector.get_y1())):
                import re
                if re.fullmatch("[оo][кk]", text.text.strip().lower()):  # it needs because technologists incorrect printing kind
                    self.kind = "ОК"
                elif re.fullmatch("[мm][кk]", text.text.strip().lower()):  # it needs because technologists incorrect printing kind
                    self.kind = "МК"
                else:
                    self.kind = text.text

            # Searching number of page
            if is_in((self.borders.get("down").vector.get_x2() - 33, self.borders.get("down").vector.get_y1(),
                      self.borders.get("down").vector.get_x2(), self.borders.get("down").vector.get_y1() + 8.5),
                     (text.vector.get_x1(), text.vector.get_y1())):
                try:
                    self.page_number = int(text.text)
                except ValueError:
                    self.page_number = int(''.join(x for x in text.text if x.isdigit()))

            # Searching info in down-center
            if is_in((self.borders.get("down").vector.get_x1() + 30, self.borders.get("down").vector.get_y1(),
                      self.borders.get("down").vector.get_x2() - 34, self.borders.get("down").vector.get_y1() + 8.3),
                     (text.vector.get_x1(), text.vector.get_y1())):
                self.additional_info = text.text

            # Searching form on right-up part of page
            if is_in((self.borders.get("up").vector.get_x2() - 150, self.borders.get("up").vector.get_y2() - 6,
                      self.borders.get("up").vector.get_x2(), self.borders.get("up").vector.get_y2()),
                     (text.vector.get_x1(), text.vector.get_y1())):
                form_re = is_it_form_of_page(text.text)
                if form_re:
                    self.form = "".join(form_re.split(" "))

        if not self.page_number:
            self.page_number = -1
        if not self.kind:
            self.kind = "Undefined"
        if not self.form:
            self.form = -1

        if self.page_number == -1 and (self.kind == "Undefined" or self.form == -1):
            raise Exception(f"Failed to resolve any headers at page on\n"
                            f"{self.vector.start_point};\n"
                            f"{self.vector.end_point}\n"
                            f"in file {self.file_name}, page {self.page_number}")

        if self.kind.lower() == "тл" \
                or (self.kind.lower() == "мк" and self.form == "2") \
                and (self.kind is None  # continue until find all searching fields
                     or not self.form
                     or not self.developer
                     or not self.checker
                     or not self.approver
                     or not self.normalizator):
            self.__detect_main_info()
            if not self.file_name:
                logging.warning(f"in file {self.file_name} found only ID of process flow")

            if not self.name_tech:
                raise Exception(f"Failed match name and code of tech process on page {self.page_number} "
                                f"in file {self.file_name}")

        self.__get_additional_info()

    def __detect_main_info(self):
        temp_list_N_TC = []  # temp list for handling of name and techname
        temp_list_descr = []  # temp list for handling description
        for text in self.content:
            if is_in((self.borders.get("up").vector.get_x1() + 137, self.borders.get("up").vector.get_y2() - 44,
                      # name and techname
                      self.borders.get("up").vector.get_x2() - 5, self.borders.get("up").vector.get_y2() - 32),
                     (text.vector.get_x1(), text.vector.get_y1())):
                temp_list_N_TC.append(text)

            if is_in((self.borders.get("up").vector.get_x1() + 102, self.borders.get("up").vector.get_y2() - 53,
                      # description
                      self.borders.get("up").vector.get_x2() - 36.7, self.borders.get("up").vector.get_y2() - 44.25),
                     (text.vector.get_x1(), text.vector.get_y1())):
                temp_list_descr.append(text.text)

            if is_in((self.borders.get("up").vector.get_x1() + 28.9, self.borders.get("up").vector.get_y1() - 35.75,
                      # developer
                      self.borders.get("up").vector.get_x1() + 65.3, self.borders.get("up").vector.get_y1() - 31.5),
                     (text.vector.get_x1(), text.vector.get_y1())):
                self.developer = text.text

            if is_in((self.borders.get("up").vector.get_x1() + 28.9, self.borders.get("up").vector.get_y1() - 40,
                      # checker
                      self.borders.get("up").vector.get_x1() + 65.3, self.borders.get("up").vector.get_y1() - 35.75),
                     (text.vector.get_x1(), text.vector.get_y1())):
                self.checker = text.text

            if is_in((self.borders.get("up").vector.get_x1() + 28.9, self.borders.get("up").vector.get_y1() - 44.25,
                      # approver
                      self.borders.get("up").vector.get_x1() + 65.3, self.borders.get("up").vector.get_y1() - 40),
                     (text.vector.get_x1(), text.vector.get_y1())):
                self.approver = text.text

            if is_in((self.borders.get("up").vector.get_x1() + 28.9, self.borders.get("up").vector.get_y1() - 52.75,
                      # normalizator
                      self.borders.get("up").vector.get_x1() + 65.3, self.borders.get("up").vector.get_y1() - 48.5),
                     (text.vector.get_x1(), text.vector.get_y1())):
                self.normalizator = text.text

            if is_in((self.borders.get("up").vector.get_x2() - 36.7, self.borders.get("up").vector.get_y1() - 52.75,
                      # liter
                      self.borders.get("up").vector.get_x2() - 26.3, self.borders.get("up").vector.get_y1() - 44.25),
                     (text.vector.get_x1(), text.vector.get_y1())):
                self.liter = text.text

        self.description = "".join(temp_list_descr)  # get the description

        # handling name and techname
        temp_list_N_TC = sorted(temp_list_N_TC, key=lambda i: i.vector.get_x1())
        temp_list_N_TC = [x.text for x in temp_list_N_TC]
        if len(temp_list_N_TC) > 3:  # if there are more than 3 text objects we can't resolve it
            raise Exception(f"Too much text in list {self.page_number} on upper headers in file {self.file_name}")
        elif len(temp_list_N_TC) == 1:  # case there are just one point of text
            temp_string = " ".join(temp_list_N_TC[0].split())
            temp_list_N_TC = temp_string.split(" ")
            if len(temp_list_N_TC) > 3:
                raise Exception(f"incorrect count of spaces in list {self.page_number} "
                                f"on upper headers in file {self.file_name}")
        if len(temp_list_N_TC) == 2:
            self.name = temp_list_N_TC[0]
            self.name_tech = temp_list_N_TC[1]
        elif len(temp_list_N_TC) == 3:
            self.name = temp_list_N_TC[0]
            self.name_tech = temp_list_N_TC[2]
        elif len(temp_list_N_TC) == 1:
            self.name_tech = temp_list_N_TC[0]

    def __get_additional_info(self):
        for text in self.content:
            # ОК1
            if self.kind.lower() == "ок" and self.form == "1":

                if is_in((self.vector.get_x2() - 21.000, self.vector.get_y2() - 52.7500,  # number_of_operation
                          self.vector.get_x2() - 5.500, self.vector.get_y2() - 44.250),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.number_of_operation = text.text.strip()

                if is_in((self.vector.get_x1() + 18.900, self.vector.get_y2() - 65.5000,  # name_of_operation
                          self.vector.get_x1() + 143.1295, self.vector.get_y2() - 57.000),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.name_of_operation = text.text

                if is_in((self.vector.get_x1() + 143.1295, self.vector.get_y2() - 65.5000,  # IOT
                          self.vector.get_x2() - 26.8198, self.vector.get_y2() - 57.000),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.IOT = text.text

                if is_in((self.vector.get_x1() + 143.1295, self.vector.get_y2() - 77.5000,  # ammo
                          self.vector.get_x2() - 44.2949, self.vector.get_y2() - 69.7594),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.ammo = text.text

            elif self.kind.lower() == "ок" and self.form.lower() in ("1а", "2а"):  # additionally for "OK 2a"
                if is_in((self.vector.get_x2() - 20.000, self.vector.get_y2() - 44.2500,  # number_of_operation
                          self.vector.get_x2() - 5.500, self.vector.get_y2() - 31.500),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.number_of_operation = text.text.strip()

            # ОК2
            elif self.kind.lower() == "ок" and self.form.lower() == "2":

                if is_in((self.vector.get_x2() - 20.000, self.vector.get_y2() - 52.7500,  # number_of_operation
                          self.vector.get_x2() - 5.500, self.vector.get_y2() - 44.2500),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.number_of_operation = text.text.strip()

                if is_in((self.vector.get_x1() + 5.500, self.vector.get_y2() - 65.5000,  # name_of_operation
                          self.vector.get_x1() + 150.500, self.vector.get_y2() - 57.000),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.name_of_operation = text.text

                if is_in((self.vector.get_x2() - 42.500, self.vector.get_y2() - 82.5000,  # IOT
                          self.vector.get_x2() - 5.5000, self.vector.get_y2() - 69.5000),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.IOT = text.text

            else:
                break
