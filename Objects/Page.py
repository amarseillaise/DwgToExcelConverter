import logging
import re

from Objects.Line import Line
from Objects.Vector import VectorPage, is_equal_coordinate
from Objects.Vector import is_in
from regularExpressions import is_it_form_of_page


def detect_pages(dataset: list[[], []]):
    lines = list(dataset[0])
    up_lines = []
    content: list = dataset[1]
    result = []

    for dbtext in content:

        if is_it_form_of_page(dbtext.text):
            for line in lines:
                if is_in((line.vector.get_x1(), line.vector.get_y1() - 8.00000,
                          line.vector.get_x2(), line.vector.get_y2()),
                         dbtext.vector.get_start_coordinate()):
                    line.set_border_side("up")
                    up_lines.append(lines.pop(lines.index(line)))
                    break
            if not line.get_border_side():
                logging.error(f"Failed to detect which line relate text {dbtext.text} in coordinate\n"
                              f"({dbtext.vector.get_x1()}; {dbtext.vector.get_y2()})\n"
                              f"in file {line.file_name}\n")

    for up_line in up_lines:
        for down_line in lines:
            if is_in((up_line.vector.get_x1() - 0.50000, up_line.vector.get_y1() - 220.00000,
                      up_line.vector.get_x1() + 0.50000, up_line.vector.get_y1() - 209.20000),
                     down_line.vector.get_start_coordinate()):
                down_line.set_border_side("down")
                result.append(Page({
                    "left": Line([None, up_line.vector.get_x1(), up_line.vector.get_x1(),
                                  down_line.vector.get_y1(), up_line.vector.get_y1(), 0, 1], up_line.file_name),
                    "right": Line([None, up_line.vector.get_x2(), up_line.vector.get_x2(),
                                   down_line.vector.get_y2(), up_line.vector.get_y2(), 0, 1], up_line.file_name),
                    "up": up_line,
                    "down": lines.pop(lines.index(down_line)),
                }, content, up_line.file_name))
                break

    if len(lines) > 1:
        logging.error(f"Failed to detect below down lines:\n"
                      f"{[(x.vector.get_start_coordinate(), x.vector.get_end_coordinate()) for x in lines]}\n"
                      f"in file {line.file_name}\n")

    return sorted(result, key=lambda x: x.page_number)


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

        self.borders["left"].set_border_side("left")
        self.borders["right"].set_border_side("right")

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
                if re.fullmatch("[оo][кk]",
                                text.text.strip().lower()):  # it needs because technologists incorrect printing kind
                    self.kind = "ОК"
                elif re.fullmatch("[мm][кk]",
                                  text.text.strip().lower()):  # it needs because technologists incorrect printing kind
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
            logging.warning(f"Failed to resolve any headers at page on\n"
                          f"{self.vector.start_point};\n"
                          f"{self.vector.end_point}\n"
                          f"in file {self.file_name}, page {self.page_number}\n")

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
                logging.warning(f"Failed match name and code of tech process on page {self.page_number} "
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

            elif str(self.kind).lower() == "ок" and str(self.form).lower() in ("1а", "2а"):  # additionally for "OK 2a"
                if is_in((self.vector.get_x2() - 20.000, self.vector.get_y2() - 44.2500,  # number_of_operation
                          self.vector.get_x2() - 5.500, self.vector.get_y2() - 31.500),
                         (text.vector.get_x1(), text.vector.get_y1())):
                    self.number_of_operation = text.text.strip()

            # ОК2
            elif str(self.kind).lower() == "ок" and str(self.form).lower() == "2":

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
