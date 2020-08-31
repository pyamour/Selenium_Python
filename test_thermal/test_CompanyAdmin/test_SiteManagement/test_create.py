from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_SiteManagement.SiteManageBase import SiteManageBase
from utilities import utilities
from config.constants import *

class TestCreate(SiteManageBase):

    TNB = COMPANYADMIN_SITE_CREATE_TNB
    datafile = COMPANYADMIN_SITE_CREATE_DATA_FILE

    test_data_create_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_create_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    def test_create_normal(self, companyname, sitename, address, latitude, longitude, label_list, user_list, expectation):
        self.site_create(companyname, sitename, address, latitude, longitude, label_list, user_list, expectation)

########################################################################################################################


