from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_RoleManagement.RoleManageBase import RoleManageBase
from utilities import utilities
from config.constants import *

class TestUpdate(RoleManageBase):

    TNB = COMPANYADMIN_ROLE_UPDATE_TNB
    datafile = COMPANYADMIN_ROLE_UPDATE_DATA_FILE

    test_data_create_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='update_rolename_service_user')

    @parameterized.expand(test_data_create_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    @pytest.mark.scenario_regression(TNB + 1)
    @pytest.mark.scenario_debug(1)
    def test_update_update_rolename_service_user(self, companyname, rolename, valuedict, expectation):
        self.role_update(companyname=companyname, rolename=rolename, valuedict=valuedict, expectation=expectation)

########################################################################################################################


