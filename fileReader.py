import math
import os

from Objects.Line import Line
from Objects.DbText import DbText


def get_data(file_name, dir_path):
    added = {}  # hashmap for already added lines. It needs because in dwg files has lines that placed on same points
    #drope = []

    abs_file = dir_path + '/' + file_name
    data = [[], []]
    with open(abs_file, 'r', encoding='utf-8') as f:
        for obj in f:
            # duplicate check
            if str(obj).startswith("$ListLine"):  # if line
                spl = obj.split("||")
                if math.isclose(float(spl[6]), 0, rel_tol=1e-1):  # if horizontal
                    key_coordinate = (round((float(spl[1]) + float(spl[2])) / 2), round(float(spl[3])))
                else:  # if vertical
                    key_coordinate = (round((float(spl[3]) + float(spl[4])) / 2), round(float(spl[1])))
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        exist = added.get((key_coordinate[0] + i, key_coordinate[1] + j))
                        if exist is not None:
                            #drope.append(exist)
                            break
                    if exist is not None:
                        break
                if exist is not None:
                    continue
                #

                line = Line(obj.split('||'), file_name)
                data[0].append(line)
                added[key_coordinate] = key_coordinate

            else:  # if text
                data[1].append(DbText(obj.split("||")))
    return data
