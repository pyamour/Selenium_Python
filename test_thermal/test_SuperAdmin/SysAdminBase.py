from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from utilities import utilities
from utilities import gmail
from utilities.Authority import Authority
from utilities.Entity import Entity
from config.constants import *
from test_thermal.test_SuperAdmin.SysAdminBaseComponent import SysAdminBaseComponent
import math
import datetime
import time
import json

class SysAdminBase(SysAdminBaseComponent):

    def company_create(self, companyname, status, email_list, expectation):

        self.start_test(locals())

        companyname, status, email_list, expectation = self.process_create_input(companyname, status, email_list, expectation)

        self.login_sysadmin()

        self.company_create_start()

        self.company_create_update_set_companyname(companyname)

        self.company_create_update_set_status(status)

        if expectation == "illegal_email_msg":
            fail_msg = "The email address is invalid"
        else:
            fail_msg = None
        self.company_create_update_set_email(email_list=email_list, fail_msg=fail_msg, expectation=expectation)

        self.company_create_update_submit(expectation)

        if expectation == "pass":
            self.verify_company_info(companyname, status, email_list)
            # self.add_user_profile(email_list, company=[companyname])
            # self.add_user_profile(email_list, role={companyname: [ROLE_COMPANY_ADMIN]})
            # self.add_user_profile(email_list, site={companyname: [SITE_ANY_SITE]})
            self.add_authority_record(email_list, company=[companyname], site={companyname: [SITE_ANY_SITE]}, role={companyname: [ROLE_COMPANY_ADMIN]})
            self.add_entity_record(company=companyname)

        self.logout()

        self.end_test(self._testMethodName)

    def verify_companyadmin_password_email(self):

        self.start_test(locals())

        # get email_list
        authority = Authority()
        email_list = authority.get_email_list(bycolumn="role", value=ROLE_COMPANY_ADMIN)

        print("Start to check email and password for:  " + str(email_list))

        valuedict = self.verify_password_email(email_list)
        self.assert_true(valuedict != [], "Did not send email or password to: " + str(email_list))

        for item in valuedict:
            authority.add_authority(email=item["email"], password=item["password"])
        print(str(authority.df))
        authority.commit()

        self.end_test(self._testMethodName)

    def company_update(self, companyname, valuedict, expectation):

        self.start_test(locals())

        companyname, key, value, expectation = self.process_update_input(companyname, valuedict, expectation)

        self.login_sysadmin()

        found_company = self.company_search(companyname)
        if found_company == {}:
            self.assertTrue(False, "Cannot find company: " + companyname)

        found_correct = found_company["companyname"] == companyname \
                        and self.get_text(found_company["name_selector"]) == found_company["companyname"] \
                        and self.get_text(found_company["id_selector"]) == found_company["id"]
        print("Found info: \n" + str(found_company))
        self.assert_true(found_correct, "Found info doesn't match what show on user interface \n" + "Try to find: " + companyname + "\n But find " + str(found_company))
        
        edit_selector = str(found_company["edit_selector"])

        if True:
            self.company_update_start(edit_selector)
            authority = Authority()

            company = companyname
            if "companyname" in key:
                company = str(value["companyname"])
                self.company_create_update_set_companyname(company)
                email_list = authority.get_email_list(bycolumn="company", value=companyname)
                for email in email_list:
                    authority.update_authority_list_value_column(email=email, column="company", value=[companyname], action="remove")
                    authority.update_authority_list_value_column(email=email, column="company", value=[company], action="add")

            if "status" in key:
                status = str(value["status"])
                self.company_create_update_set_status(status)
            else:
                status = None

            if "email" in key:
                email_list = str(value["email"])
                email_list = utilities.str_to_list(email_list)
                if expectation == "illegal_email_msg":
                    fail_msg = "The email address is invalid"
                else:
                    fail_msg = None
                self.company_create_update_set_email(email_list=email_list, fail_msg=fail_msg, expectation=expectation)

                # deal with user profile
                # email list connected with target company
                existing_connected_email_list = authority.get_email_list(bycolumn="company", value=company)

                to_add_connection_email_list = [i for i in email_list if i not in existing_connected_email_list]
                print("To_add_connection_email_list:   " + str(to_add_connection_email_list))
                for email in to_add_connection_email_list:
                    authority.add_authority(email=email, company=[company])

                to_delete_email_list = [i for i in existing_connected_email_list if i not in email_list]
                print("To_delete_email_list:   " + str(to_delete_email_list))  #remove connection
                for email in to_delete_email_list:
                    authority.update_authority_list_value_column(email=email, column="company", value=[company], action="remove")
            else:
                email_list = None

            self.company_create_update_submit(expectation)

            if expectation == "pass":
                self.verify_company_info(company, status, email_list)
                print("start to update user profile with: \n" + str(authority.df))
                authority.commit()

        self.logout()

        self.end_test(self._testMethodName)

    def company_read(self, companyname, expectation):

        self.start_test(locals())

        self.login_sysadmin()

        found_company = self.company_search(companyname)
        if companyname == "":
            self.assert_true(found_company == {}, "Should not locate individual company")
        if companyname != "" and expectation == 'fail':
            self.assert_true(found_company == {}, "Should not found company: " + companyname)
        if companyname != "" and expectation == "pass":
            print("Try to find company: " + companyname)
            print("Find: " + str(found_company))
            self.assert_true(found_company["companyname"] == companyname, "Try to find: " + companyname + "\n But find " + str(found_company))

        self.logout()

        self.end_test(self._testMethodName)

    def company_delete(self, companyname, expectation):

        self.start_test(locals())

        self.login()

        found_company = self.company_search(companyname)

        if expectation != "pass":
            self.assertTrue(found_company == {})
        else:
            self.assertTrue(found_company != {})

            all_deleted = False
            while not all_deleted:
                delete_selector = found_company["delete_selector"]
                self.company_delete_action(delete_selector)
                found_company = self.company_search(companyname)
                if found_company == {}:
                    all_deleted = True

        self.logout()

        self.end_test(self._testMethodName)

    def superadmin_login(self, username=SYSADMIN_ACCOUNT, password=SYSADMIN_PASSWORD, url=HOME_URL, expectation="pass"):

        self.start_test(locals())

        self.login(username=username, password=password, url=url, expectation=expectation)

        if expectation == "pass":
            self.logout()

        self.end_test(self._testMethodName)

    def superadmin_reset_password(self, username, password, expectation):

        self.start_test(locals())

        self.reset_password(username=username, password=password, expectation=expectation)

        if expectation == "pass":
            self.login(username=username, password=password, expectation="pass")
            self.add_authority_record(email_list=[username], password=password)
            self.logout(username=username)
        if expectation == "fail_input_password":
            self.login(username=username, password=password, expectation="fail")
        if expectation == "fail_request_reset_password":
            pass

        self.end_test(self._testMethodName)

    def company_delete_emptify_company(self, companyname, expectation):

        self.start_test(locals())

        self.login()

        self.company_emptify_company_action(companyname)

        self.logout()

        self.end_test(self._testMethodName)

    def company_delete_emptify_user(self, expectation="pass"):

        self.start_test(locals())

        self.login_sysadmin()

        self.company_emptify_user_action()

        self.logout()

        self.end_test(self._testMethodName)