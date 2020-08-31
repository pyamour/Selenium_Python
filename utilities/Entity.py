import pandas as pd
from config.constants import *
from utilities import utilities
#import utilities
import os
import re


class Entity:

    def __init__(self, datafile=ENTITY_DATA_FILE):

        self.datafile = datafile
        file_exist = os.path.isfile(self.datafile)

        if file_exist:
            self.df = pd.read_csv(self.datafile, usecols=ENTITY_COLUMNS)
            self.df.drop_duplicates(subset="company", keep="last", inplace=True)
        else:
            self.df = pd.DataFrame(columns=ENTITY_COLUMNS)

        self.df = self.df.where(self.df.notnull(), None)  # Transfer NaN to None

    def commit(self):
        self.df.to_csv(self.datafile, sep=',', index=False, quoting=1)

    def add_entity(self, company, status=STATUS_ENABLED, site: list = None, camera: dict = None, controller: dict = None):

        print("Start add_entity in Entity.py")
        print(locals())

        #Update existing record
        if company in self.df["company"].tolist():
            print("Update existing company: " + company)
            update_single_value = True
            add_list_value = True
            add_key_list_value = True

            info_dict = {"status": status, "site": site, "camera": camera, "controller": controller}

            for key in list(info_dict.keys()):
                if info_dict[key] is not None:
                    if key in ENTITY_SINGLE_VALUE_COLUMNS:
                        update_single_value = update_single_value and self.update_entity_single_value_column(
                            company=company, column=key, value=info_dict[key])
                    if key in ENTITY_LIST_VALUE_COLUMNS:
                        add_list_value = add_list_value and self.update_entity_list_value_column(
                            company=company, column=key, value=info_dict[key], action="add")
                    if key in ENTITY_KEY_LIST_VALUE_COLUMNS:
                        add_key_list_value = add_key_list_value and self.update_entity_key_list_value_column(company=company, column=key, value=info_dict[key], action="add")


            return update_single_value and add_list_value and add_key_list_value

        #Add new record
        print("Add new company: " + company)

        [status] = list(map(utilities.none_to_blank, [status]))
        [site] = list(
            map(utilities.none_to_blank_list, [site]))
        [camera, controller] = list(
            map(utilities.none_to_blank_dict, [camera, controller]))
        print("status: " + str(status) + " site: " + str(site) + " camera: " + str(camera) + " controller: " + str(controller))

        info_dict = {"company": company, "status": status, "site": utilities.list_to_str(site), "camera": utilities.dict_to_str(camera),
                     "controller": utilities.dict_to_str(controller)}
        print("info to add: " + str(info_dict))

        self.df = self.df.append([info_dict], ignore_index=True)
        print("Added \n" + str(info_dict) + "  \nto entity profile")
        print(self.df)

        return True

    def update_entity_single_value_column(self, company, column, value):

        if value is None:
            return False

        if not (column in ENTITY_SINGLE_VALUE_COLUMNS):
            return False

        self.df.loc[self.df.company == company, column] = value
        return True

    def update_entity_list_value_column(self, company, column, value: list, action="add"):

        if value is None:
            return False

        existing_value = utilities.str_to_list(list(self.df.loc[self.df.company == company, column])[0])
        if existing_value is None:
            existing_value = []
        print("existing_value: " + str(existing_value))
        print("value to process: " + str(value))
        if action == "add":
            existing_value.extend(value)
            dest_value = existing_value
            print(dest_value)
            dest_value = list(set(dest_value))
        elif action == "remove":
            dest_value = list(set(existing_value) - set(value))
        else:
            print("Wrong action")
            return False

        dest_value = utilities.list_to_str(dest_value)
        self.df.loc[self.df.company == company, column] = dest_value
        return True

    def update_entity_key_list_value_column(self, company, column, value: dict, action="add"):

        if value is None:
            return False

        print("Start update_entity_profile_key_list_value_column")
        print(locals())

        existing_key_value = list(self.df.loc[self.df.company == company, column])[0]
        print("existing_key_value from df: " + str(existing_key_value))
        if existing_key_value is None:
            existing_key_value = {}
        else:
            existing_key_value = eval(existing_key_value)
        print("existing_key_value from df: " + str(existing_key_value))
        for ex_key, ex_value in existing_key_value.items():
            existing_key_value[ex_key] = utilities.str_to_list(str(ex_value))
        print("existing_key_value_list: " + str(existing_key_value))

        print("value to process: " + str(value))
        (to_key, to_value), = dict(value).items()

        if existing_key_value == {}:
            if action == "add":
                dest_key_value = dict(value)
            if action == "remove":
                dest_key_value = existing_key_value

        if (existing_key_value != {}) and (to_key not in existing_key_value.keys()):
            if action == "add":
                dest_key_value = {**existing_key_value, **dict(value)}
            if action == "remove":
                dest_key_value = existing_key_value

        if (existing_key_value != {}) and (to_key in existing_key_value.keys()):
            for ex_key, ex_value in existing_key_value.items():
                if ex_key == to_key:
                    if action == "add":
                        ex_value.extend(to_value)
                        existing_key_value[ex_key] = list(set(ex_value))
                    if action == "remove":
                        existing_key_value[ex_key] = list(set(ex_value) - set(to_value))
            dest_key_value = existing_key_value

        print("dest_key_value: " + str(dest_key_value))

        dest_value = utilities.dict_to_str(dest_key_value)
        print("dest_value: " + str(dest_value))

        self.df.loc[self.df.company == company, column] = dest_value
        print(self.df)

        return True
