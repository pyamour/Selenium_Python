from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_CompanyAdmin.test_SiteManagement.SiteManageBase import SiteManageBase
from utilities import utilities
from utilities.Authority import Authority
from config.constants import *


class TestRead(SiteManageBase):
    TNB = COMPANYADMIN_SITE_READ_TNB
    datafile = COMPANYADMIN_SITE_READ_DATA_FILE

    test_data_read_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_read_normal)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    def test_read_normal(self, companyname, sitename, expectation):
        self.site_read(companyname, sitename, expectation)

    authority = Authority()
    test_data_read_check_authority_info = authority.get_site_authority_info()

    @parameterized.expand(test_data_read_check_authority_info, skip_on_empty=True)  # skip_on_empty=True doesn't work, while there is no site, pytest will run wrong
    @pytest.mark.scenario_regression_companyadmin(TNB + 2)
    def test_read_check_authority_info(self, company, site, email_list):
        self.check_authority_info(company=company, site=site, email_list=email_list, expectation="pass")
