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

class SysAdminBaseComponent(ThermalBase):

    def process_create_input(self, companyname, status, email_list, expectation):
        [companyname, status, expectation] = map(str, [companyname, status, expectation])
        [email_list] = map(utilities.str_to_list, [email_list])
        return companyname, status, email_list, expectation

    def process_update_input(self, companyname, valuedict, expectation):
        [companyname, expectation] = map(str, [companyname, expectation])
        [[key, value]] = map(utilities.valuedict_str_to_key_value, [valuedict])
        return companyname, key, value, expectation

    def company_create_start(self):
        self.click(".el-icon-plus", by=By.CSS_SELECTOR)

    def company_create_update_set_companyname(self, companyname, expectation="pass"):
        self.click("div:nth-child(2) > .el-input > .el-input__inner", by=By.CSS_SELECTOR)
        self.type("div:nth-child(2) > .el-input > .el-input__inner", by=By.CSS_SELECTOR, text=companyname + Keys.ENTER)

    def company_create_update_set_status(self, status, expectation="pass"):

        selector = "#__layout > section > section > main > div > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.name-logo-container > div.name-container > div.el-switch.is-checked"
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

    def company_create_update_set_email(self, email_list: list, fail_msg=None, expectation="pass"):
        selector = "#__layout > section > section > main > div > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(2) > span:nth-child("
        self.remove_add_list(target_type="email", target_list=email_list, selector=selector, fail_msg=fail_msg, expectation=expectation)

    def company_search(self, companyname):

        if companyname == "":
            return {}

        # Only return one company with max id
        self.refresh_page()
        self.type(".el-input:nth-child(2) > .el-input__inner", by=By.CSS_SELECTOR, text=companyname)
        time.sleep(6)
        print("Search: " + companyname)

        # total_selector = "#__layout > section > section > main > div > div.el-card.is-always-shadow > div > div:nth-child(3) > div > span.el-pagination__total"
        total_selector = ".el-pagination__total"
        total, perpage, pages, next_page_selector_str, previous_page_selector_str = self.get_page_navigation_info(total_selector)

        info_dict = {}
        max_id = "00"
        dest_page = 0

        for i in range(pages):
            page = i + 1
            if page > 1:
                #self.type(".el-pagination__editor > .el-input__inner", str(page) + Keys.ENTER)
                self.click(next_page_selector_str)
            print("Start search in page: " + str(page))

            if page == pages:
                rows = total % perpage
                if rows == 0:
                    rows = perpage
            else:
                rows = perpage
            print("In page: " + str(page) + " " + str(rows) + " rows exist")

            for r in range(rows):
                print("row: " + str(r))
                #name_selector_str = ".el-table__row:nth-child(" + str(r+1) + ") > .el-table_1_column_3 > .cell"
                #id_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") > .el-table_1_column_2 > .cell"
                id_selector_str = "//tr[" + str(r+1) + "]/td[2]/div"
                name_selector_str = "//tr[" + str(r + 1) + "]/td[3]/div"
                status_selector_str = "//tr[" + str(r + 1) + "]/td[4]/div"
                email_selector_str = "//tr[" + str(r + 1) + "]/td[6]/div"
                edit_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") .el-button:nth-child(1) > span"
                # edit_selector_str = "/tr[" + str(r+1) +"]/td[7]/div/button[1]/span"
                delete_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") .el-button:nth-child(2) > span"
                # delete_selector_str = "/tr[" + str(r+1) +"]/td[7]/div/button[2]/span"

                wait_time = 0
                while (not self.is_element_present(name_selector_str)) and wait_time < 120:
                    print("Is name selector visible: " + str(self.is_element_present(name_selector_str)) + " wait 6 seconds")
                    time.sleep(6)
                    wait_time += 6
                    self.wait_for_ready_state_complete()

                if self.is_element_present(name_selector_str):
                    row_companyname = self.get_text(name_selector_str)
                    row_id = self.get_text(id_selector_str)
                    print("In row: " + str(r+1) + " companyname: " + row_companyname + " id: " + row_id)
                    if (row_companyname == companyname and int(str(row_id)[1:]) > int(str(max_id)[1:])):
                        max_id = row_id
                        dest_page = page
                        print("Got one match record in row: " + str(r + 1) + " companyname: " + row_companyname + " id: " + row_id)
                        print("max_id:  " + max_id + "   dest_page:  " + str(dest_page))

                        info_dict["companyname"] = row_companyname
                        info_dict["id"] = row_id
                        info_dict["status"] = self.get_text(status_selector_str)
                        info_dict["companyadmin"] = self.get_text(email_selector_str)
                        info_dict["edit_selector"] = edit_selector_str
                        info_dict["delete_selector"] = delete_selector_str
                        info_dict["name_selector"] = name_selector_str
                        info_dict["id_selector"] = id_selector_str
        if int(dest_page) > 0:
            for i in range(pages-dest_page):
                #self.type(".el-pagination__editor > .el-input__inner", str(dest_page) + Keys.ENTER)
                self.click(previous_page_selector_str)
                #self.wait_for_ready_state_complete()
                print("Go to page:  " + str(pages-i-1))
        print("max_id:  " + max_id + "   dest_page:  " + str(dest_page))
        return info_dict

    def verify_company_info(self, companyname, status, email_list):
        print("Start to verify company info")
        print(locals())

        found_company = self.company_search(companyname)
        if found_company == {}:
            self.assertTrue(False, "Cannot find company: " + companyname)
        correct_info = found_company["companyname"] == companyname
        if correct_info and status != None:
            correct_info = correct_info and found_company["status"] == status
        if correct_info and email_list != None:
            companyadmin_list = found_company["companyadmin"]
            companyadmin_list = utilities.str_to_list(companyadmin_list)
            email_list = list(set(email_list))
            correct_info = correct_info and sorted(companyadmin_list) == sorted(email_list)

        # print(found_company)
        if not correct_info:
            print("Company info doesn't match")
            print("Expected: " + companyname + "   " + str(status) + "    " + str(email_list))
            print("Got: " + str(found_company))
        self.assertTrue(correct_info, "Company info doesn't match \n" + "Expected: " + companyname + "   " + str(status) + "    " + str(email_list) + "\n" + "Got: " + str(found_company))

    def verify_password_email(self, email_list):
        email_list_bk = email_list.copy()
        duration = 0
        max_duration = len(email_list) * 2
        start_time = datetime.datetime.now()
        valuedict = []

        while duration < max_duration and email_list != []:
            for email in email_list:
                password = gmail.check_password_in_gmail(email)
                if password != "":
                    print("Start to verify password: " + password + "  for " + email)
                    self.login(email, password)
                    self.logout(email)
                    print(email + "   " + password + "   verified successfully")
                    #user_file.update_user_profile_single_value_column(email=email, column="password", value=password)
                    valuedict.append({"email":email, "password":password})
                    #user_file.commit()
                    #print(str(user_file.df))
                    email_list_bk.remove(email)

            duration = datetime.datetime.now() - start_time
            duration = duration.total_seconds() // 60
            email_list = email_list_bk.copy()
            if duration < max_duration and email_list != []:
                time.sleep(60)
        return valuedict


    def company_create_update_submit(self, expectation):
        self.click(".button-container > .el-button--primary > span", by=By.CSS_SELECTOR)

        if expectation == "pass":
            print(self.get_text(".el-message__content"))
            self.assert_text("Success", ".el-message__content")
        elif expectation == "illegal_companyname_msg":
            print(self.get_text(".name-container > div:nth-child(3)"))
            self.assert_element_present(".name-container > div:nth-child(3)")
        elif expectation == "need_email_msg" or expectation == "illegal_email_msg":
            print(self.get(".main-container > div:nth-child(5)"))
            self.assert_element_present(".main-container > div:nth-child(5)")
        else:
            self.assert_true("Success" in self.get_text(".el-message__content"), "Create or update company failed")

    def company_update_start(self, edit_selector):

        self.click(edit_selector)

    def company_delete_action(self, delete_selector):
        self.click(delete_selector, by=By.CSS_SELECTOR)
        self.click(".el-message-box__btns > .el-button--primary > span", by=By.CSS_SELECTOR)
        self.assert_text("The company has been successfully deleted", ".el-message__content")
        print(self.get_text(".el-message__content"))

    def company_emptify_company_action(self, companyname):
        self.type(".el-input:nth-child(2) > .el-input__inner", by=By.CSS_SELECTOR, text=companyname)

        print("Search: " + companyname)
        total_text = self.get_text(".el-pagination__total")
        total = int(total_text.strip().split(' ')[1])
        print("Result total: " + str(total))

        r = 0
        while r <= total:
            current_row = r + 1
            r = r + 1
            selector_str = ".el-table__row:nth-child(" + str(current_row) + ") > .el-table_1_column_3 > .cell"
            if self.get_text(selector_str) not in ["luci", "Tridel Inc.", "04743f26-aeb3-4caf-b791-5a0a7f3ce8bb", "luci@1234",
                                                   "Luci.ai Inc"]:
                selector_str = ".el-table__row:nth-child(" + str(current_row) + ") .el-button:nth-child(2) > span"
                self.click(selector_str, by=By.CSS_SELECTOR)
                self.click(".el-message-box__btns > .el-button--primary > span", by=By.CSS_SELECTOR)
                print(self.get_text(".el-message__content"))
                if "The company has been successfully deleted" in self.get_text(".el-message__content"):
                    r = r - 1
                self.refresh_page()
                total_text = self.get_text(".el-pagination__total")
                total = str(int(total_text.strip().split(' ')[1]))
                print("Result total: " + total)

    def company_emptify_user_action(self, expectation="pass"):

        self.refresh_page()
        self.wait_for_ready_state_complete()
        self.wait(3)

        total_text = self.get_text(".el-pagination__total")
        total = int(total_text.strip().split(' ')[1])
        print("Companies total: " + str(total))

        # todo: get perpage automatically
        perpage = 20
        # todo: get pages automatically
        pages = math.ceil(total / perpage)
        print("pages: " + str(pages))

        info_dict = {}
        next_page_selector_str = ".el-icon-arrow-right"
        previous_page_selector_str = ".el-icon-arrow-left"
        max_id = "00"
        dest_page = 0

        for i in range(pages):
            page = i + 1
            if page > 1:
                # self.type(".el-pagination__editor > .el-input__inner", str(page) + Keys.ENTER)
                self.click(next_page_selector_str)
                self.wait(3)
            print("Start search in page: " + str(page))

            if page == pages:
                rows = total % perpage
                if rows == 0:
                    rows = perpage
            else:
                rows = perpage
            print("In page: " + str(page) + " " + str(rows) + " rows exist")

            for r in range(rows):
                current_row = r + 1
                r = r + 1

                edit_selector_str = ".el-table__row:nth-child(" + str(current_row) + ") .el-button:nth-child(1) > span"
                self.company_update_start(edit_selector_str)

                selector = "#__layout > section > section > main > div > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(2) > span:nth-child("
                target_list = ['test' + str(i) + '@luci.ai' for i in range(1, 31)]
                self.add_list(target_type="email", target_list=["info@luci.ai"], selector=selector)
                self.remove_list(target_type="email", target_list=target_list, selector=selector)

                self.company_create_update_submit(expectation)
