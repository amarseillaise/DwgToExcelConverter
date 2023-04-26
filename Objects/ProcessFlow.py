class ProcessFlow:
    def __init__(self, file_name, marker, name, description, developer, checker, approver, normalizator, liter):
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


class Operation:
    def __init__(self, nnt):
        self.number = nnt[0]
        self.description = nnt[1]
        self.tsekh = nnt[2]
        self.ammo = None
        self.IOT = None
        self.shifts = []


class Shift:
    def __init__(self, number, description, tools_list, percent):
        self.number = number
        self.description = description
        self.tools = tools_list
        self.percent_control = percent
        pass


class Tool:
    def __init__(self, name):
        self.name = name
        self.standard = None
        self.quantity = None
        self.um = None


class UnresolvedText:
    def __init__(self, page, text):
        self.number_of_operation = page
        self.text = text
