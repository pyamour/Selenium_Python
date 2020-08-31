import pandas as pd
from config.constants import *
from utilities import utilities
#import utilities
from utilities.Entity import Entity
#from Entity import Entity
import os
import re
import pprint


class Authority:

    def __init__(self, datafile=AUTHORITY_DATA_FILE):

        self.datafile = datafile
        file_exist = os.path.isfile(self.datafile)

        if file_exist:
            self.df = pd.read_csv(self.datafile, usecols=AUTHORITY_COLUMNS)
            self.df.drop_duplicates(subset="email", keep="last", inplace=True)
        else:
            self.df = pd.DataFrame(columns=AUTHORITY_COLUMNS)

        self.df = self.df.where(self.df.notnull(), None)  # Transfer NaN to None

    def commit(self):
        self.df.to_csv(self.datafile, sep=',', index=False, quoting=1)

    def get_user_info(self, email, column):

        if column not in AUTHORITY_COLUMNS:
            return None

        info = list(self.df[self.df["email"] == email][column])
        if len(info) > 0:
            if column in AUTHORITY_SINGLE_VALUE_COLUMNS:
                return str(info[0])
            if column in AUTHORITY_LIST_VALUE_COLUMNS:
                return utilities.str_to_list(str(info[0]))
            if column in AUTHORITY_KEY_LIST_VALUE_COLUMNS:
                return utilities.str_to_dict(str(info[0]))

    def get_email_list(self, bycolumn=None, value=None, company=None):

        print("In Authority get_email_list")
        print(locals())

        df = pd.DataFrame(columns=self.df.keys())
        for id, row in self.df.iterrows():
            if company in row["company"]:
                df = df.append(row)

        if bycolumn not in AUTHORITY_COLUMNS:
            return None

        if bycolumn is None and value is None:
            email_list = list(df["email"])

        if bycolumn in AUTHORITY_SINGLE_VALUE_COLUMNS:
            email_list = list(df[df[bycolumn] == value]["email"])

        if bycolumn in AUTHORITY_LIST_VALUE_COLUMNS:
            email_list = []
            for index, item in df.iterrows():
                if value in utilities.str_to_list(item[bycolumn]):
                    email_list.append(item["email"])

        if bycolumn in AUTHORITY_KEY_LIST_VALUE_COLUMNS:
            email_list = []
            for index, item in df.iterrows():
                print("Content of item: " + str(item))
                info_dict = utilities.str_to_dict(item[bycolumn])
                for info_key, info_value in info_dict.items():
                    print("item['email']: " + str(item["email"]))
                    print("info_value in item: " + str(info_value))
                    if value in info_value:
                        email_list.append(item["email"])

        return email_list

    def get_flat_authority_info(self, column="site"):

        df = self.df[["email", "company", column]]

        #print("Original df: " + str(df))
        flat_authority_df = pd.DataFrame(columns=["company", column, "email"])
        for index, row in df.iterrows():
            email = row["email"]
            company_list = utilities.str_to_list(row["company"])
            site_dict = utilities.str_to_dict(row[column])
            if company_list is None or company_list == []:
                continue
            for company in company_list:
                to_append_list = ["", "", ""]
                to_append_list[0] = company
                to_append_list[2] = email
                if site_dict is None or site_dict == {}:
                    continue
                site_list = site_dict[company]
                for site in site_list:
                    to_append_list[1] = site
                    flat_authority_df = flat_authority_df.append(
                        pd.Series(to_append_list, index=['company', column, 'email']), ignore_index=True)

        return flat_authority_df

    def replace_any_with_specific_site(self, flat_authority_df):
        entity = Entity()
        entity_df = entity.df
        columns = flat_authority_df.keys()
        dest_flat_authority_df = pd.DataFrame(columns=columns)
        for index, row in flat_authority_df.iterrows():
            to_append_list = ["", "", ""]
            if row["site"] == SITE_ANY_SITE:
                #print("get site record")
                #print(list(entity_df[entity_df["company"] == row["company"]]))
                site_value = list(entity_df[entity_df["company"] == row["company"]]["site"])
                if site_value != [] and site_value is not None:
                    site_list = utilities.str_to_list(site_value[0])
                    if site_list is not None and len(site_list) > 0:
                        for site in site_list:
                            to_append_list[0] = row["company"]
                            to_append_list[1] = site
                            to_append_list[2] = row["email"]
                            dest_flat_authority_df = dest_flat_authority_df.append(pd.Series(to_append_list, index=columns),
                                                                                   ignore_index=True)
            else:
                dest_flat_authority_df = dest_flat_authority_df.append(pd.Series(row, index=columns),
                                                                       ignore_index=True)

        #print("anysite_processed_flat_authority_df: " + str(dest_flat_authority_df))
        return dest_flat_authority_df

    def get_role_or_site_authority_info(self, column="site"):

        flat_authority_df = self.get_flat_authority_info(column=column)
        #print("flat_authority_df: " + str(flat_authority_df))
        if column == "site":
            flat_authority_df = self.replace_any_with_specific_site(flat_authority_df)
        site_authority_df = flat_authority_df.groupby(["company", column])["email"].apply(list)
        site_authority_df = site_authority_df.reset_index()

        list_of_rows = [list(row) for row in site_authority_df.values]
        #print(str(list_of_rows))
        return list_of_rows

    def get_role_authority_info(self):

        return self.get_role_or_site_authority_info(column="role")

    def get_site_authority_info(self):

        return self.get_role_or_site_authority_info(column="site")

    def transform_user_profile_to_user_authority(self, row):

        [username] = map(str, [row[0]])
        [company_list] = map(utilities.str_to_list, [row[1]])
        [site_dict, role_dict] = map(utilities.str_to_dict, [row[2], row[3]])

        return [username, company_list, site_dict, role_dict]

    def get_user_authority_info(self):

        row_list = [list(row) for row in self.df[["email", "company", "site", "role"]].values]
        authority_list = map(self.transform_user_profile_to_user_authority, row_list)

        return authority_list

    def add_authority(self, email, password=None, status=None, company: list = None, site: dict = None, role: dict = None):

        print("Start add_authority in Authority.py")
        print(locals())

        if not utilities.email_is_valid(email):
            print("Invalid email: " + email)
            return False

        #Update existing record
        if email in self.df["email"].tolist():
            print("Update existing user: " + email)
            update_single_value = True
            add_list_value = True
            add_key_list_value = True

            info_dict = {"password": password, "status": status, "company": company, "site": site, "role": role}

            for key in list(info_dict.keys()):
                if info_dict[key] is not None:
                    if key in AUTHORITY_SINGLE_VALUE_COLUMNS:
                        update_single_value = update_single_value and self.update_authority_single_value_column(
                            email=email, column=key, value=info_dict[key])
                    if key in AUTHORITY_LIST_VALUE_COLUMNS:
                        add_list_value = add_list_value and self.update_authority_list_value_column(
                            email=email, column=key, value=info_dict[key], action="add")
                    if key in AUTHORITY_KEY_LIST_VALUE_COLUMNS:
                        add_key_list_value = add_key_list_value and self.update_authority_key_list_value_column(email=email, column=key, value=info_dict[key], action="add")


            return update_single_value and add_list_value and add_key_list_value

        #Add new record
        print("Add new user: " + email)

        [password, status] = list(map(utilities.none_to_blank, [password, status]))
        [company] = list(
            map(utilities.none_to_blank_list, [company]))
        [site, role] = list(
            map(utilities.none_to_blank_dict, [site, role]))
        print("company: " + str(company) + " site: " + str(site) + " role: " + str(role))

        info_dict = {}
        info_dict["email"] = email
        info_dict["password"] = password
        info_dict["status"] = status
        info_dict["company"] = utilities.list_to_str(company)
        info_dict["site"] = utilities.dict_to_str(site)
        print(info_dict["site"])
        info_dict["role"] = utilities.dict_to_str(role)
        # info_dict = {"email": email, "password": password, "status": status, "company": utilities.list_to_str(company), "site": utilities.list_to_str(site), "role": utilities.list_to_str(role)}
        print("info to add: " + str(info_dict))

        self.df = self.df.append([info_dict], ignore_index=True)
        print("Added \n" + str(info_dict) + "  \nto user profile")
        print(self.df)

        return True

    def remove_authority(self, email, password=None, status=None, company: list = None, site: dict = None, role: dict = None):

        print("Start remove_authority in Authority.py")
        print(locals())

        if not utilities.email_is_valid(email):
            print("Invalid email: " + email)
            return False

        if email not in self.df["email"].tolist():
            return False

        # Update existing record
        print("Update existing user: " + email)
        update_single_value = True
        remove_list_value = True
        remove_key_list_value = True

        # get site and role dict to remove
        if company is not None and company != []:

            site_to_remove = {}
            role_to_remove = {}
            existing_user_authority_list = self.get_user_authority_info()
            for existing_user_authority in existing_user_authority_list:
                if existing_user_authority[0] == email:
                    for each_company in company:
                        site_to_remove.update({each_company: existing_user_authority[2][each_company]})
                        role_to_remove.update({each_company: existing_user_authority[3][each_company]})
                    break

            if site is not None and site_to_remove != {}:
                site.update(site_to_remove)
            elif site is None and site_to_remove != {}:
                site = site_to_remove

            if role is not None and role_to_remove != {}:
                role.update(role_to_remove)
            elif role is None and role_to_remove != {}:
                role = role_to_remove

        info_dict = {"password": password, "status": status, "company": company, "site": site, "role": role}

        for key in list(info_dict.keys()):
            if info_dict[key] is not None:
                if key in AUTHORITY_SINGLE_VALUE_COLUMNS:
                    update_single_value = update_single_value and self.update_authority_single_value_column(
                        email=email, column=key, value=info_dict[key])
                if key in AUTHORITY_LIST_VALUE_COLUMNS:
                    remove_list_value = remove_list_value and self.update_authority_list_value_column(
                        email=email, column=key, value=info_dict[key], action="remove")
                if key in AUTHORITY_KEY_LIST_VALUE_COLUMNS:
                    remove_key_list_value = remove_key_list_value and self.update_authority_key_list_value_column(
                        email=email, column=key, value=info_dict[key], action="remove")

        return update_single_value and remove_list_value and remove_key_list_value

    def update_authority_single_value_column(self, email, column, value):

        if not utilities.email_is_valid(email):
            return False

        if value is None:
            return False

        if not (column in AUTHORITY_SINGLE_VALUE_COLUMNS):
            return False

        self.df.loc[self.df.email == email, column] = value
        return True

    def update_authority_list_value_column(self, email, column, value: list, action="add"):
        if value is None:
            return False

        existing_value = utilities.str_to_list(list(self.df.loc[self.df.email == email, column])[0])
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
        self.df.loc[self.df.email == email, column] = dest_value
        return True

    def update_authority_key_list_value_column(self, email, column, value: dict, action="add"):
        if value is None:
            return False

        print("Start update_user_profile_key_list_value_column")
        print(locals())

        existing_key_value = list(self.df.loc[self.df.email == email, column])[0]
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

        no_empty_dest_key_value = dest_key_value.copy()
        for key in dest_key_value.keys():
            if not dest_key_value[key]:
                no_empty_dest_key_value = no_empty_dest_key_value.pop(key)
        print("no_empty_dest_key_value: " + str(no_empty_dest_key_value))

        dest_value = utilities.dict_to_str(no_empty_dest_key_value)
        print("dest_value: " + str(dest_value))

        self.df.loc[self.df.email == email, column] = dest_value
        print(str(self.df["company"]))

        return True
