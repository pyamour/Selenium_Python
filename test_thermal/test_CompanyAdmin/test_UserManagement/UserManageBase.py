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
from test_thermal.test_CompanyAdmin.test_UserManagement.UserManageBaseComponent import UserManageBaseComponent
import math
import datetime
import time
import json


class UserManageBase(UserManageBaseComponent):

    def check_authority_info(self, email, company_list, site_dict, role_dict, expectation="pass"):
        self.start_test(locals())

        self.login_company_admin()

        for company in company_list:
            self.choose_company(companyname=company)

            self.user_manage_enter()

            time.sleep(10)

            site_list = site_dict[company]
            role_list = role_dict[company]
            self.verify_user_authority(username=email, site_list=site_list, role_list=role_list)

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def user_create(self, companyname, username, display_name, status, site_list, role_list, expectation="pass"):

        self.start_test(locals())

        companyname, username, display_name, status, site_list, role_list, expectation = self.process_create_input(companyname, username, display_name, status, site_list, role_list, expectation)

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.user_manage_enter()

        self.user_create_start()

        self.user_create_update_set_username(username, expectation)

        #self.user_create_update_set_display_name(display_name, expectation)

        self.user_create_update_set_status(status, expectation)

        fail_msg = None
        self.user_create_update_set_site(site_list=site_list, fail_msg=fail_msg, expectation=expectation)

        fail_msg = None
        self.user_create_update_set_role(role_list=role_list, fail_msg=fail_msg, expectation=expectation)

        self.user_create_update_submit(expectation)

        if expectation == "pass":
            time.sleep(10)
            self.verify_user_info(username, display_name, status, site_list, role_list)
            self.add_authority_record(email_list=[username], company=[companyname], site={companyname: site_list}, role={companyname: role_list})
            # self.add_user_record() # later when test userprofile

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def user_read(self, companyname, username, expectation):

        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.user_manage_enter()

        found_user = self.user_search(username)
        if username == "":
            self.assert_true(found_user == {}, "Should not locate individual user")
        if username != "" and expectation == 'fail':
            self.assert_true(found_user == {}, "Should not found user: " + username)
        if companyname != "" and expectation == "pass":
            print("Try to find user: " + username)
            print("Find: " + str(found_user))
            self.assert_true(found_user["username"] == username,
                             "Try to find: " + username + "\n But find " + str(found_user))

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def user_delete(self, companyname, username, expectation):

        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.user_manage_enter()

        found_user = self.user_search(username)

        if expectation != "pass":
            self.assertTrue(found_user == {})
        else:
            self.assertTrue(found_user != {})

            all_deleted = False
            authority = Authority()
            while not all_deleted:
                delete_selector = found_user["delete_selector"]
                self.user_delete_action(delete_selector)
                self.remove_authority_record(email_list=[username], company=[companyname])
                time.sleep(10)  # wait refresh
                found_user = self.user_search(username)
                if found_user == {}:
                    all_deleted = True

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)