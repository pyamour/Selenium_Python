from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_SuperAdmin.SysAdminBase import SysAdminBase
from utilities import utilities
from config.constants import *

class TestDelete(SysAdminBase):

    TNB = SYSADMIN_COMPANY_DELETE_TNB
    datafile = SYSADMIN_COMPANY_DELETE_DATA_FILE

    test_data_delete_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')
    @parameterized.expand(test_data_delete_normal)
    @pytest.mark.scenario_regression(TNB+1)
    def test_delete_normal(self, companyname, expectation):
        self.company_delete(companyname, expectation)

    test_data_delete_notexist = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='notexist')
    @parameterized.expand(test_data_delete_notexist)
    @pytest.mark.scenario_regression(TNB+2)
    def test_delete_notexist(self, companyname, expectation):
        self.company_delete(companyname, expectation)

    @pytest.mark.scenario_renew_env(1)
    @pytest.mark.scenario_regression_companyadmin(1)
    def test_delete_emptify_testuser(self, expectation="pass"):   # add info@luci.ai to each company as admin, and delete all other company admins
        self.company_delete_emptify_user(expectation)

    @pytest.mark.scenario_renew_env(2)
    @pytest.mark.skip
    def test_delete_emptify_company(self, companyname="", expectation="pass"):  #empty all test company data
        self.company_delete_emptify_company(companyname, expectation)