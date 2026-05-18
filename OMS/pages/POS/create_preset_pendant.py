from OMS.pages.POS.base_pos import BasePOS


class CreatePresetPendantOrderPOS:
    def __init__(self, page):
        self.page = page
        self.base_pos = BasePOS(page)
        self.slug = None
        self.global_delay = 1500  # 1.5 seconds

    # Utility Methods

    def wait_delay(self, page=None):
        if page:
            page.wait_for_timeout(self.global_delay)
        else:
            self.page.wait_for_timeout(self.global_delay)

    def highlight(self, locator):
        locator.evaluate("""
            element => {
                element.style.border = '3px solid red';
                element.style.transition = '0.3s';
            }
        """)
        self.wait_delay()

    def click_with_effect(self, locator, page=None):
        locator.wait_for(state="visible")
        self.highlight(locator)
        locator.click()
        self.wait_delay(page)

    # NEW: Highlight + Fill (so search box also highlights)
    def fill_with_effect(self, locator, value, page=None):
        locator.wait_for(state="visible")
        self.highlight(locator)
        locator.fill(value)
        self.wait_delay(page)

    # Main Methods

    def select_store_list(self):
        stores = self.base_pos.store_list()
        store = stores["Ny_store"]
        self.click_with_effect(store)

    def select_product_type(self):
        product_type = self.base_pos.product_type()
        self.click_with_effect(product_type["Preset"])
        self.click_with_effect(product_type["Cyo_Pendant"])

    def take_product_slug(self):

        # Step 1: Open new tab
        with self.page.context.expect_page() as new_page_info:
            preset_page = self.page.locator(
                "//div[@class='v-row w-100 justify-start mb-4']//div[2]//button[2]"
            )
            self.click_with_effect(preset_page)

        preset_tab = new_page_info.value
        preset_tab.wait_for_load_state("domcontentloaded")
        self.wait_delay(preset_tab)

        # Step 2: Click product
        product = preset_tab.locator("(//div[@class='product_box'])[2]").first
        self.click_with_effect(product, preset_tab)
        preset_tab.wait_for_load_state("domcontentloaded")

        # Step 3: Highlight whole page before copying slug
        preset_tab.evaluate("""
            document.body.style.border = '5px solid blue';
        """)
        self.wait_delay(preset_tab)

        # Step 4: Capture slug
        full_url = preset_tab.url
        print("Full URL:", full_url)

        self.slug = full_url.split("/")[-1]
        print("Captured Slug:", self.slug)

        # Step 5: Close tab and return
        preset_tab.close()
        self.page.bring_to_front()
        self.wait_delay()

    def search_product_slug(self):
        search_slug = self.page.get_by_role("textbox", name="Search Slug")

        # Highlight + Fill
        self.fill_with_effect(search_slug, self.slug)

        # FIX: specify which Submit button
        submit = self.page.locator("button[class='v-btn v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-x-large v-btn--variant-flat']")
        self.click_with_effect(submit)
        self.wait_delay()
