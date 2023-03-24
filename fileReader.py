from Objects.Line import Line
from Objects.DbText import DbText


def get_data(file_name, dir_path):
    abs_file = dir_path + '/' + file_name
    data = [[], []]
    with open(abs_file, 'r', encoding='utf-8') as f:
        for obj in f:
            if str(obj).startswith("$ListLine"):
                data[0].append(Line(obj.split('||')))
            else:
                data[1].append(DbText(obj.split("||")))
    return data
