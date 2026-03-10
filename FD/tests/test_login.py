from FD.pages.login.login_page import LoginPage


def test_login_user_Used_Credentails(page):
    login= LoginPage(page)
    login.open_login_page()
    #login.close_popup_if_present()

    login.login_user()




