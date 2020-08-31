import os

###############          Path             ###############################

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

AUTHORITY_DATA_FILE = ROOT_PATH + '/test_thermal/data_authority.csv'
ENTITY_DATA_FILE = ROOT_PATH + '/test_thermal/data_entity.csv'
ROLE_DATA_FILE = ROOT_PATH + '/test_thermal/data_role.csv'

SYSADMIN_COMPANY_CREATE_DATA_FILE = ROOT_PATH + '/test_thermal/test_SuperAdmin/test_ClientManagement/data_create.csv'
SYSADMIN_COMPANY_UPDATE_DATA_FILE = ROOT_PATH + '/test_thermal/test_SuperAdmin/test_ClientManagement/data_update.csv'
SYSADMIN_COMPANY_DELETE_DATA_FILE = ROOT_PATH + '/test_thermal/test_SuperAdmin/test_ClientManagement/data_delete.csv'
SYSADMIN_COMPANY_READ_DATA_FILE = ROOT_PATH + '/test_thermal/test_SuperAdmin/test_ClientManagement/data_read.csv'
SYSADMIN_COMPANY_LOGIN_DATA_FILE = ROOT_PATH + '/test_thermal/test_SuperAdmin/test_ClientManagement/data_login.csv'

COMPANYADMIN_SITE_CREATE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_SiteManagement/data_create.csv'
COMPANYADMIN_SITE_READ_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_SiteManagement/data_read.csv'
COMPANYADMIN_SITE_DELETE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_SiteManagement/data_delete.csv'

COMPANYADMIN_USER_READ_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_UserManagement/data_read.csv'
COMPANYADMIN_USER_CREATE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_UserManagement/data_create.csv'
COMPANYADMIN_USER_DELETE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_UserManagement/data_delete.csv'

COMPANYADMIN_ROLE_READ_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_RoleManagement/data_read.csv'
COMPANYADMIN_ROLE_CREATE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_RoleManagement/data_create.csv'
COMPANYADMIN_ROLE_DELETE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_RoleManagement/data_delete.csv'
COMPANYADMIN_ROLE_UPDATE_DATA_FILE = ROOT_PATH + '/test_thermal/test_CompanyAdmin/test_RoleManagement/data_update.csv'

DASHBOARD_READ_DATA_FILE = ROOT_PATH + '/test_thermal/test_Dashboard/data_read.csv'
EBTREPORT_READ_DATA_FILE = ROOT_PATH + '/test_thermal/test_Reporting/data_read.csv'

HOME_URL = 'http://xxxxxxxxxxx'
print("HOME_URL: " + HOME_URL)

SYSADMIN_ACCOUNT = 'xxxxxxxx'
SYSADMIN_PASSWORD = 'xxxxxxxx'
COMPANYADMIN_ACCOUNT = 'xxxxxxxxx'

APPLICATION_USER_ACCOUNT = 'xxxx'
WINDOW_WIDTH = 1920
WINDOW_HEIGH = 977

AUTHORITY_COLUMNS = ["email", "password", "status", "company", "site", "role"]
AUTHORITY_SINGLE_VALUE_COLUMNS = ["email", "password", "status"]
AUTHORITY_LIST_VALUE_COLUMNS = ["company"]
AUTHORITY_KEY_LIST_VALUE_COLUMNS = ["site", "role"]

ENTITY_COLUMNS = ["company", "status", "site", "camera", "controller"]
ENTITY_SINGLE_VALUE_COLUMNS = ["company", "status"]
ENTITY_LIST_VALUE_COLUMNS = ["site"]
ENTITY_KEY_LIST_VALUE_COLUMNS = ["camera", "controller"]

ROLE_COLUMNS = ["company", "custome_role", "service"]
ROLE_SINGLE_VALUE_COLUMNS = ["company"]
ROLE_LIST_VALUE_COLUMNS = ["custome_role"]
ROLE_KEY_LIST_VALUE_COLUMNS = ["service"]

SITE_ANY_SITE = 'Any'

ROLE_COMPANY_ADMIN = 'Company Admin'
ROLE_SITE_ADMIN = 'Site Admin'
ROLE_SITE_OPERATOR = 'Site Operator'
ROLE_APPLICATION_USER = 'Application User'

SERVICE_ALERT_MANAGE = 'Alert Manage'
SERVICE_USER_MANAGE = 'User Manage'
SERVICE_SITE_MANAGE = 'Site Manage'
SERVICE_ROLE_MANAGE = 'Role Manage'
SERVICE_DASHBOARD_VIEW = 'Dashboard View'
SERVICE_EVENT_REVIEW = 'Event Review'
SERVICE_REPORT_VIEW = 'Report View'
SERVICE_RESOURCE_MANAGE = 'Resource Manage'

STATUS_ENABLED = "Enabled"
STATUS_DISABLED = "Disabled"

# CNB: Company Number Base
CNB = 8
# SNB: Site Number Base
SNB = 9

# TNB: Test Number Base
SYSADMIN_COMPANY_LOGIN_TNB = 100
SYSADMIN_COMPANY_CREATE_TNB = 200
SYSADMIN_COMPANY_READ_TNB = 300
SYSADMIN_COMPANY_UPDATE_TNB = 400
SYSADMIN_COMPANY_DELETE_TNB = 500

COMPANYADMIN_SITE_CREATE_TNB = 1100
COMPANYADMIN_SITE_READ_TNB = 1200
COMPANYADMIN_SITE_DELETE_TNB = 1300

COMPANYADMIN_USER_READ_TNB = 2100
COMPANYADMIN_USER_CREATE_TNB = 2200
COMPANYADMIN_USER_DELETE_TNB = 2400

COMPANYADMIN_ROLE_READ_TNB = 3100
COMPANYADMIN_ROLE_CREATE_TNB = 3200
COMPANYADMIN_ROLE_UPDATE_TNB = 3300
COMPANYADMIN_ROLE_DELETE_TNB = 3400

DASHBOARD_READ_TNB = 11100
EBTREPORT_READ_TNB = 11200

DEMO_CREDENTIAL = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
