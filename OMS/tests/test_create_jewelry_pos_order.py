from OMS.pages import login_page
from OMS.pages.POS.base_pos import BasePOS

from OMS.pages.POS.create_jewelry import CreateJewelryOrderPOS
from OMS.pages.login_page import LoginPage
from OMS.utils.json_reader import get_login_user


class TestCreateJewelryOrder:

    @staticmethod
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

    def test_create_jewelry_ring(self, page):

        self._login_and_open_pos(page)

        order = CreateJewelryOrderPOS(page)

        order.select_store_list()
        order.select_product_type()

        order.search_jewelry_sku()

        order.select_ring_size()







