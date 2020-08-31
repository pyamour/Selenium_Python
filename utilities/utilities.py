import re
import pandas as pd
from config.constants import *
import json


def gen_testdata(csvfile, delimiter=',', header=0, scenario='', usecols=None):
    # Create a dataframe from csv
    df = pd.read_csv(csvfile, delimiter=delimiter, header=header, usecols=usecols)
    if scenario != '':
        df = df[df['scenario'] == scenario]
    if "scenario" in df.keys():
        df = df.drop("scenario", axis=1)
    df = df.where(df.notnull(), None)  # Transfer NaN to None

    # auto increase companyname and sitename number to create new set of testdata
    ai_list = [["companyname", CNB], ["sitename", SNB]]
    for ai in ai_list:
        if ai[0] in df.keys():
            for index, row in df.iterrows():
                if row[ai[0]] and row[ai[0]] != 'NaN' and row[ai[0]] != 'None' and row[ai[0]] is not None:
                    if row[ai[0]][-3:].isdigit():
                        row[ai[0]] = str(row[ai[0]][:-3]) + str(int(row[ai[0]][-3:]) + int(ai[1]))

    # User list comprehension to create a list of lists from Dataframe rows
    list_of_rows = [list(row) for row in df.values]

    return list_of_rows


def none_to_blank(x):
    if x is None:
        x = ""
    return x


def none_to_blank_list(x):
    if x is None:
        x = []
    return x


def none_to_blank_dict(x):
    if x is None:
        x = {}
    return x


def email_is_valid(email):
    rex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(rex, email) is None:
        return False
    else:
        return True


def str_to_list(src_str):

    if src_str == None or src_str == 'nan' or src_str == 'None' or str(src_str) == 'nan':
        dest_list = None
        return dest_list
    elif src_str == "":
        dest_list = []
        return dest_list
    else:
        src_str = src_str.replace("\n", ";")
        dest_list = str(src_str).split(";")
        dest_list = list(map(lambda x: x.strip(), dest_list))
        return dest_list


def list_to_str(src_list):
    src_list = list(map(lambda x: ";" + str(x), src_list))
    dest_str = "".join(src_list)
    dest_str = dest_str[1:]
    return dest_str


def dict_to_str(src_key_list):
    if len(src_key_list) == 0:
        dest_str = ""
        return dest_str

    dest_str = "{"
    for key in src_key_list.keys():
        dest_str = dest_str + "'" + str(key) + "':'"
        dest_str = dest_str + list_to_str(src_key_list[key]) + "'" + ","
    dest_str = dest_str[:-1] + "}"

    return dest_str

def str_to_dict(dict_str):

    info_dict = eval(str(dict_str))
    if info_dict is None or info_dict == {}:
        return info_dict
    #print("info_dict: " + str(info_dict))
    for key, value in info_dict.items():
        info_dict[key] = str_to_list(value)
        #print(info_dict[key])
    #print(str(info_dict))
    return info_dict


def valuedict_str_to_key_value(valuedict: str):
    if valuedict == "" or valuedict == None or valuedict == 'nan' or valuedict == 'None' or str(valuedict) == 'nan':
        key = []
        value = {}
    else:
        valuedict = str(valuedict).replace("\'", "\"")
        valuedict = json.loads(str(valuedict))
        key = list(valuedict.keys())
        value = valuedict
    return [key, value]
