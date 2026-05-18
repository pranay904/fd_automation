import time

from FD.pages.forms.drop_a_hint_page import DropHint
from FD.utils.yaml_loader import load_yaml

def test_drop_hint(page):

    creds = load_yaml("config/credentials.yaml")["default_user"]
    data = load_yaml("test_data/form_data.yaml")["drop_hint"]

    #open the drop a hint

    drop_hint = DropHint(page)
    drop_hint.open_Base_url()

    # verify the drop a hint on pdp
    drop_hint.navigate_to_pdp()

    #  validate the form
    drop_hint.drop_hint_all_fields(
        name=creds["name"],
        email=creds["email"],
        partner_name=creds["partner_name"],
        partner_email=creds["partner_email"],
        message=data["product_name"]
    )

    time.sleep(10)

    drop_hint.submit_gemo_drop_hint_form()

    time.sleep(10)

    # drop_hint.fill_name(creds["name"])
    # drop_hint.fill_email(creds["email"])
    # drop_hint.fill_partner_name(creds["partner_name"])
    # drop_hint.fill_partner_email(creds["partner_email"])
    # drop_hint.fill_message(data["product_name"])
    #
    # drop_hint.submit_form()
    # time.sleep(3)
