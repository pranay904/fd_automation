import time

import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage

import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from playwright.sync_api import expect


@pytest.mark.order(1)
def test_register_user(page):
    register = RegisterPage(page)

    # Proceed with registration
    register.open_register_page()
    register.close_popup_if_present()
    email = register.register_user()
    register.logout_user()

@pytest.mark.order(2)
def test_logoutUser(page):
    logout= RegisterPage(page)

    logout.logout_user()

@pytest.mark.order(3)
def test_login_user(page):
    login = RegisterPage(page)
    login.open_login_page()
   #login.close_popup_if_present()
    login.login_user()




