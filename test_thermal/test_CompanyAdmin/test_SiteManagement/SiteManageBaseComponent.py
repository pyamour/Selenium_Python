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


class SiteManageBaseComponent(ThermalBase):

    def process_create_input(self, sitename, address, latitude, longitude, label_list, user_list, expectation):
        [sitename, address, latitude, longitude, expectation] = map(str, [sitename, address, latitude, longitude, expectation])
        [label_list, user_list] = map(utilities.str_to_list, [label_list, user_list])
        return sitename, address, latitude, longitude, label_list, user_list, expectation

    def verify_site_authority(self, sitename, email_list=None):
        print("Start to verify site authority")
        local = locals()
        local.pop('self')
        print(local)

        found_site = self.site_search(sitename)
        if found_site == {}:
            self.assertTrue(False, "Cannot find site: " + sitename)
        correct_info = found_site["sitename"] == sitename

        if correct_info and email_list != None:
            found_email_list = list(set(found_site["user_list"]))
            email_list = list(set(email_list))
            correct_info = correct_info and sorted(found_email_list) == sorted(email_list)
            if not correct_info:
                print("Email list doesn't match")

        if correct_info:
            print("Expected: " + str(local))
            print("Got: " + str(found_site))
        self.assertTrue(correct_info, "Site info doesn't match \n" + "Expected: " + str(
            local) + "\n" + "Got: " + str(found_site))

    def site_create_start(self):
        self.click(".el-icon-plus", by=By.CSS_SELECTOR)

    def site_create_update_set_sitename(self, sitename, expectation="pass"):
        self.type(".name-container > div:nth-child(2) .el-input__inner", sitename)

    def site_create_update_set_address(self, address, expectation="pass"):
        self.type("div:nth-child(4) .el-input__inner", address)

    def site_create_update_set_latitude(self, latitude, expectation="pass"):
        self.type("div:nth-child(6) .el-input__inner", latitude)

    def site_create_update_set_longitude(self, longitude, expectation="pass"):
        self.type("div:nth-child(8) .el-input__inner", longitude)

    def site_create_update_set_label(self, label_list: list, fail_msg=None, expectation="pass"):
        selector = "#pane-0 > div > div:nth-child(2) > div.el-dialog__wrapper > div > div.el-dialog__body > div > div.administrator-container > div:nth-child(2) > span:nth-child("
        self.remove_add_list(target_type="label", target_list=label_list, selector=selector, fail_msg=fail_msg,
                             expectation=expectation)

    def site_create_update_set_user(self, user_list, expectation="pass"):
        pass

    def site_search(self, sitename):
        # Only return one site with latest date
        #Todo: use option selector

        print("Search: " + sitename)
        total_selector = "#pane-0 > div > div:nth-child(2) > div:nth-child(2) > div > span.el-pagination__total"
        total, perpage, pages, next_page_selector_str, previous_page_selector_str = self.get_page_navigation_info(
            total_selector)

        if sitename == "":
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

            for r in range(rows):
                date_selector_str = "//tr[" + str(r + 1) + "]/td[1]/div"
                name_selector_str = "//tr[" + str(r + 1) + "]/td[2]/div"
                address_selector_str = "//tr[" + str(r + 1) + "]/td[3]/div"
                label_selector_str = "//tr[" + str(r + 1) + "]/td[4]/div"
                user_selector_str = "//tr[" + str(r + 1) + "]/td[5]/div"
                # user_selector_str = '//*[@id="pane-0"]/div/div[2]/div[1]/div[1]/div[3]/table/tbody/tr[' + str(r + 1) + ']/td[5]/div/table'
                edit_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") .el-button:nth-child(1) > span"
                # edit_selector_str = "/tr[" + str(r+1) +"]/td[7]/div/button[1]/span"
                delete_selector_str = ".el-table__row:nth-child(" + str(r + 1) + ") .el-button:nth-child(2) > span"
                # delete_selector_str = "/tr[" + str(r+1) +"]/td[7]/div/button[2]/span"

                if self.is_element_present(name_selector_str):
                    row_sitename = self.get_text(name_selector_str)
                    row_date = self.get_text(date_selector_str)
                    print("In row: " + str(r + 1) + " sitename: " + row_sitename + " date: " + row_date)
                    if row_sitename == sitename and datetime.datetime.strptime(str(row_date), '%b %d, %Y').date() > datetime.datetime.strptime(str(max_date), '%b %d, %Y').date():
                        max_date = row_date
                        dest_page = page
                        print("Got one match max_date:  " + max_date + "   dest_page:  " + str(dest_page))

                        info_dict["sitename"] = row_sitename
                        info_dict["date"] = row_date
                        info_dict["address"] = self.get_text(address_selector_str)
                        info_dict["label_list"] = utilities.str_to_list(self.get_text(label_selector_str))
                        if not self.is_element_present(user_selector_str):
                            time.sleep(10)
                        print("Got user list from page: " + self.get_text(user_selector_str))
                        info_dict["user_list"] = utilities.str_to_list(self.get_text(user_selector_str))
                        info_dict["edit_selector"] = edit_selector_str
                        info_dict["delete_selector"] = delete_selector_str
                        info_dict["name_selector"] = name_selector_str
                        info_dict["date_selector"] = date_selector_str
        if int(dest_page) > 0:
            for i in range(pages - dest_page):
                # self.type(".el-pagination__editor > .el-input__inner", str(dest_page) + Keys.ENTER)
                self.click(previous_page_selector_str)
                # self.wait_for_ready_state_complete()
                print("Go to page:  " + str(pages - i - 1))
        print("Finally got max_date:  " + max_date + "   dest_page:  " + str(dest_page))
        return info_dict

    def verify_site_info(self, sitename, address, latitude, longitude, label_list, user_list):
        print("Start to verify site info")
        local = locals()
        local.pop('self')
        print(local)

        found_site = self.site_search(sitename)
        if found_site == {}:
            self.assertTrue(False, "Cannot find site: " + sitename)
        correct_info = found_site["sitename"] == sitename
        if correct_info and address != None:
            correct_info = correct_info and found_site["address"] == address
        # if correct_info and latitude != None:
        #     correct_info = correct_info and found_site["latitude"] == latitude
        # if correct_info and longitude != None:
        #     correct_info = correct_info and found_site["longitude"] == longitude
        if correct_info and label_list != None:
            found_label_list = list(set(found_site["label_list"]))
            label_list = list(set(label_list))
            correct_info = correct_info and sorted(found_label_list) == sorted(label_list)

        if correct_info and user_list != None:
            found_user_list = list(set(found_site["user_list"]))
            user_list = list(set(user_list))
            correct_info = correct_info and sorted(found_user_list) == sorted(user_list)

        if not correct_info:
            print("Site info doesn't match")
        print("Expected: " + str(local))
        print("Got: " + str(found_site))
        self.assertTrue(correct_info, "Site info doesn't match \n" + "Expected: " + str(
            local) + "\n" + "Got: " + str(found_site))

        return found_site

    def site_create_update_submit(self, expectation):
        self.click(".el-button--primary:nth-child(2)", by=By.CSS_SELECTOR)

        if expectation == "pass":
            print(self.get_text(".el-message__content"))
            #self.assert_text("Success", ".el-message__content")

    def site_delete_action(self, delete_selector):
        self.click(delete_selector, by=By.CSS_SELECTOR)
        self.click(".el-message-box__btns > .el-button--primary > span", by=By.CSS_SELECTOR)
        self.assert_text("The site has been successfully deleted", ".el-message__content")
        print(self.get_text(".el-message__content"))
