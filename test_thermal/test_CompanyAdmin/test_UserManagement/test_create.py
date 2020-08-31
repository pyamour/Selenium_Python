from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_UserManagement.UserManageBase import UserManageBase
from utilities import utilities
from utilities.Authority import Authority
from config.constants import *


class TestRead(UserManageBase):
    TNB = COMPANYADMIN_USER_CREATE_TNB
    datafile = COMPANYADMIN_USER_CREATE_DATA_FILE

    test_data_create_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_create_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    def test_create_normal(self, companyname, username, display_name, status, site_list, role_list, expectation):
        self.user_create(companyname=companyname, username=username, display_name=display_name, status=status, site_list=site_list, role_list=role_list,
                         expectation=expectation)
