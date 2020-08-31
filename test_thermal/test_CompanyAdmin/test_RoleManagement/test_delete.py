from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_RoleManagement.RoleManageBase import RoleManageBase
from utilities import utilities
from config.constants import *


class TestDelete(RoleManageBase):
    TNB = COMPANYADMIN_ROLE_DELETE_TNB
    datafile = COMPANYADMIN_ROLE_DELETE_DATA_FILE

    test_data_delete_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_delete_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    def test_delete_normal(self, companyname, rolename, expectation):
        self.role_delete(companyname, rolename, expectation)