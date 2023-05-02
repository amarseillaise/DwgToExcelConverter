import math
from Objects.Line import Line
from Objects.DbText import DbText


def get_data(file_name: str, dir_path: str):

    abs_file_path: str = dir_path + '/' + file_name
    data = [{}, []]
    key_coordinate: tuple[float, float]  # for detect coordinate with high accuracy
    with open(abs_file_path, 'r', encoding='utf-8') as f:
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
                        exist = data[0].get((key_coordinate[0] + i, key_coordinate[1] + j))
                        if exist:
                            break
                    if exist:
                        break
                if exist:
                    continue
                #

                line = Line(obj.split('||'), file_name)
                data[0][key_coordinate] = line

            else:  # if text
                data[1].append(DbText(obj.split("||")))
    return data
