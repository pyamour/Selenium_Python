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


class UserManageBaseComponent(ThermalBase):

    def process_create_input(self, companyname, username, display_name, status, site_list, role_list, expectation):
        [companyname, username, display_name, status, expectation] = map(str, [companyname, username, display_name, status, expectation])
        [site_list, role_list] = map(utilities.str_to_list, [site_list, role_list])
        return companyname, username, display_name, status, site_list, role_list, expectation

    def user_create_start(self):
        self.click("#pane-2 .el-icon-plus", by=By.CSS_SELECTOR)

    def user_create_update_set_username(self, username, expectation="pass"):
        self.type(".name-container .el-input__inner", username)

    def user_create_update_set_status(self, status, expectation="pass"):

        selector = "#pane-2 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.name-logo-container > div.name-container > div.el-switch.is-checked > span"
        if self.is_element_present(selector):
            enabled = True
        else:
            enabled = False
        print("Original status value: " + str(enabled))

        if status == "Disabled" and enabled:
            self.click('.el-switch__core')
        if status == "Enabled" and not enabled:
            self.click('.el-switch__core')

        if self.is_element_present(selector):
            enabled = True
        else:
            enabled = False
        print("Now status value: " + str(enabled))

    def user_create_update_set_site(self, site_list: list, fail_msg=None, expectation="pass"):
        selector = None
        self.remove_add_checkbox_group_site(target_type="site", target_list=site_list, selector=selector,
                                            fail_msg=fail_msg, expectation=expectation)

    def user_create_update_set_role(self, role_list: list, fail_msg=None, expectation="pass"):
        selector = None
        self.remove_add_checkbox_group_role(target_type="role", target_list=role_list, selector=selector,
                                            fail_msg=fail_msg, expectation=expectation)

    def user_search(self, username):
        # Only return one user with latest date
        #Todo: use option selector

        print("Search: " + username)
        total_selector = "#pane-2 > div > div:nth-child(2) > div:nth-child(2) > div > span.el-pagination__total"
        total, perpage, pages, next_page_selector_str, previous_page_selector_str = self.get_page_navigation_info(total_selector)

        if username == "":
            return {}

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
            """
            '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[1]/div'
            '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div'
            '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[2]/td[1]/div'
            '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[2]/td[1]/div'
            '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[7]/div/button[1]/span'
            '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[7]/div/button[2]/span'
            """
            selector_str_1 = '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr['
            selector_str_2 = ']/td['
            selector_str_3 = ']/div'
            for r in range(rows):
                date_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '1' + selector_str_3
                name_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '2' + selector_str_3
                display_name_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '3' + selector_str_3
                status_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '4' + selector_str_3
                site_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '5' + selector_str_3
                role_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '6' + selector_str_3
                edit_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '7' + selector_str_3 + "/button[1]/span"
                # edit_selector_str = '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[' + str(r+1) + ']/td[7]/div/button[1]/span'
                delete_selector_str = selector_str_1 + str(r + 1) + selector_str_2 + '7' + selector_str_3 + "/button[2]/span"
                # delete_selector_str = '//*[@id="pane-2"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[' + str(r+1) + ']/td[7]/div/button[2]/span'

                if self.is_element_present(name_selector_str):
                    row_date = self.get_text(date_selector_str)
                    row_username = self.get_text(name_selector_str)

                    print("In row: " + str(r + 1) + " username: " + row_username + " date: " + row_date)
                    if row_username == username and datetime.datetime.strptime(str(row_date), '%b %d, %Y').date() > datetime.datetime.strptime(str(max_date), '%b %d, %Y').date():
                        max_date = row_date
                        dest_page = page
                        print("Got one match max_date:  " + max_date + "   dest_page:  " + str(dest_page))

                        info_dict["date"] = row_date
                        info_dict["username"] = row_username
                        info_dict["display_name"] = self.get_text(display_name_selector_str)
                        info_dict["status"] = self.get_text(status_selector_str)
                        info_dict["site_list"] = utilities.str_to_list(self.get_text(site_selector_str))
                        info_dict["role_list"] = utilities.str_to_list(self.get_text(role_selector_str))
                        info_dict["edit_selector"] = edit_selector_str
                        info_dict["delete_selector"] = delete_selector_str
                        info_dict["name_selector"] = name_selector_str
                        info_dict["date_selector"] = date_selector_str
                else:
                    print("Selector str doesn't match")
        if int(dest_page) > 0:
            for i in range(pages - dest_page):
                # self.type(".el-pagination__editor > .el-input__inner", str(dest_page) + Keys.ENTER)
                self.click(previous_page_selector_str)
                # self.wait_for_ready_state_complete()
                print("Go to page:  " + str(pages - i - 1))
        print("Finally got max_date:  " + max_date + "   dest_page:  " + str(dest_page))

        print("return info_dict: " + str(info_dict))
        return info_dict

    def verify_user_info(self, username, display_name=None, status=None, site_list=None, role_list=None):
        print("Start to verify user info")
        local = locals()
        local.pop('self')
        print(local)

        found_user = self.user_search(username)
        if found_user == {}:
            self.assertTrue(False, "Cannot find user: " + username)
        correct_info = found_user["username"] == username
        if correct_info and display_name is not None:
            correct_info = correct_info and found_user["display_name"] == display_name
        if correct_info and status is not None:
            correct_info = correct_info and found_user["status"] == status
        if correct_info and site_list is not None:
            found_site_list = found_user["site_list"]
            site_list = list(set(site_list))
            correct_info = correct_info and sorted(found_site_list) == sorted(site_list)
        if correct_info and role_list is not None:
            found_role_list = found_user["role_list"]
            role_list = list(set(role_list))
            correct_info = correct_info and sorted(found_role_list) == sorted(role_list)

        if not correct_info:
            print("user info doesn't match")
        print("Expected: " + str(local))
        print("Got: " + str(found_user))
        self.assertTrue(correct_info, "user info doesn't match \n" + "Expected: " + str(
            local) + "\n" + "Got: " + str(found_user))

    def verify_user_authority(self, username, display_name=None, status=None, site_list=None, role_list=None):
        print("Start to verify user authority")
        local = locals()
        local.pop('self')
        print(local)

        found_user = self.user_search(username)
        if found_user == {}:
            self.assertTrue(False, "Cannot find user: " + username)
        correct_info = found_user["username"] == username
        if correct_info and display_name != None:
            correct_info = correct_info and found_user["display_name"] == display_name
            if not correct_info:
                print("Display name doesn't match")
        if correct_info and status != None:
            correct_info = correct_info and found_user["status"] == status
            if not correct_info:
                print("Status doesn't match")

        if correct_info and site_list != None:
            found_site_list = list(set(found_user["site_list"]))
            site_list = list(set(site_list))
            correct_info = correct_info and sorted(found_site_list) == sorted(site_list)
            if not correct_info:
                print("Site list doesn't match")
        if correct_info and role_list != None:
            found_role_list = list(set(found_user["role_list"]))
            role_list = list(set(role_list))
            correct_info = correct_info and sorted(found_role_list) == sorted(role_list)
            if not correct_info:
                print("Role list doesn't match")

        if correct_info:
            print("Expected: " + str(local))
            print("Got: " + str(found_user))
        self.assertTrue(correct_info, "user info doesn't match \n" + "Expected: " + str(
            local) + "\n" + "Got: " + str(found_user))

    def user_create_update_submit(self, expectation):
        self.click("//span[contains(.,'OK')]")
        if expectation == "pass":
            print(self.get_text(".el-message__content"))
            #self.assert_text("Success", ".el-message__content")

    def user_delete_action(self, delete_selector):
        self.click(delete_selector, by=By.CSS_SELECTOR)
        self.click(".el-message-box__btns > .el-button--primary > span", by=By.CSS_SELECTOR)
        self.assert_text("The user has been successfully deleted", ".el-message__content")
        print(self.get_text(".el-message__content"))

    def remove_add_checkbox_group_site(self, target_type, target_list: list, selector=None, fail_msg=None,
                                       expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))

        if target_list == [SITE_ANY_SITE]:
            selector = "//span[contains(.,'Any Site')]"
            self.click(selector)
            print("Site set: " + self.get_text("#pane-2 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(2) > label.el-checkbox.is-checked"))
            return

        item_str = "#pane-2 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(2) > div.el-checkbox-group > label:nth-child(#0) > span.el-checkbox__label"
        selected_item_str = "#pane-2 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(2) > div.el-checkbox-group > label:nth-child(#0) > span.el-checkbox__input.is-checked"

        # Get existing selected target list
        existing_list = []
        i = 0
        stop = False
        while not stop:
            i = i + 1
            i_item_str = item_str.replace("#0", str(i))
            i_selected_item_str = selected_item_str.replace("#0", str(i))
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
            i_item_str = item_str.replace("#0", str(i))
            i_selected_item_str = selected_item_str.replace("#0", str(i))
            if not self.is_element_present(i_item_str):
                stop = True
            elif self.get_text(i_item_str) in (to_add_list + to_delete_list):
                self.click(i_item_str)
                if self.is_element_present(i_selected_item_str):
                    print("Site set: " + self.get_text(i_item_str))

    def remove_add_checkbox_group_role(self, target_type, target_list: list, selector=None, fail_msg=None,
                                       expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))
        item_str = "#pane-2 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(4) > div.el-checkbox-group > label:nth-child(#0) > span.el-checkbox__label"
        selected_item_str = "#pane-2 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(4) > div.el-checkbox-group > label:nth-child(#0) > span.el-checkbox__input.is-checked"

        # Get existing selected target list
        existing_list = []
        i = 0
        stop = False
        while not stop:
            i = i + 1
            i_item_str = item_str.replace("#0", str(i))
            i_selected_item_str = selected_item_str.replace("#0", str(i))
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
            i_item_str = item_str.replace("#0", str(i))
            i_selected_item_str = selected_item_str.replace("#0", str(i))
            if not self.is_element_present(i_item_str):
                stop = True
            elif self.get_text(i_item_str) in (to_add_list + to_delete_list):
                self.click(i_item_str)
                if self.is_element_present(i_selected_item_str):
                    print("Role set: " + self.get_text(i_item_str))
