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
from test_thermal.test_CompanyAdmin.test_SiteManagement.SiteManageBaseComponent import SiteManageBaseComponent
import math
import datetime
import time
import json


class SiteManageBase(SiteManageBaseComponent):

    def check_authority_info(self, company, site, email_list, expectation="pass"):
        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=company)

        self.site_manage_enter()

        self.verify_site_authority(sitename=site, email_list=email_list)

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def site_create(self, companyname, sitename, address, latitude, longitude, label_list, user_list, expectation):

        self.start_test(locals())

        sitename, address, latitude, longitude, label_list, user_list, expectation = self.process_create_input(sitename,
                                                                                                               address,
                                                                                                               latitude,
                                                                                                               longitude,
                                                                                                               label_list,
                                                                                                               user_list,
                                                                                                               expectation)

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.site_manage_enter()

        self.site_create_start()

        self.site_create_update_set_sitename(sitename, expectation)

        self.site_create_update_set_address(address, expectation)

        # self.site_create_update_set_latitude(latitude, expectation)

        # self.site_create_update_set_longitude(longitude, expectation)

        fail_msg = None
        self.site_create_update_set_label(label_list=label_list, fail_msg=fail_msg, expectation=expectation)

        # self.site_create_update_set_user(user_list, expectation)

        self.site_create_update_submit(expectation)

        if expectation == "pass":
            # to avoid a bug that after create a new site, user list is blank
            self.refresh_page()
            self.site_manage_enter()
            self.verify_site_info(sitename, address, latitude, longitude, label_list, user_list)
            self.add_entity_record(company=companyname, site=[sitename])

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def site_read(self, companyname, sitename, expectation):
        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.site_manage_enter()

        found_site = self.site_search(sitename)
        if sitename == "":
            self.assert_true(found_site == {}, "Should not locate individual site")
        if sitename != "" and expectation == 'fail':
            self.assert_true(found_site == {}, "Should not found site: " + sitename)
        if sitename != "" and expectation == "pass":
            print("Try to find site: " + sitename)
            print("Find: " + str(found_site))
            self.assert_true(found_site["sitename"] == sitename,
                             "Try to find: " + sitename + "\n But find " + str(found_site))
        print("Try to find: " + sitename + "\n and find " + str(found_site))

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

    def site_delete(self, companyname, sitename, expectation):

        self.start_test(locals())

        self.login_company_admin()

        self.choose_company(companyname=companyname)

        self.site_manage_enter()

        time.sleep(10)  # too slow
        found_site = self.site_search(sitename)

        if expectation != "pass":
            self.assert_true(found_site == {}, "Should not find site: " + sitename)
        else:
            self.assertTrue(found_site != {}, "Can not find site: " + sitename)

            all_deleted = False
            authority = Authority()
            while not all_deleted:
                delete_selector = found_site["delete_selector"]
                self.site_delete_action(delete_selector)
                self.remove_authority_record(email_list=authority.get_email_list(bycolumn="site", value=sitename, company=companyname), site={companyname: [sitename]})

                # after delete， user list does not show
                self.refresh_page()
                self.site_manage_enter()

                found_site = self.site_search(sitename)
                if found_site == {}:
                    all_deleted = True

        self.logout(COMPANYADMIN_ACCOUNT)

        self.end_test(self._testMethodName)

