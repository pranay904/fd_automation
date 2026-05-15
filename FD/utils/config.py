import os
from pathlib import Path

# BASE SITE URLS

BASE_URL = "https://ap-diam.com/"

REGISTER_URL = "https://ap-diam.com/register"
LOGIN_URL = "https://friendlydiamonds.com/login"

CYO_R_URL = "https://friendlydiamonds.com/ring-settings"  # CYO Ring Settings URL
DIAMOND_SETTING_URL = "https://friendlydiamonds.com/loose-diamonds?cyo=ring"  # Diamond Setting URL



# MODULE URLS

PRESET_URL = "https://friendlydiamonds.com/preset-engagement-rings"
PAYMENT_URL = "https://friendlydiamonds.com/"

CYO_R_URL = "https://friendlydiamonds.com/ring-settings"

CONTACT_US_URL = "https://friendlydiamonds.com/contact-us"

BESPOKE_JEWELRY_URL = "https://friendlydiamonds.com/customized-jewelry"


FCI_quiz= "https://friendlydiamonds.com/fci/engagement-ring-quiz"




# TEST DATA PATHS

file_path = Path("FD/test_data/media/images.jpg").resolve()

DATA_DIR = os.path.join("test_data")  # <-- updated folder name
PRESET_FILTER_EXCEL = os.path.join(DATA_DIR, "preset_filter_testcases.xlsx")
