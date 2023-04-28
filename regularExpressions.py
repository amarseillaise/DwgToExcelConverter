import re


def is_it_form_of_page(string):
    re_pattern_whole_string = r"(?:Форма|форма)[ ]+\d{1,2}(?:\w{1}|[ ]+\w{1}|\b)"  # r"(?:Форма|форма)\s+\d{1,2}(?:\w{1}|\s|\b)"
    re_pattern_of_number_of_form = r"\d{1,2}(?:\w{1}|[ ]+\w{1}|\b)"
    try:
        pre_result = re.search(re_pattern_whole_string, string)
        result = re.search(re_pattern_of_number_of_form, pre_result[0])
        return result[0].strip()
    except (IndexError, TypeError):
        return None


def is_it_number_of_field(string):
    re_pattern = r"(?:^|[ ]+)\d\d"  # r"(?:^|[ ]+|\|)\d\d\|"
    result = re.fullmatch(re_pattern, string)
    return True if result is not None else False


def is_it_new_item(string, re_pattern):
    result = re.search(re_pattern, string)
    return True if result is not None else False
