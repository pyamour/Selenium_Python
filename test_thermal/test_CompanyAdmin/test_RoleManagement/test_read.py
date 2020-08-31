from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_RoleManagement.RoleManageBase import RoleManageBase
from utilities import utilities
from utilities.Authority import Authority
from config.constants import *


class TestRead(RoleManageBase):
    TNB = COMPANYADMIN_ROLE_READ_TNB
    datafile = COMPANYADMIN_ROLE_READ_DATA_FILE

    test_data_read_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_read_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    def test_read_normal(self, companyname, rolename, expectation):
        self.role_read(companyname, rolename, expectation)

    authority = Authority()
    test_data_read_check_authority_info = authority.get_role_authority_info()

    @parameterized.expand(test_data_read_check_authority_info, skip_on_empty=True)  # skip_on_empty=True doesn't work
    @pytest.mark.scenario_regression_companyadmin(TNB + 2)
    @pytest.mark.scenario_regression(TNB + 1)
    def test_read_check_authority_info(self, company, role, email_list):
        self.check_authority_info(company=company, role=role, email_list=email_list, expectation="pass")
