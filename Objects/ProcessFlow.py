import re
import logging
from Objects.Vector import is_in
from regularExpressions import is_it_new_item, is_it_number_of_field


class ProcessFlow:
    def __init__(self, file_name: str, marker: str, name: str, description: str, developer: str, checker: str,
                 approver: str, normalizator: str, liter: str):
        self.file_name = file_name
        self.marker = marker
        self.name = name
        self.description = description
        self.developer = developer
        self.checker = checker
        self.approver = approver
        self.normalizator = normalizator
        self.liter = liter
        self.operations = {}
        self.unresolved_text = []


    def detect_operations(self, pages):
        def __split_operation_field(string):
            m = re.search(r"\s[0123]\d\d\s", string)

            number = string[m.start():m.end()]
            description = string[m.end():]
            tsekh = string[:m.start()].replace("А", "")
            return Operation((number.strip(), description.strip(), tsekh.strip()))
        
        
        #  detect operations dataset in fields via vector's coordinate
        fields = []
        for page in pages:
            if page.kind.lower() == "мк":
                for i in range(len(page.vector.fields_coordinate)):
                    temp_list = []
                    for text in page.content:
                        if is_in(page.vector.fields_coordinate[i], text.vector.get_start_coordinate()) \
                                and not is_it_number_of_field(text.text):
                            temp_list.append(text)
                    temp_list = sorted(temp_list, key=lambda x: x.vector.get_x1())
                    if len(temp_list) > 0:
                        fields.append("".join(x.text + "  " for x in temp_list))

        #  find operations via regexp r"\s[0123]\d\d\s"
        unresolved = ""
        previous_field = None
        for field in fields:
            if is_it_new_item(field, r"\s[0123]\d\d\s"):
                # in case first element of list
                if not previous_field:
                    previous_field = field
                    continue
                #
                o = __split_operation_field(previous_field)
                self.operations[o.number] = o
                previous_field = field
            elif previous_field:
                previous_field += " " + field
            else:
                unresolved += field

        try:
            o = __split_operation_field(previous_field)
            self.operations[o.number] = o  # in case final element of list
        except TypeError:
            self.unresolved_text.append(UnresolvedText("Somewhere in MK", unresolved))

    def detect_shifts(self, pages):


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
            percent = string[percent_match.start():percent_match.end()].replace(" ",
                                                                                "") if percent_match is not None else None
            #

            number = string[s.start():s.end()]
            try:
                description = string[s.end():start_about_tools_pos]
            except AttributeError:
                description = string[s.end():]
            return Shift(number.replace(".", "").replace("О", "").strip(), description.strip(), tools, percent)

        def __fields_data_getter(unresolved=""):
            previous_field = None
            for field in fields:
                if is_it_new_item(field, r"(?:^|(?: |^)[оО])(?: +|^)\d{1,2}\.? "):
                    # in case first element of list
                    if not previous_field:
                        previous_field = field
                        continue
                    #
                    s = __split_shift_field(previous_field)
                    try:
                        self.operations[previous_page.number_of_operation].shifts.append(s)
                    except KeyError:
                        self.operations[previous_page.number_of_operation] = Operation(
                            (previous_page.number_of_operation, previous_page.name_of_operation, ""))
                        logging.warning(
                            f"In file {self.file_name} operation #{previous_page.number_of_operation} not found in MK")
                        operation = self.operations[previous_page.number_of_operation]
                        operation.IOT = previous_page.IOT
                        operation.ammo = previous_page.ammo
                        self.operations[previous_page.number_of_operation].shifts.append(s)
                    previous_field = field
                elif previous_field:
                    previous_field += " " + field
                else:
                    unresolved += field

            s = __split_shift_field(previous_field)
            self.operations[previous_page.number_of_operation].shifts.append(s)  # in case final element of list

            if unresolved:
                self.unresolved_text.append(UnresolvedText(previous_page.number_of_operation, unresolved))

            fields.clear()


        #  detect operations dataset in fields via vector's coordinate
        fields = []
        previous_page = pages[0]
        for page in pages:
            if page.kind.lower() == "ок" and page.number_of_operation:
                if previous_page.page_number != pages[0].page_number \
                        and page.number_of_operation != previous_page.number_of_operation:

                    #  find operations via regexp r"(?:^|О) +\d{1,2}\.? "
                    unresolved = ""
                    __fields_data_getter()

                # in case it's first page of operation we get headers
                if page.form in ("1", "2"):
                    try:
                        operation = self.operations[page.number_of_operation]
                    except KeyError:
                        self.operations[page.number_of_operation] = Operation(
                            (page.number_of_operation, page.name_of_operation, ""))
                        logging.warning(f"In file {self.file_name} operation #{page.number_of_operation} not found in MK")
                        operation = self.operations[page.number_of_operation]
                    operation.IOT = page.IOT
                    operation.ammo = page.ammo
                #

                for i in range(len(page.vector.fields_coordinate)):
                    temp_list = []
                    for text in page.content:
                        if is_in(page.vector.fields_coordinate[i], text.vector.get_start_coordinate()) \
                                and not is_it_number_of_field(text.text):
                            temp_list.append(text)
                    temp_list = sorted(temp_list, key=lambda x: x.vector.get_x1())
                    if len(temp_list) > 0:
                        fields.append("".join(x.text + "  " for x in temp_list))

                previous_page = page

        if page.kind.lower() == "ок" and page.number_of_operation:
            __fields_data_getter(unresolved)



class Operation:
    def __init__(self, nnt: tuple):
        self.number = nnt[0]
        self.description = nnt[1]
        self.tsekh = nnt[2]
        self.ammo = ""
        self.IOT = ""
        self.shifts = []


class Shift:
    def __init__(self, number: int, description: str, tools_list: list, percent: str):
        self.number = number
        self.description = description
        self.tools = tools_list
        self.percent_control = percent
        pass


class Tool:
    def __init__(self, name: str):
        self.name = name
        self.standard = ""
        self.quantity = None
        self.um = ""


class UnresolvedText:
    def __init__(self, page: str, text: str):
        self.number_of_operation = page
        self.text = text
