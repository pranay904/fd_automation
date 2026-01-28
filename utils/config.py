import os

# =========================================================
# BASE SITE URLS
# =========================================================
BASE_URL = "https://frontendtwo.ap-diam.com/"

REGISTER_URL = "https://frontendtwo.ap-diam.com/register"
LOGIN_URL = "https://frontendtwo.ap-diam.com/login"

# =========================================================
# MODULE URLS
# =========================================================
PRESET_URL = "https://friendlydiamonds.com/preset-engagement-rings"
PAYMENT_URL = "https://payment.ap-diam.com/"

# =========================================================
# TEST DATA PATHS
# =========================================================
DATA_DIR = os.path.join("test_data")  # <-- updated folder name
PRESET_FILTER_EXCEL = os.path.join(DATA_DIR, "preset_filter_testcases.xlsx")
