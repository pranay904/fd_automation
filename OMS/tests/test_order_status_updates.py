import pytest

from OMS.pages.login_page import LoginPage
from OMS.pages.order_status_update.CancelledRefundedStatus import CancelledRefundedStatus
from OMS.pages.order_status_update.ReturnAndRefundedStatus import ReturnAndRefundedStatus
from OMS.pages.order_status_update.ReturnRequestedStatus import ReturnRequestedStatus
from OMS.pages.order_status_update.ReturnStatus import ReturnStatus
from OMS.pages.order_status_update.cancelled_status import CancelledStatus
from OMS.pages.order_status_update.delivered_status import DeliveredStatus
from OMS.pages.order_status_update.orderstatusbase import OrderStatusBase
from OMS.pages.order_status_update.shipped_status import ShippedStatus
from OMS.utils.json_reader import get_login_user


# -------------------------------
# Generic login function
# -------------------------------
def login(page):
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_data = get_login_user()
    login_page.login(login_data["email"], login_data["password"])

# -------------------------------
# Base order navigation

def open_order_status_update(page):
    order_status = OrderStatusBase(page)
    order_status.open_order_and_all_order_line()
    order_status.click_on_order_status_update()
    return order_status

# -------------------------------
# Test: Cancelled status
# -------------------------------
def test_cancelled_status(page):
    login(page)
    open_order_status_update(page)
    status = CancelledStatus(page)
    status.select()

# -------------------------------
# Test: Shipped status
# -------------------------------
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
