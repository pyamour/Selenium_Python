from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_RoleManagement.RoleManageBase import RoleManageBase
from utilities import utilities
from config.constants import *

class TestCreate(RoleManageBase):

    TNB = COMPANYADMIN_ROLE_CREATE_TNB
    datafile = COMPANYADMIN_ROLE_CREATE_DATA_FILE

    test_data_create_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_create_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    @pytest.mark.scenario_regression(TNB + 1)
    def test_create_normal(self, companyname, rolename, service_list, user_list, expectation):
        self.role_create(companyname=companyname, rolename=rolename, service_list=service_list, user_list=user_list, expectation=expectation)

########################################################################################################################


