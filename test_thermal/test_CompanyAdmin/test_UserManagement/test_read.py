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
    TNB = COMPANYADMIN_USER_READ_TNB
    datafile = COMPANYADMIN_USER_READ_DATA_FILE

    authority = Authority()
    test_data_read_check_authority_info = authority.get_user_authority_info()
    @parameterized.expand(test_data_read_check_authority_info, skip_on_empty=True)
    @pytest.mark.scenario_regression_companyadmin(TNB + 2)
    @pytest.mark.scenario_regression(TNB + 1)
    def test_read_check_authority_info(self, email, company_list, site_dict, role_dict):
        self.check_authority_info(email=email, company_list=company_list, site_dict=site_dict,
                                  role_dict=role_dict, expectation="pass")

    test_data_read_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_read_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    def test_read_normal(self, companyname, username, expectation):
        self.user_read(companyname, username, expectation)