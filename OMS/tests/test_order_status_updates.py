import time

import pytest

from OMS.pages.login_page import LoginPage
from OMS.pages.order_status_update.CancelledRefundedStatus import CancelledRefundedStatus
from OMS.pages.order_status_update.ReturnAndRefundedStatus import ReturnAndRefundedStatus
from OMS.pages.order_status_update.ReturnRequestedStatus import ReturnRequestedStatus
from OMS.pages.order_status_update.ReturnStatus import ReturnStatus
from OMS.pages.order_status_update.cancelled_status import CancelledStatus
from OMS.pages.order_status_update.delivered_status import DeliveredStatus
from OMS.pages.order_status_update.edit_product import EditProduct
from OMS.pages.order_status_update.order_line_update import AddDiamondLines
from OMS.pages.order_status_update.orderstatusbase import OrderStatusBase
from OMS.pages.order_status_update.shipped_status import ShippedStatus
from OMS.utils.json_reader import get_login_user


# -------------------------------
# Generic login function
# -------------------------------
def login(page):

    # If already on dashboard, skip login
    if "frontendoms.ap-diam.com" in page.url and "login" not in page.url:
        print("Already logged in — skipping login")
        return

    login_page = LoginPage(page)
    login_page.open_login_page()

    login_data = get_login_user()
    login_page.login(login_data["email"], login_data["password"])

    # Wait until dashboard loads properly
    page.wait_for_load_state("networkidle")



# -------------------------------
# Base order navigation

def open_order_status_update(page):
    order_status = OrderStatusBase(page)
    order_status.open_order_and_all_order_line()
    order_status.click_on_order_status_update()
    return order_status

# Test: Cancelled status

def test_cancelled_status(page):
    login(page)
    open_order_status_update(page)
    status = CancelledStatus(page)
    status.select()

# Test: Shipped status


def test_shipped_status(page):
    login(page)
    open_order_status_update(page)
    status = ShippedStatus(page)
    status.select()


# Test: Returned & Refunded status

def test_cancelled_and_Refunded_status(page):
    login(page)
    open_order_status_update(page)
    status = CancelledRefundedStatus(page)
    status.select()


def test_delivered_satus(page):
    login(page)
    open_order_status_update(page)
    status = DeliveredStatus(page)
    status.select()


# Test: ReturnAndRefundedStatus

def test_return_and_refunded_status(page):
    login(page)
    open_order_status_update(page)
    status = ReturnAndRefundedStatus(page)
    status.select()


# Test: Return Requested Status

def test_return_requested_status(page):
    login(page)
    open_order_status_update(page)
    status = ReturnRequestedStatus(page)
    status.select()

# -------------------------------
# Test: Delivered status
# -------------------------------
def test_return_staus(page):
    login(page)
    open_order_status_update(page)
    status = ReturnStatus(page)
    status.select()


def test_add_diamond_line(page):

    login(page)
    time.sleep(1)

    update = AddDiamondLines(page)
    update.open_all_order_line()

    update.add_diamond_line()



def test_update_product_size(page):

    login(page)

    edit_product = EditProduct(page)
    edit_product.open_all_order_line()
    time.sleep(2)
    edit_product.preset_product()
    time.sleep(2)
    edit_product.edit_product_form()
    edit_product.update_size()
    edit_product.handle_size_modal()


def test_update_mount_and_other_details(page):

    login(page)

    edit_product = EditProduct(page)
    edit_product.open_all_order_line()
    time.sleep(3)
    edit_product.preset_product()
    time.sleep(2)
    edit_product.edit_product_form()
    edit_product.update_mount()
    edit_product.update_product_details()



def test_add_product_note(page):

    login(page)
    edit_product = EditProduct(page)
    edit_product.open_all_order_line()
    time.sleep(2)
    edit_product.preset_product()
    time.sleep(2)

    edit_product.add_product_note()


def test_update_product_status(page):

    login(page)
    edit_product = EditProduct(page)
    edit_product.open_all_order_line()
    time.sleep(2)
    edit_product.preset_product()
    time.sleep(2)
    edit_product.edit_product_status()













