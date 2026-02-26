from FD.utils.yaml_loader import load_yaml

from FD.pages.forms.Gemologist_page import Gemologist

def test_gemologist(page):

    creds = load_yaml("config/credentials.yaml")["default_user"]
    data = load_yaml("test_data/form_data.yaml")["gemologist"]

    gemo = Gemologist(page)

    gemo.naviagate_to_gemo()

    # fill the details

    gemo.fill_name(creds["name"])
    gemo.fill_email(creds["email"])

    gemo.fill_message(creds["message"])

    gemo.submit_gemo_drop_hint_form()


