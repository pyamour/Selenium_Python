from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from test_thermal.test_SuperAdmin.SysAdminBase import SysAdminBase
from utilities import utilities
from config.constants import *

class TestUpdate(SysAdminBase):

    TNB = SYSADMIN_COMPANY_UPDATE_TNB
    datafile = SYSADMIN_COMPANY_UPDATE_DATA_FILE

    test_data_update_update_companyname = utilities.gen_testdata(datafile, delimiter=',', header=0, scenario='update_companyname')
    @parameterized.expand(test_data_update_update_companyname)
    @pytest.mark.scenario_regression(TNB+1)
    def test_update_update_companyname(self,companyname,valuedict,expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_status = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                            scenario='update_status')
    @parameterized.expand(test_data_update_update_status)
    @pytest.mark.scenario_regression(TNB+2)
    def test_update_update_status(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                           scenario='update_email')
    @parameterized.expand(test_data_update_update_email)
    @pytest.mark.scenario_regression(TNB+3)
    def test_update_update_email(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_companyname_status_email = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                              scenario='update_companyname_status_email')
    @parameterized.expand(test_data_update_update_companyname_status_email)
    @pytest.mark.scenario_regression(TNB+4)
    def test_update_update_companyname_status_email(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_companyname_duplicate = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                           scenario='update_companyname_duplicate')
    @parameterized.expand(test_data_update_update_companyname_duplicate)
    @pytest.mark.scenario_regression(TNB+5)
    @pytest.mark.skip
    def test_update_update_companyname_duplicate(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_companyname_rule = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                      scenario='update_companyname_rule')

    @parameterized.expand(test_data_update_update_companyname_rule)
    @pytest.mark.scenario_regression(TNB+6)
    def test_update_update_companyname_rule(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_companyname_illegal = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                         scenario='update_companyname_illegal')

    @parameterized.expand(test_data_update_update_companyname_illegal)
    @pytest.mark.scenario_regression(TNB+7)
    def test_update_update_companyname_illegal(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email_duplicate = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                     scenario='update_email_duplicate')
    @parameterized.expand(test_data_update_update_email_duplicate)
    @pytest.mark.scenario_regression(TNB+8)
    def test_update_update_email_duplicate(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email_two_same = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                    scenario='update_email_two_same')

    @parameterized.expand(test_data_update_update_email_two_same)
    @pytest.mark.scenario_regression(TNB+9)
    def test_update_update_email_two_same(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email_blank = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                 scenario='update_email_blank')
    @parameterized.expand(test_data_update_update_email_blank)
    @pytest.mark.scenario_regression(TNB+10)
    def test_update_update_email_blank(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email_illegal = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                   scenario='update_email_illegal')
    @parameterized.expand(test_data_update_update_email_illegal)
    @pytest.mark.scenario_regression(TNB+11)
    def test_update_update_email_illegal(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email_remove = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                                  scenario='update_email_remove')

    @parameterized.expand(test_data_update_update_email_remove)
    @pytest.mark.scenario_regression(TNB+13)
    def test_update_update_email_remove(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################

    test_data_update_update_email_add = utilities.gen_testdata(datafile, delimiter=',', header=0,
                                                               scenario='update_email_add')

    @parameterized.expand(test_data_update_update_email_add)
    @pytest.mark.scenario_regression(TNB+12)
    def test_update_update_email_add(self, companyname, valuedict, expectation):
        self.company_update(companyname, valuedict, expectation)

########################################################################################################################
