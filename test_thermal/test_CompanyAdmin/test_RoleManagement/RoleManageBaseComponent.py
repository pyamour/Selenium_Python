from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from utilities import utilities
from utilities import gmail
from utilities.Authority import Authority
from config.constants import *
from test_thermal.ThermalBase import ThermalBase
import math
import datetime
import time
import json


class RoleManageBaseComponent(ThermalBase):

    def process_create_input(self, companyname, rolename, service_list, user_list, expectation):
        [companyname, rolename, expectation] = map(str, [companyname, rolename, expectation])
        [service_list, user_list] = map(utilities.str_to_list, [service_list, user_list])
        return companyname, rolename, service_list, user_list, expectation

    def process_update_input(self, companyname, rolename, valuedict,expectation):
        [companyname, rolename, expectation] = map(str, [companyname, rolename, expectation])
        [[key, value]] = map(utilities.valuedict_str_to_key_value, [valuedict])
        return companyname, rolename, key, value, expectation

    def verify_role_authority(self, rolename, email_list=None):
        print("Start to verify role authority")
        local = locals()
        local.pop('self')
        print(local)

        found_role = self.role_search(rolename)
        if found_role == {}:
            self.assertTrue(False, "Cannot find role: " + rolename)
        correct_info = found_role["rolename"] == rolename

        if correct_info and email_list != None:
            print("user_list in found_role: " + str(found_role["user_list"]))
            found_email_list = list(set(found_role["user_list"]))
            print("found_email_list: " + str(found_email_list))
            email_list = list(set(email_list))
            print("email_list: " + str(email_list))
            correct_info = correct_info and sorted(found_email_list) == sorted(email_list)
            if not correct_info:
                print("Email list doesn't match")

        if correct_info:
            print("Expected: " + str(local))
            print("Got: " + str(found_role))
        self.assertTrue(correct_info, "role info doesn't match \n" + "Expected: " + str(
            local) + "\n" + "Got: " + str(found_role))

    def role_create_start(self):
        self.click("#pane-1 .el-icon-plus", by=By.CSS_SELECTOR)

    def role_update_start(self, selector):
        self.click(selector)

    def role_create_update_set_rolename(self, rolename, expectation="pass"):
        self.type(".name-container > div:nth-child(2) .el-input__inner", rolename)

    def role_create_update_set_service_list(self, service_list, fail_msg=None, expectation="pass"):
        selector = None
        self.remove_add_checkbox_group(target_type="service", target_list=service_list, selector=selector,
                                       fail_msg=fail_msg, expectation=expectation)

    def role_create_update_set_user_list(self, user_list: list, fail_msg=None, expectation="pass"):
        selector = None
        self.remove_add_dropdown_list(target_type="user", target_list=user_list, selector=selector, fail_msg=fail_msg,
                                      expectation=expectation)

    def role_search(self, rolename):
        # Only return one role with latest date
        # Todo: use option selector

        print("Search: " + rolename)

        if rolename == "":
            return {}

        total_selector = "#pane-1 > div > div:nth-child(2) > div:nth-child(2) > div > span.el-pagination__total"
        total, perpage, pages, next_page_selector_str, previous_page_selector_str = self.get_page_navigation_info(
            total_selector)
        info_dict = {}
        max_date = "Jan 01, 2020"
        dest_page = 0

        for i in range(pages):
            page = i + 1
            if page > 1:
                self.click(next_page_selector_str)
            print("Start search in page: " + str(page))

            if page == pages:
                rows = total % perpage
                if rows == 0:
                    rows = perpage
            else:
                rows = perpage
            print("In page: " + str(page) + " " + str(rows) + " rows exist")

            source = self.get_page_source()
            soup = self.get_beautiful_soup(source)
            tables = soup.find_all(name="table", class_="el-table__body")
            # print("Get " + str(len(tables)) + " tables") table for site admin, role admin, user admin are together
            table = tables[1]
            tr = table.find('tr')

            for r in range(rows):
                tds = tr.find_all('td', recursive=False)
                #print(tds[0].get_text(separator=';'))
                #print(tds[1].get_text(separator=';'))
                #print(tds[2].get_text(separator=';'))
                #print(tds[3].get_text(separator=';'))
                #print(tds[4].get_text(separator=';'))
                row_date = tds[0].get_text(separator=';').strip()
                row_rolename = tds[1].get_text(separator=';').strip()
                print("In row: " + str(r + 1) + " rolename: " + row_rolename + " date: " + row_date)

                if row_rolename == rolename and datetime.datetime.strptime(str(row_date),
                                                                           '%b %d, %Y').date() > datetime.datetime.strptime(
                    str(max_date), '%b %d, %Y').date():
                    max_date = row_date
                    dest_page = page
                    print("Got one match max_date:  " + max_date + "   dest_page:  " + str(dest_page))

                    info_dict["rolename"] = row_rolename
                    info_dict["date"] = row_date
                    info_dict["preset"] = tds[2].get_text(separator=';').strip()
                    info_dict["service_list"] = utilities.str_to_list(tds[3].get_text(separator=';').strip())
                    info_dict["user_list"] = utilities.str_to_list(tds[4].get_text(separator=';').strip())
                    edit_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") .el-button:nth-child(1) > span"
                    delete_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") .el-button:nth-child(2) > span"
                    info_dict["edit_selector"] = edit_selector_str
                    info_dict["delete_selector"] = delete_selector_str
                    info_dict["name_selector"] = None
                    info_dict["date_selector"] = None

                tr = tr.find_next_sibling()

        if int(dest_page) > 0:
            for i in range(pages - dest_page):
                # self.type(".el-pagination__editor > .el-input__inner", str(dest_page) + Keys.ENTER)
                self.click(previous_page_selector_str)
                # self.wait_for_ready_state_complete()
                print("Go to page:  " + str(pages - i - 1))
        print("Finally got max_date:  " + max_date + "   dest_page:  " + str(dest_page))
        print("Got info_dict: " + str(info_dict))
        return info_dict

    def verify_role_info(self, rolename, service_list, user_list):
        print("Start to verify role info")
        local = locals()
        local.pop('self')
        print(local)

        found_role = self.role_search(rolename)
        if found_role == {}:
            self.assertTrue(False, "Cannot find role: " + rolename)
        correct_info = found_role["rolename"] == rolename
        if correct_info and service_list is not None:
            found_service_list = found_role["service_list"]
            service_list = list(set(service_list))
            correct_info = correct_info and sorted(found_service_list) == sorted(service_list)
        if correct_info and user_list is not None:
            found_user_list = found_role["user_list"]
            user_list = list(set(user_list))
            correct_info = correct_info and sorted(found_user_list) == sorted(user_list)

        if not correct_info:
            print("role info doesn't match")
        print("Expected: " + str(local))
        print("Got: " + str(found_role))
        self.assertTrue(correct_info, "role info doesn't match \n" + "Expected: " + str(
            local) + "\n" + "Got: " + str(found_role))

    def role_create_update_submit(self, expectation):
        self.click(".el-button--primary:nth-child(2)", by=By.CSS_SELECTOR)

        if expectation == "pass":
            print(self.get_text(".el-message__content"))
            # self.assert_text("Success", ".el-message__content")

    def role_delete_action(self, delete_selector):
        self.click(delete_selector, by=By.CSS_SELECTOR)
        self.click(".el-message-box__btns > .el-button--primary > span", by=By.CSS_SELECTOR)
        self.assert_text("The role has been successfully deleted", ".el-message__content")
        print(self.get_text(".el-message__content"))

    def remove_add_checkbox_group(self, target_type, target_list: list, selector=None, fail_msg=None,
                                  expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))

        item_str = "#pane-1 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.name-logo-container > div > div:nth-child(4) > div.el-checkbox-group > label:nth-child("
        selected_item_str = "#pane-1 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.name-logo-container > div > div:nth-child(4) > div.el-checkbox-group > label:nth-child(0) > span.el-checkbox__input.is-checked"

        # Get existing selected target list
        existing_list = []
        i = 0
        stop = False
        while not stop:
            i = i + 1
            i_item_str = item_str + str(i) + ")"
            i_selected_item_str = selected_item_str.replace("0", str(i))
            if not self.is_element_present(i_item_str):
                stop = True
            elif self.is_element_present(i_selected_item_str):
                existing_list.append(self.get_text(i_item_str))
        print("Existing_" + target_type + "_list:  " + str(existing_list))

        to_add_list = [i for i in target_list if i not in existing_list]
        print("To_add_" + target_type + "_list:   " + str(to_add_list))
        to_delete_list = [i for i in existing_list if i not in target_list]
        print("To_delete_" + target_type + "_list:   " + str(to_delete_list))

        # To delete or add
        i = 0
        stop = False
        while not stop:
            i = i + 1
            i_item_str = item_str + str(i) + ")"
            if not self.is_element_present(i_item_str):
                stop = True
            elif self.get_text(i_item_str) in (to_add_list + to_delete_list):
                self.click(i_item_str)

    def remove_add_dropdown_list(self, target_type, target_list: list, selector=None, fail_msg=None,
                                 expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))

        existing_item_str = ".el-tag:nth-child(0) > .el-select__tags-text"
        delete_item_str = ".el-tag:nth-child(0) > .el-tag__close"
        dropdown_item_str = "//div[3]/div/div/ul/li[0]"
        open_dropdown_str = ".el-input:nth-child(2) > .el-input__inner"
        close_dropdown_str = ".is-reverse"

        # Get existing target list
        existing_list = []
        i = 0
        stop = False
        while not stop:
            i = i + 1
            [i_existing_item_str, i_delete_item_str, i_dropdown_item_str] = map(lambda x: x.replace("0", str(i)),
                                                                                [existing_item_str, delete_item_str,
                                                                                 dropdown_item_str])
            if not self.is_element_present(i_existing_item_str):
                stop = True
            else:
                existing_list.append(self.get_text(i_existing_item_str))
        print("Existing_" + target_type + "_list:  " + str(existing_list))

        to_add_list = [i for i in target_list if i not in existing_list]
        print("To_add_" + target_type + "_list:   " + str(to_add_list))
        to_delete_list = [i for i in existing_list if i not in target_list]
        print("To_delete_" + target_type + "_list:   " + str(to_delete_list))

        # To delete
        i = 0
        stop = False
        while not stop and i < len(existing_list) and len(to_delete_list) > 0:
            i = i + 1
            [i_existing_item_str, i_delete_item_str, i_dropdown_item_str] = map(lambda x: x.replace("0", str(i)),
                                                                                [existing_item_str, delete_item_str,
                                                                                 dropdown_item_str])
            if self.is_element_present(i_existing_item_str):
                target = self.get_text(i_existing_item_str)
                if target in to_delete_list:
                    self.click(i_delete_item_str)
                    to_delete_list.remove(target)
                    i = i - 1
            else:
                stop = True

        # To add
        self.click(open_dropdown_str)

        i = 0
        stop = False
        while not stop and len(to_add_list) > 0:
            i = i + 1
            [i_existing_item_str, i_delete_item_str, i_dropdown_item_str] = map(lambda x: x.replace("0", str(i)),
                                                                                [existing_item_str, delete_item_str,
                                                                                 dropdown_item_str])
            if self.is_element_present(i_dropdown_item_str):
                target = self.get_text(i_dropdown_item_str)
                if target in to_add_list:
                    self.click(i_dropdown_item_str)
                    to_add_list.remove(target)
            else:
                stop = True

        self.click(close_dropdown_str)
