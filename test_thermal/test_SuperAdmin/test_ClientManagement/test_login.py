from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_SuperAdmin.SysAdminBase import SysAdminBase
from utilities import utilities
from config.constants import *

class TestLogin(SysAdminBase):

    TNB = SYSADMIN_COMPANY_LOGIN_TNB
    datafile = SYSADMIN_COMPANY_LOGIN_DATA_FILE

####################################################################################################################################

    test_data_login_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')
    @parameterized.expand(test_data_login_normal)
    @pytest.mark.scenario_regression(TNB + 1)
    def test_login_normal(self, username, password, url, expectation):
        self.superadmin_login(expectation=expectation)

####################################################################################################################################

    test_data_login_unauthorized_url = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='unauthorized_url')
    @parameterized.expand(test_data_login_unauthorized_url)
    @pytest.mark.scenario_regression(TNB + 2)
    def test_unauthorized_url(self, username, password, url, expectation):
        self.superadmin_login(url=url, expectation=expectation)

####################################################################################################################################

    test_data_login_illegal_name_password = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                              scenario='illegal_name_password')
    @parameterized.expand(test_data_login_illegal_name_password)
    @pytest.mark.scenario_regression(TNB + 3)
    def test_illegal_name_password(self, username, password, url, expectation):
        self.superadmin_login(username=username, password=password, expectation=expectation)

####################################################################################################################################

    test_data_login_reset_password_normal = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                   scenario='reset_password_normal')
    @parameterized.expand(test_data_login_reset_password_normal)
    @pytest.mark.scenario_regression(TNB + 4)
    def test_reset_password_normal(self, username, password, url, expectation):
        self.superadmin_reset_password(username=username, password=password, expectation=expectation)

####################################################################################################################################

    test_data_login_reset_password_wrong_password = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                            scenario='reset_password_wrong_password')
    @parameterized.expand(test_data_login_reset_password_wrong_password)
    @pytest.mark.scenario_regression(TNB + 5)
    def test_reset_password_wrong_password(self, username, password, url, expectation):
        self.superadmin_reset_password(username=username, password=password, expectation=expectation)

####################################################################################################################################

    test_data_login_reset_password_wrong_email = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                            scenario='reset_password_wrong_email')
    @parameterized.expand(test_data_login_reset_password_wrong_email)
    @pytest.mark.scenario_regression(TNB + 6)
    def test_reset_password_wrong_password(self, username, password, url, expectation):
        self.superadmin_reset_password(username=username, password=password, expectation=expectation)

####################################################################################################################################