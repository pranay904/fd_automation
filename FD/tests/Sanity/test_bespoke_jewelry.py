import time

from FD.pages.forms.bespoke_jewlery import Bespoke_Jewelery
from FD.utils.yaml_loader import load_yaml


def test_bespoke_form(page):

    # Load credentials and test data
    creds = load_yaml("config/credentials.yaml")["default_user"]
    data = load_yaml("test_data/form_data.yaml")["contact_us"]

    #open the form
    bespoke = Bespoke_Jewelery(page)
    bespoke.open_bespoke_jewelery()

    #fill the form
    bespoke.fill_name_jewelry(creds["name"])
    time.sleep(2)
    bespoke.fill_email(creds["form_email"])
    bespoke.fill_phone(creds["phone"])

    # select jewelry & budget
    bespoke.select_jewelry_type()
    bespoke.select_budget_type()

    bespoke.fill_message(data["message"])
    #
    #
    # # Upload file
    # bespoke.upload_file(
    #     ".upload-btn",
    #     "(//input[@type='file'])[1]",
    #     str(file_path)
    # )
    #
    #
    # # Optional: wait until file is actually attached (recommended)
    # page.locator("(//input[@type='file'])[1]").wait_for(state="attached")

    # Submit form
    bespoke.submit_form()
    time.sleep(10)













