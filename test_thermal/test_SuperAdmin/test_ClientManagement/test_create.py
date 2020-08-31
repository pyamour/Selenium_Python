from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_SuperAdmin.SysAdminBase import SysAdminBase
from utilities import utilities
from config.constants import *

class TestCreate(SysAdminBase):

    TNB = SYSADMIN_COMPANY_CREATE_TNB
    datafile = SYSADMIN_COMPANY_CREATE_DATA_FILE

    test_data_create_normal = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='normal')
    @parameterized.expand(test_data_create_normal)
    @pytest.mark.scenario_regression(TNB+1)
    def test_create_normal(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_name_rule = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='name_rule')
    @parameterized.expand(test_data_create_name_rule)
    @pytest.mark.scenario_regression(TNB+2)
    def test_create_name_rule(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_name_duplicate = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='name_duplicate')
    @parameterized.expand(test_data_create_name_duplicate)
    @pytest.mark.scenario_regression(TNB+3)
    @pytest.mark.skip #system does not check duplicate company name
    def test_create_name_duplicate(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_name_illegal = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                           scenario='name_illegal')
    @parameterized.expand(test_data_create_name_illegal)
    @pytest.mark.scenario_regression(TNB+4)
    def test_create_name_illegal(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)
########################################################################################################################

    test_data_create_email_duplicate = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                              scenario='email_duplicate')
    @parameterized.expand(test_data_create_email_duplicate)
    @pytest.mark.scenario_regression(TNB+5)
    def test_create_email_duplicate(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_email_two_same_email = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                   scenario='email_two_same_email')

    @parameterized.expand(test_data_create_email_two_same_email)
    @pytest.mark.scenario_regression(TNB+6)
    def test_create_email_two_same_email(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_email_blank = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                          scenario='email_blank')
    @parameterized.expand(test_data_create_email_blank)
    @pytest.mark.scenario_regression(TNB+7)
    def test_create_email_blank(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_email_illegal = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                            scenario='email_illegal')

    @parameterized.expand(test_data_create_email_illegal)
    @pytest.mark.scenario_regression(TNB+8)
    def test_create_email_illegal(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_create_status = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                     scenario='status')

    @parameterized.expand(test_data_create_status)
    @pytest.mark.scenario_regression(TNB+9)
    @pytest.mark.skip  # do not support to create a disabled company
    def test_create_status(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)

########################################################################################################################

    test_data_for_companyadmin_test = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                     scenario='for_companyadmin_test')

    @parameterized.expand(test_data_for_companyadmin_test)
    @pytest.mark.scenario_regression(TNB + 10)
    @pytest.mark.scenario_regression_companyadmin(TNB + 1)
    @pytest.mark.skip   # run only once
    def test_create_for_companyadmin_test(self, companyname, status, email_list, expectation):
        self.company_create(companyname, status, email_list, expectation)
########################################################################################################################

    @pytest.mark.scenario_regression(TNB+11)
    @pytest.mark.scenario_regression_companyadmin(TNB + 2)
    def test_create_verify_companyadmin_password_email(self):
        self.verify_companyadmin_password_email()
