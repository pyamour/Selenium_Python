from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_SiteManagement.SiteManageBase import SiteManageBase
from utilities import utilities
from config.constants import *


class TestDelete(SiteManageBase):
    TNB = COMPANYADMIN_SITE_DELETE_TNB
    datafile = COMPANYADMIN_SITE_DELETE_DATA_FILE

    test_data_delete_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_delete_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    @pytest.mark.scenario_regression(TNB + 1)
    def test_delete_normal(self, companyname, sitename, expectation):
        self.site_delete(companyname, sitename, expectation)
