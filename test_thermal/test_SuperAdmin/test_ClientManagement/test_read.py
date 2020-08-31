from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_SuperAdmin.SysAdminBase import SysAdminBase
from utilities import utilities
from config.constants import *


class TestRead(SysAdminBase):
    TNB = SYSADMIN_COMPANY_READ_TNB
    datafile = SYSADMIN_COMPANY_READ_DATA_FILE

    test_data_read_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')

    @parameterized.expand(test_data_read_normal)
    @pytest.mark.scenario_regression(TNB + 3)
    def test_read_normal(self, companyname, expectation):
        self.company_read(companyname, expectation)

    test_data_read_notexist = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='notexist')

    @parameterized.expand(test_data_read_notexist)
    @pytest.mark.scenario_regression(TNB + 2)
    def test_read_notexist(self, companyname, expectation):
        self.company_read(companyname, expectation)

    @pytest.mark.scenario_regression(TNB + 1)
    def test_read_default(self):
        self.company_read(companyname="", expectation="pass")
