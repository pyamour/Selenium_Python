from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from parameterized import parameterized
import pytest
from utilities import utilities
from utilities import gmail
from utilities.Authority import Authority
from utilities.Entity import Entity
from utilities.Role import Role
from config.constants import *
import time
import datetime
import math


class ThermalBase(BaseCase):

    def start_test(self, locals):
        print("\n")
        print("Start testcase: " + str(locals["self"]))
        print("With data:")
        for key in locals.keys():
            if key != 'self':
                print(key + ": " + str(locals[key]))
        print("****************************************************************************")

    def end_test(self, method_name):
        print("End testcase: " + method_name)
        print("****************************************************************************")
        print("****************************************************************************")

    def login_application_user(self, username=APPLICATION_USER_ACCOUNT):
        authority = Authority()
        password = authority.get_user_info(email=APPLICATION_USER_ACCOUNT, column="password")
        self.login(username=APPLICATION_USER_ACCOUNT, password=password)

    def login_company_admin(self, username=COMPANYADMIN_ACCOUNT):
        authority = Authority()
        password = authority.get_user_info(email=COMPANYADMIN_ACCOUNT, column="password")
        self.login(username=COMPANYADMIN_ACCOUNT, password=password)

    def login_sysadmin(self):
        self.login(username=SYSADMIN_ACCOUNT, password=SYSADMIN_PASSWORD)

    def login(self, username=SYSADMIN_ACCOUNT, password=SYSADMIN_PASSWORD, url=HOME_URL, expectation="pass"):

        self.get(url)
        self.driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGH)

        if url != HOME_URL:
            time.sleep(6)
            current_url = self.get_current_url()
            print("Forward to: " + current_url)
            login_url = HOME_URL + "/login"
            self.assert_true(current_url == login_url, "Unauthorized visit to " + url)

        self.click("username1", by=By.ID)
        self.send_keys("username1", by=By.ID, text=username)
        self.send_keys("password1", by=By.ID, text=password)
        self.click(".login-button > span", by=By.CSS_SELECTOR)

        if expectation == "pass":
            self.assert_text("Login successfully", ".el-message__content")
            print("Login successfully")
        else:
            self.assert_true(self.is_element_present(
                "//p[contains(.,'Error: Invalid credentials during a bind operation. Code: 0x31')]"))

    def logout(self, username="sysadmin"):

        if username == "sysadmin":
            self.click(".el-icon-arrow-down", by=By.CSS_SELECTOR)
            self.click(".el-dropdown-menu__item", by=By.CSS_SELECTOR)
            print("Logout successfully")
        else:
            self.click(".el-icon-arrow-down:nth-child(2)", by=By.CSS_SELECTOR)
            # self.driver.find_element(By.XPATH, "//li[contains(.,\' Logout\')]").click()
            self.click("//li[contains(.,\' Logout\')]", by=By.XPATH)
            print("Logout successfully")

    def choose_company(self, companyname=""):
        if companyname == "":
            return
        if self.is_element_present(".el-icon-arrow-down:nth-child(1)"):
            self.click(".el-icon-arrow-down:nth-child(1)")
        else:
            time.sleep(6)
            self.click(".el-icon-arrow-down:nth-child(1)")

        # todo: get all options in el-dropdown-menu

        companyname_selector = "//li[contains(.,'" + companyname + "')]"
        self.click(companyname_selector)

    def site_manage_enter(self):
        self.click(".el-icon-s-tools", by=By.CSS_SELECTOR)
        self.click("tab-0", by=By.ID)
        time.sleep(10)  # wait for data loading  # todo: automatically monitor data loaded or not

    def user_manage_enter(self):
        self.click(".el-icon-s-tools", by=By.CSS_SELECTOR)
        self.click("tab-2", by=By.ID)
        time.sleep(10)  # wait for data loading  # todo: automatically monitor data loaded or not

    def role_manage_enter(self):
        self.click(".el-icon-s-tools", by=By.CSS_SELECTOR)
        self.click("tab-1", by=By.ID)
        time.sleep(10)  # wait for data loading  # todo: automatically monitor data loaded or not

    def get_page_navigation_info(self, total_selector):

        # total_selector = "#pane-2 > div > div:nth-child(2) > div:nth-child(2) > div > span.el-pagination__total"
        total_selector = total_selector
        if not self.is_element_present(total_selector):
            time.sleep(10)
        total_text = self.get_text(total_selector)
        total = int(total_text.strip().split(' ')[1])
        print("Result total: " + str(total))

        # todo: get perpage automatically
        perpage = 20

        # todo: get pages automatically
        pages = math.ceil(total / perpage)
        print("pages: " + str(pages))

        next_page_selector_str = ".el-icon-arrow-right"
        previous_page_selector_str = ".el-icon-arrow-left"

        return total, perpage, pages, next_page_selector_str, previous_page_selector_str

    def no_data_wait(self):
        if self.is_element_present("//span[contains(.,'No Data')]"):
            time.sleep(10)

    def process_user_profile_obsolete(self, username, password, company_list, site_list, role_list, expectation):
        [username, password, expectation] = map(str, [username, password, expectation])
        [company_list] = map(utilities.str_to_list, [company_list])
        [site_list, role_list] = map(utilities.str_to_dict, [site_list, role_list])

        return username, password, company_list, site_list, role_list, expectation

    def remove_add_list(self, target_type, target_list: list, selector, fail_msg=None, expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))

        # Get existing target list
        existing_list = []
        i = 0
        stop = False
        while not stop:
            i = i + 1
            if not self.is_element_present(selector + str(i) + ')'):
                stop = True
            else:
                existing_list.append(self.get_text(selector + str(i) + ')'))
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
            if self.is_element_present(selector + str(i) + ')'):
                target = self.get_text(selector + str(i) + ')')
                if target in to_delete_list:
                    self.click(selector + str(i) + ') > i')
                    to_delete_list.remove(target)
                    i = i - 1
            else:
                stop = True

        # To add
        for target in to_add_list:
            self.click(".button-new-tag > span", by=By.CSS_SELECTOR)
            self.send_keys(".input-new-tag > .el-input__inner", by=By.CSS_SELECTOR, text=target)
            self.send_keys(".input-new-tag > .el-input__inner", by=By.CSS_SELECTOR, text=Keys.ENTER)

        if expectation == "illegal_email_msg":  # To do: Now can only test add one target and the target is invalid case
            if fail_msg is not None:
                self.assert_true(fail_msg in self.get_text(".el-message__content"))
            print(self.get_text(".el-message__content"))

    def add_list(self, target_type, target_list: list, selector, fail_msg=None, expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))

        to_add_list = target_list
        print("To_add_" + target_type + "_list:   " + str(to_add_list))

        for target in to_add_list:
            self.click(".button-new-tag > span", by=By.CSS_SELECTOR)
            self.send_keys(".input-new-tag > .el-input__inner", by=By.CSS_SELECTOR, text=target)
            self.send_keys(".input-new-tag > .el-input__inner", by=By.CSS_SELECTOR, text=Keys.ENTER)

    def remove_list(self, target_type, target_list: list, selector, fail_msg=None, expectation="pass"):
        print(target_type + " to be set:  " + str(target_list))

        # Get existing target list
        existing_list = []
        i = 0
        stop = False
        while not stop:
            i = i + 1
            if not self.is_element_present(selector + str(i) + ')'):
                stop = True
            else:
                existing_list.append(self.get_text(selector + str(i) + ')'))
        print("Existing_" + target_type + "_list:  " + str(existing_list))

        to_delete_list = [i for i in target_list if i in existing_list]
        print("To_delete_" + target_type + "_list:   " + str(to_delete_list))

        i = 0
        stop = False
        while not stop and i < len(existing_list) and len(to_delete_list) > 0:
            i = i + 1
            if self.is_element_present(selector + str(i) + ')'):
                target = self.get_text(selector + str(i) + ')')
                if target in to_delete_list:
                    self.click(selector + str(i) + ') > i')
                    to_delete_list.remove(target)
                    i = i - 1
            else:
                stop = True

    def add_authority_record(self, email_list, password=None, status=None, company: list = None, site: dict = None,
                             role: dict = None):
        #print("At add_authority_record \n " + str(locals()))

        if email_list is None:
            return
        email_list = list(set(email_list))
        authority = Authority()
        for email in email_list:
            authority.add_authority(email, password=password, status=status, company=company, site=site, role=role)
        #print(str(authority.df))
        authority.commit()

    def remove_authority_record(self, email_list, password=None, status=None, company: list = None, site: dict = None,
                             role: dict = None):
        print("At remove_authority_record \n " + str(locals()))

        if email_list is None:
            return
        email_list = list(set(email_list))
        authority = Authority()
        for email in email_list:
            authority.remove_authority(email, company=company, site=site, role=role)
        print("At remove_authority_record, to save to file: ")
        print(str(authority.df))
        authority.commit()

    def add_entity_record(self, company, status=STATUS_ENABLED, site: list = None, camera: dict = None,
                          controller: dict = None):

        print("At add_entity_record \n " + str(locals()))

        if company is None:
            return

        entity = Entity()
        entity.add_entity(company=company, status=status, site=site, camera=camera, controller=controller)

        print(str(entity.df))
        entity.commit()

    def add_role_record(self, company, custome_role: list, service: dict):

        print("At add_role_record \n " + str(locals()))

        if company is None or custome_role is None or service is None or len(custome_role) == 0 or service == {}:
            return False

        role = Role()
        role.add_role(company=company, custome_role=custome_role, service=service)

        print(str(role.df))
        role.commit()

    def remove_role_record(self, company, custome_role: list):

        print("At add_role_record \n " + str(locals()))

        if company is None or custome_role is None or len(custome_role) == 0:
            return False

        role = Role()
        role.remove_role(company=company, custome_role=custome_role)

        print(str(role.df))
        role.commit()

    def request_reset_password(self, username, expectation="pass"):
        self.get(HOME_URL)
        self.click(".forget-credential")
        self.type("useremail", username, by=By.ID)
        self.click(".el-button--primary > span")

        if expectation != "fail_request_reset_password":
            pass_msg = "An email has been sent to your email. Follow the directions in the email to reset your password."
        else:
            pass_msg = "The email is not registered."
        self.assert_text(pass_msg, ".el-message__content")
        after = str(datetime.datetime.now().timestamp()).split(".")[0]
        print(self.get_text(".el-message__content"))
        return after

    def input_new_password(self, reset_url, password="Raptors@2019", expectation="pass"):
        self.get(reset_url)

        self.type("newpwd", password, by=By.ID)
        self.type("newpwdcheck", password, by=By.ID)
        self.click(".el-button > span")

        post_msg = self.get_text(".el-message__content")
        print(post_msg)
        if expectation == "pass":
            msg = "Your password has been reset successful."
            self.assert_true(msg in post_msg, "Cannot reset password")

        else:
            msg = "Your new password should contain uppercase, lowercase letters, special characters, digits and have at least 8 characters"
            self.assert_true(msg in post_msg, "Wrong password passed")

    def reset_password(self, username, password, expectation):
        after = self.request_reset_password(username=username, expectation=expectation)
        if expectation == "fail_request_reset_password":
            return
        reset_url = gmail.get_reset_password_url_in_gmail(receiver=username, after=after)
        self.input_new_password(reset_url, password, expectation)

        # self.login(username=username, password=password)
        # self.logout(username=username)
