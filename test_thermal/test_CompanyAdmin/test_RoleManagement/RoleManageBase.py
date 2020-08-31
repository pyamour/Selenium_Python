from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from utilities import utilities
from utilities import gmail
from utilities.Authority import Authority
from utilities.Role import Role
from config.constants import *
from test_thermal.ThermalBase import ThermalBase
from test_thermal.test_CompanyAdmin.test_RoleManagement.RoleManageBaseComponent import RoleManageBaseComponent
import math
import datetime
import time
import json


class RoleManageBase(RoleManageBaseComponent):

    def check_authority_info(self, company, role, email_list, expectation="pass"):
        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=company)

        self.role_manage_enter()

        self.verify_role_authority(rolename=role, email_list=email_list)

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def role_create(self, companyname, rolename, service_list, user_list, expectation):

        self.start_test(locals())

        companyname, rolename, service_list, user_list, expectation = self.process_create_input(companyname=companyname, rolename=rolename, service_list=service_list, user_list=user_list, expectation=expectation)
        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.role_manage_enter()

        self.role_create_start()

        self.role_create_update_set_rolename(rolename, expectation)

        self.role_create_update_set_service_list(service_list, expectation)

        self.role_create_update_set_user_list(user_list, expectation)

        self.role_create_update_submit(expectation)

        if expectation == "pass":
            time.sleep(10)  # Too slowly to refresh record in page
            self.verify_role_info(rolename, service_list, user_list)
            self.add_role_record(company=companyname, custome_role=[rolename], service={rolename: service_list})
            self.add_authority_record(email_list=user_list, company=[companyname], role={companyname: [rolename]})

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def role_update(self, companyname, rolename, valuedict, expectation="pass"):

        self.start_test(locals())

        companyname, rolename, key, value, expectation = self.process_update_input(companyname=companyname,
                                                                                                rolename=rolename,
                                                                                                valuedict=valuedict,
                                                                                                expectation=expectation)
        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.role_manage_enter()

        found_role = self.role_search(rolename=rolename)
        if found_role == {}:
            self.assertTrue(False, "Cannot find role: " + rolename)

        found_correct = found_role["rolename"] == rolename
        print("Found info: \n" + str(found_role))
        self.assert_true(found_correct,
                         "Found info doesn't match \n" + "Try to find: " + rolename + "\n But find " + str(
                             found_role))

        edit_selector = str(found_role["edit_selector"])
        self.role_update_start(edit_selector)

        role_entity = Role()
        role = rolename
        service_list = None
        user_list = None
        if "rolename" in key:
            role = str(value["rolename"])
            self.role_create_update_set_rolename(role)

        if "service" in key:
            service_list = str(value["service"])
            service_list = utilities.str_to_list(service_list)
            fail_msg = None
            self.role_create_update_set_service_list(service_list=service_list, fail_msg=fail_msg, expectation=expectation)

        if "user" in key:
            user_list = str(value["user"])
            user_list = utilities.str_to_list(user_list)
            fail_msg = None
            self.role_create_update_set_user_list(user_list=user_list, fail_msg=fail_msg, expectation=expectation)

        self.role_create_update_submit(expectation)

        if expectation == "pass":
            time.sleep(10)  # Too slowly to refresh record in page
            self.verify_role_info(role, service_list, user_list)

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def role_read(self, companyname, rolename, expectation):
        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.role_manage_enter()

        found_role = self.role_search(rolename)
        if rolename == "":
            self.assert_true(found_role == {}, "Should not locate individual role")
        if rolename != "" and expectation == 'fail':
            self.assert_true(found_role == {}, "Should not found role: " + rolename)
        if rolename != "" and expectation == "pass":
            print("Try to find role: " + rolename)
            print("Find: " + str(found_role))
            self.assert_true(found_role != {} and found_role["rolename"] == rolename,
                             "Try to find: " + rolename + "\n But find " + str(found_role))
        print("Try to find: " + rolename + "\n and find " + str(found_role))

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def role_delete(self, companyname, rolename, expectation):

        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.role_manage_enter()

        found_role = self.role_search(rolename)

        if expectation != "pass":
            self.assert_true(found_role == {}, "Should not find role: " + rolename)
        else:
            self.assertTrue(found_role != {}, "Can not find role: " + rolename)

            all_deleted = False
            authority = Authority()
            while not all_deleted:
                delete_selector = found_role["delete_selector"]
                self.role_delete_action(delete_selector)
                self.remove_authority_record(
                    email_list=authority.get_email_list(bycolumn="role", value=rolename, company=companyname),
                    role={companyname: [rolename]})
                # self.remove_role_record(company=companyname, custome_role=[rolename])

                time.sleep(6)  # wait for refresh
                found_role = self.role_search(rolename)
                if found_role == {}:
                    all_deleted = True

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)
