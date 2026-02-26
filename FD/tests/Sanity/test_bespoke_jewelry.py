import time

from FD.pages.bespoke_jewlery import Bespoke_Jewlery
from FD.utils.yaml_loader import load_yaml
from FD.test_data import media

def test_bespoke_form(page):

    # Load credentials and test data
    creds = load_yaml("config/credentials.yaml")["default_user"]
    data = load_yaml("test_data/form_data.yaml")["contact_us"]

    #open the form
    bespoke = Bespoke_Jewlery(page)
    bespoke.open_bespoke_jewlery()

    #fill the form
    bespoke.fill_name_jewelry(creds["name"])
    time.sleep(1)
    bespoke.fill_email_jewelry(creds["email"])
    bespoke.fill_phone(creds["phone"])

    # select jewelry & budget
    bespoke.select_jewelry_type()
    bespoke.select_budget_type()

    bespoke.fill_message(data["message"])

    # Optional file upload
    bespoke.upload_file(
        ".upload-btn",                  # Button that reveals the file input (your button selector)
        "(//input[@type='file'])[1]",    # File input selector (adjust if needed)
        "C:/Users/DELL/Documents/Image/images (1).jpg" # Path to the media file you want to upload
    )
    time.sleep(2)

    bespoke.submit_form()

    time.sleep(2)









