import pytest
from pages.contact_us_page import ContactUsPage
from utils.yaml_loader import load_yaml

 # optional if using playwright fixtures
def test_contact_us_form(page):

    # Load credentials and test data
    creds = load_yaml("config/credentials.yaml")["default_user"]
    data = load_yaml("test_data/form_data.yaml")["contact_us"]

    # Open Contact Us page
    contact = ContactUsPage(page)
    contact.open_contact_us()

    # Fill form
    contact.fill_name(creds["name"])
    contact.fill_email(creds["email"])
    contact.fill_phone(creds["phone"])
    contact.fill_message(data["message"])

    # Optional file upload
    # contact.upload_file("input[type='file']", "data/media/ring.jpg")

    # Submit
    contact.submit_form()
