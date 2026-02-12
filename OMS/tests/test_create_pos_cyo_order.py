import pytest

from OMS.pages.POS.base_pos import BasePOS
from OMS.pages.POS.create_cyo_order_pos import CreateCYOOrderPOS
from OMS.pages.login_page import LoginPage
from OMS.utils.json_reader import get_login_user


class TestCreateCYOOrder:

    def test_create_cyo_order(self, page):
        """
        Test Steps:
        1. Login
        2. Open POS
        3. Select Store
        4. Select Product Type
        5. Search Setting SKU
        6. Search Diamond SKU
        """

        # ---------- Login ----------
        login_page = LoginPage(page)
        login_page.open_login_page()

        login_data = get_login_user()
        login_page.login(login_data["email"], login_data["password"])

        # ---------- Open POS ----------
        base_pos = BasePOS(page)
        base_pos.open_pos()

        # ---------- Create Order ----------
        order = CreateCYOOrderPOS(page)

        # Step 1: Select Store
        order.select_store_list()

        # Step 2: Select Product Type
        order.select_product_type()

        # Step 3: Search Setting SKU
        order.search_setting_sku()

        order.select_ring_size()

        # Step 4: Search Diamond SKU
        order.search_diamond_sku()

        # Optional assertion (update based on your UI)
        # assert page.locator("text=Add to Cart").is_visible()
