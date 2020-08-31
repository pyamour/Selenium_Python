from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized
import pytest
from utilities import utilities
from utilities import gmail
from config.constants import *
from test_thermal.ThermalBase import ThermalBase

class  TestLogin(ThermalBase):

    def test_login(self, username="superadmin", password="lifeisgood"):
        print("\n")
        print("Start testcase: " + self._testMethodName)

        username = "xxxxx"
        password = "xxxxx"

        self.login(username=username, password=password)
        self.logout(username=username)

        print("End testcase: " + self._testMethodName)