import logging
from Objects.Vector import Vector
from Objects.Vector import is_in
from RegularExpressions import detect_form_via_re


class Page:  # I should make a child classes
    def __init__(self, lines, dataset, filename):
        self.file_name = filename
        self.up_border = None
        self.down_border = None
        self.left_border = None
        self.right_border = None
        self.vector = None
        self.content = []
        self.page_number = None
        self.kind = None
        self.additional_info = None
        self.form = None
        self.name = None
        self.name_tech = None
        self.liter = None
        # humans МК
        self.description = None
        self.developer = None
        self.checker = None
        self.approver = None
        self.normalizator = None
        # operations OK
        self.number_of_operation = None
        self.IOT = None
        self.name_of_operation = None
        self.ammo = None

        if len(lines) != 4:
            raise Exception(f"Incorrect count of borders in file {filename}")

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

        for obj in dataset:
            if is_in((self.vector.x_start, self.vector.y_start, self.vector.x_end, self.vector.y_end),
                     (obj.vector.x, obj.vector.y)):
                self.content.append(obj)
        self.__detect_headers()
        self.vector.get_fields_coordinate(self.kind, self.form)

    def __detect_headers(self):
        for text in self.content:

            # Searching kind of page
            if is_in((self.down_border.vector.x_start, self.down_border.vector.y_start,
                      self.down_border.vector.x_start + 28, self.down_border.vector.y_start + 8.3),
                     (text.vector.x, text.vector.y)):
                import re
                if re.fullmatch("[оo][кk]", text.text.strip().lower()) is not None:  # it needs because technologists incorrect printing kind
                    self.kind = "ОК"
                elif re.fullmatch("[мm][кk]", text.text.strip().lower()) is not None:  # it needs because technologists incorrect printing kind
                    self.kind = "МК"
                else:
                    self.kind = text.text

            # Searching number of page
            if is_in((self.down_border.vector.x_end - 33, self.down_border.vector.y_start,
                      self.down_border.vector.x_end, self.down_border.vector.y_start + 8.3),
                     (text.vector.x, text.vector.y)):
                try:
                    self.page_number = int(text.text)
                except ValueError:
                    self.page_number = int(''.join(x for x in text.text if x.isdigit()))

            # Searching info in down-center
            if is_in((self.down_border.vector.x_start + 30, self.down_border.vector.y_start,
                      self.down_border.vector.x_end - 34, self.down_border.vector.y_start + 8.3),
                     (text.vector.x, text.vector.y)):
                self.additional_info = text.text

            # Searching form on right-up part of page
            if is_in((self.up_border.vector.x_end - 150, self.up_border.vector.y_end - 6,
                      self.up_border.vector.x_end, self.up_border.vector.y_end),
                     (text.vector.x, text.vector.y)):
                form_re = detect_form_via_re(text.text)
                if form_re is not None:
                    self.form = "".join(form_re.split(" "))

        if self.page_number is None:
            self.page_number = -1
        if self.kind is None:
            self.kind = "Undefined"
        if self.form is None:
            self.form = -1

        if self.page_number == -1 and (self.kind == "Undefined" or self.form == -1):
            raise Exception(f"Failed to resolve any headers at page on {self.vector.get_start_coordinate()};"
                            f"{self.vector.get_end_coordinate()} in file {self.file_name}, page {self.page_number}")

        if self.kind.lower() == "тл" \
                or (self.kind.lower() == "мк" and self.form == "2") \
                and (self.kind is None  # continue until find all searching fields
                     or self.form is None
                     or self.developer is None
                     or self.checker is None
                     or self.approver is None
                     or self.normalizator is None):
            self.__detect_main_info()

            if self.name_tech is None:
                raise Exception(f"Failed to match name and code of tech process on page {self.page_number} "
                                f"in file {self.file_name}")

        self.__get_additional_info()

    def __detect_main_info(self):
        temp_list_N_TC = []  # temp_list_N_TC list for handling of name and techname
        temp_list_descr = []  # temp_list_N_TC list for handling description
        for text in self.content:
            if is_in((self.up_border.vector.x_start + 137, self.up_border.vector.y_end - 44,  # name and techname
                      self.up_border.vector.x_end - 5, self.up_border.vector.y_end - 32),
                     (text.vector.x, text.vector.y)):
                temp_list_N_TC.append(text)

            if is_in((self.up_border.vector.x_start + 102, self.up_border.vector.y_end - 53,  # description
                      self.up_border.vector.x_end - 36.7, self.up_border.vector.y_end - 44.25),
                     (text.vector.x, text.vector.y)):
                temp_list_descr.append(text.text)

            if is_in((self.up_border.vector.x_start + 28.9, self.up_border.vector.y_start - 35.75,  # developer
                      self.up_border.vector.x_start + 65.3, self.up_border.vector.y_start - 31.5),
                     (text.vector.x, text.vector.y)):
                self.developer = text.text

            if is_in((self.up_border.vector.x_start + 28.9, self.up_border.vector.y_start - 40,  # checker
                      self.up_border.vector.x_start + 65.3, self.up_border.vector.y_start - 35.75),
                     (text.vector.x, text.vector.y)):
                self.checker = text.text

            if is_in((self.up_border.vector.x_start + 28.9, self.up_border.vector.y_start - 44.25,  # approver
                      self.up_border.vector.x_start + 65.3, self.up_border.vector.y_start - 40),
                     (text.vector.x, text.vector.y)):
                self.approver = text.text

            if is_in((self.up_border.vector.x_start + 28.9, self.up_border.vector.y_start - 52.75,  # normalizator
                      self.up_border.vector.x_start + 65.3, self.up_border.vector.y_start - 48.5),
                     (text.vector.x, text.vector.y)):
                self.normalizator = text.text

            if is_in((self.up_border.vector.x_end - 36.7, self.up_border.vector.y_start - 52.75,  # liter
                      self.up_border.vector.x_end - 26.3, self.up_border.vector.y_start - 44.25),
                     (text.vector.x, text.vector.y)):
                self.liter = text.text

        self.description = "".join(temp_list_descr)  # get the description

        # handling name and techname
        temp_list_N_TC = sorted(temp_list_N_TC, key=lambda i: i.vector.x)
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
            logging.warning(f"in file {self.file_name} found only ID of process flow")

    def __get_additional_info(self):
        for text in self.content:
            # ОК1
            if self.kind.lower() == "ок" and self.form == "1":

                if is_in((self.vector.x_end - 21.000, self.vector.y_end - 52.7500,  # number_of_operation
                          self.vector.x_end - 5.500, self.vector.y_end - 44.250),
                         (text.vector.x, text.vector.y)):
                    self.number_of_operation = text.text.strip()

                if is_in((self.vector.x_start + 18.900, self.vector.y_end - 65.5000,  # name_of_operation
                          self.vector.x_start + 143.1295, self.vector.y_end - 57.000),
                         (text.vector.x, text.vector.y)):
                    self.name_of_operation = text.text

                if is_in((self.vector.x_start + 143.1295, self.vector.y_end - 65.5000,  # IOT
                          self.vector.x_end - 26.8198, self.vector.y_end - 57.000),
                         (text.vector.x, text.vector.y)):
                    self.IOT = text.text

                if is_in((self.vector.x_start + 143.1295, self.vector.y_end - 77.5000,  # ammo
                          self.vector.x_end - 44.2949, self.vector.y_end - 69.7594),
                         (text.vector.x, text.vector.y)):
                    self.ammo = text.text

            elif self.kind.lower() == "ок" and self.form.lower() in ("1а", "2а"):  # additionally for "OK 2a"
                if is_in((self.vector.x_end - 20.000, self.vector.y_end - 44.2500,  # number_of_operation
                          self.vector.x_end - 5.500, self.vector.y_end - 31.500),
                         (text.vector.x, text.vector.y)):
                    self.number_of_operation = text.text.strip()

            # ОК2
            elif self.kind.lower() == "ок" and self.form.lower() == "2":

                if is_in((self.vector.x_end - 20.000, self.vector.y_end - 52.7500,  # number_of_operation
                          self.vector.x_end - 5.500, self.vector.y_end - 44.2500),
                         (text.vector.x, text.vector.y)):
                    self.number_of_operation = text.text.strip()

                if is_in((self.vector.x_start + 5.500, self.vector.y_end - 65.5000,  # name_of_operation
                          self.vector.x_start + 150.500, self.vector.y_end - 57.000),
                         (text.vector.x, text.vector.y)):
                    self.name_of_operation = text.text

                if is_in((self.vector.x_end - 42.500, self.vector.y_end - 82.5000,  # IOT
                          self.vector.x_end - 5.5000, self.vector.y_end - 69.5000),
                         (text.vector.x, text.vector.y)):
                    self.IOT = text.text

            else:
                break
