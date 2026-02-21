from OMS.pages.POS.base_pos import BasePOS
from OMS.pages.POS.create_preset_Earring import CreatePresetEarringOrderPOS
from OMS.pages.POS.create_preset_pendant import CreatePresetPendantOrderPOS
from OMS.pages.POS.create_preset_ring import CreatePresetRingOrderPOS
from OMS.pages.login_page import LoginPage
from OMS.utils.json_reader import get_login_user


class TestCreatePresetOrder:

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

    # Test CYO Ring
    def test_create_preset_ring(self, page):

        self._login_and_open_pos(page)

        order = CreatePresetRingOrderPOS(page)

        order.select_store_list()
        order.select_product_type()
        order.take_product_slug()
        order.search_product_slug()

    def test_create_preset_pendant(self, page):
        self._login_and_open_pos(page)

        order = CreatePresetPendantOrderPOS(page)

        order.select_store_list()
        order.select_product_type()
        order.take_product_slug()
        order.search_product_slug()

    def test_create_preset_earring(self, page):
        self._login_and_open_pos(page)

        order = CreatePresetEarringOrderPOS(page)

        order.select_store_list()
        order.select_product_type()
        order.take_product_slug()
        order.search_product_slug()


