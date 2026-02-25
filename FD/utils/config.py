import os

# =========================================================
# BASE SITE URLS
# =========================================================
BASE_URL = "https://payment.ap-diam.com/"

REGISTER_URL = "https://payment.ap-diam.com/register"
LOGIN_URL = "https://payment.ap-diam.com/login"

CYO_R_URL = "https://payment.ap-diam.com/ring-settings"  # CYO Ring Settings URL
DIAMOND_SETTING_URL = "https://payment.ap-diam.com/loose-diamonds?cyo=ring"  # Diamond Setting URL


# =========================================================
# MODULE URLS
# =========================================================
PRESET_URL = "https://friendlydiamonds.com/preset-engagement-rings"
PAYMENT_URL = "https://payment.ap-diam.com/"

CYO_R_URL = "https://friendlydiamonds.com/ring-settings"

CONTACT_US_URL = "https://friendlydiamonds.com/contact-us"

BESPOKE_JEWELRY_URL = "https://friendlydiamonds.com/customized-jewelry"



# =========================================================
# TEST DATA PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Test data directory inside FD
DATA_DIR = os.path.join(BASE_DIR, "test_data")

# Excel file path
PRESET_FILTER_EXCEL = os.path.join(DATA_DIR, "preset_filter_testcases.xlsx")
