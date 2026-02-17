import pytest

from OMS.pages.POS.base_pos import BasePOS
from OMS.pages.POS.create_cyo_ring import CreateCYOOrderPOS
from OMS.pages.POS.create_cyo_pendant import CreateCYOPendantOrderPOS
from OMS.pages.POS.create_cyo_earring import CreateCYOEarringOrderPOS
from OMS.pages.POS.create_diamond import CreateDiamondOrderPOS
from OMS.pages.login_page import LoginPage
from OMS.utils.json_reader import get_login_user


class TestCreateCYOOrder:

    # -----
    # Common Login + POS Open

    def _login_and_open_pos(self, page):

        login_page = LoginPage(page)

        # Check if already logged in (Dashboard visible)
        try:
            if page.locator("text=Dashboard").is_visible(timeout=3000):
                print("Already logged in - skipping login")
            else:
                raise Exception
        except:
            login_page.open_login_page()
            login_data = get_login_user()
            login_page.login(login_data["email"], login_data["password"])

        base_pos = BasePOS(page)
        base_pos.open_pos()

    # ---------------------------------------------------------
    # Test CYO Ring
    # ---------------------------------------------------------
    def test_create_cyo_ring(self, page):

        self._login_and_open_pos(page)

        order = CreateCYOOrderPOS(page)

        order.select_store_list()
        order.select_product_type()
        order.search_setting_sku()
        order.select_ring_size()
        order.search_diamond_sku()

    # ---------------------------------------------------------
    #  Test CYO Pendant
    # ---------------------------------------------------------
    def test_create_cyo_pendant(self, page):

        self._login_and_open_pos(page)

        order = CreateCYOPendantOrderPOS(page)

        order.select_store_list()
        order.select_product_type()
        order.search_setting_sku()
        order.select_chain_length()
        order.search_diamond_sku()

    # ---------------------------------------------------------
    # Test CYO Earring
    # ---------------------------------------------------------
    def test_create_cyo_earring(self, page):

        self._login_and_open_pos(page)

        order = CreateCYOEarringOrderPOS(page)

        order.select_store_list()
        order.select_product_type()
        order.search_setting_sku()
        order.select_back_type()
        order.search_diamond_sku()

    def test_add_cart_diamond(self, page):

        self._login_and_open_pos(page)

        order= CreateDiamondOrderPOS(page)

        order.select_store_list()
        order.select_product_type()

        order.search_diamond_sku()






# import pytest

#
# from OMS.pages.POS.base_pos import BasePOS
# from OMS.pages.POS.create_cyo_ring import CreateCYOOrderPOS
# from OMS.pages.login_page import LoginPage
# from OMS.utils.json_reader import get_login_user
#
#
# class TestCreateCYOOrder:
#
#     def test_create_cyo_order(self, page):
#         """
#         Test Steps:
#         1. Login
#         2. Open POS
#         3. Select Store
#         4. Select Product Type
#         5. Search Setting SKU
#         6. Search Diamond SKU
#         """
#
#         # ---------- Login ----------
#         login_page = LoginPage(page)
#         login_page.open_login_page()
#
#         login_data = get_login_user()
#         login_page.login(login_data["email"], login_data["password"])
#
#         # ---------- Open POS ----------
#         base_pos = BasePOS(page)
#         base_pos.open_pos()
#
#         # ---------- Create Order ----------
#         order = CreateCYOOrderPOS(page)
#
#         # Step 1: Select Store
#         order.select_store_list()
#
#         # Step 2: Select Product Type
#         order.select_product_type()
#
#         # Step 3: Search Setting SKU
#         order.search_setting_sku()
#
#         order.select_ring_size()
#
#         # Step 4: Search Diamond SKU
#         order.search_diamond_sku()
#
#         # Optional assertion (update based on your UI)
#         # assert page.locator("text=Add to Cart").is_visible()
