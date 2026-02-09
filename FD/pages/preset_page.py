import re

from utils.config import PRESET_URL
from test_data.expected_filters import FILTER_CONFIG


class Preset:

    def __init__(self, page):
        self.page = page

    # ------------------ Open Page ------------------

    def open_preset_url(self):
        self.page.goto(PRESET_URL)

    # ------------------ Open Metal Dropdown ------------------

    def open_metal_filter(self):
        self.page.locator("//div[contains(text(),'metal')]").click()

    # ------------------ Normalize Text ------------------

    def _normalize_metal_text(self, text: str) -> str:
        return re.sub(r"(14K|18K|PT)$", "", text).strip()

    # ------------------ Verify Metal Options ------------------

    def verify_metal_options(self):
        metal_items = self.page.locator(
            "//div[@class='drop_item_metal drop_item']//ul[@class='mb-0']/li"
        )

        metal_items.first.wait_for(state="visible")

        ui_texts = metal_items.all_text_contents()
        normalized_ui = [self._normalize_metal_text(t) for t in ui_texts]

        print("\nMetal options in filter:")
        for text in normalized_ui:
            print(text)

        for _, expected_metals in FILTER_CONFIG["Metal"].items():
            for expected in expected_metals:
                if expected not in normalized_ui:
                    raise AssertionError(
                        f"Expected metal '{expected}' not found in filter"
                    )

        print("All metal options verified")

    # ------------------ Click One Metal ------------------

    def click_first_metal(self):
        metal_items = self.page.locator(
            "//div[@class='drop_item_metal drop_item']//ul[@class='mb-0']/li"
        )

        metal_items.first.wait_for(state="visible")
        selected_text = metal_items.first.text_content()
        metal_items.first.click()

        selected_metal = self._normalize_metal_text(selected_text)

        print(f"Selected metal: {selected_metal}")
        return selected_metal

    # ------------------ Verify Applied Filter ------------------

    def verify_applied_filter(self, selected_metal):
        filter_tag = self.page.locator(
            "(//div[@class='filter_tags for_desktop'])[1]"
        )
        filter_tag.wait_for(state="visible")

        filter_texts = filter_tag.all_text_contents()
        normalized_filters = [
            self._normalize_metal_text(text)
            for text in filter_texts
        ]

        print("\nApplied filter tags:")
        for text in normalized_filters:
            print(text)

        if selected_metal not in normalized_filters:
            raise AssertionError(
                f"Applied filter '{selected_metal}' not shown in filter tags"
            )

        print("Applied filter verified")

    # ------------------ Verify PLP Swatches ------------------

    def verify_plp_swatches(self, selected_metal):
        # Map metal names to class names in HTML
        metal_map = {
            "14Kt White Gold": "white",
            "14Kt Yellow Gold": "yellow",
            "14Kt Rose Gold": "rose",
            "18Kt White Gold": "white",
            "18Kt Yellow Gold": "yellow",
            "18Kt Rose Gold": "rose",
            "Platinum": "platinum"
        }

        expected_class = metal_map[selected_metal]

        # Wait for first product to load
        self.page.locator("//div[@name='prod_box_animation']").first.wait_for(state="visible")

        # Get all swatches for the first product
        swatches = self.page.locator(
            "//div[@name='prod_box_animation']//div[contains(@class,'metal_color')]/div[contains(@class,'metal_box')]"
        )

        # Loop through swatches and check if expected class is part of the class attribute
        found = False
        for i in range(swatches.count()):
            classes = swatches.nth(i).get_attribute("class")  # e.g., "metal_box white active"
            if expected_class in classes:  # <-- partial match
                found = True
                break

        if not found:
            raise AssertionError(f"PLP does not show swatch for '{selected_metal}'")

        print(" PLP swatch matches selected metal")

# def verify_plp_swatches(self, selected_metal):
#     metal_map = {
#         "14Kt White Gold": "White",
#         "14Kt Yellow Gold": "Yellow",
#         "14Kt Rose Gold": "Rose",
#         "18Kt White Gold": "White",
#         "18Kt Yellow Gold": "Yellow",
#         "18Kt Rose Gold": "Rose",
#         "Platinum": "Platinum"
#     }
#
#     expected_text = metal_map[selected_metal]
#
#     # Wait for product to load
#     self.page.locator("//div[@name='prod_box_animation']").first.wait_for(state="visible")
#
#     swatches = self.page.locator(
#         "//div[@name='prod_box_animation']//div[contains(@class,'metal_color')]/div[contains(@class,'metal_box')]"
#     )
#
#     found = False
#     for i in range(swatches.count()):
#         swatch_text = swatches.nth(i).text_content()  # <-- use text_content instead of get_attribute
#         if swatch_text.strip() == expected_text:
#             found = True
#             break
#
#     if not found:
#         raise AssertionError(f"PLP does not show swatch for '{selected_metal}'")
#
#     print(" PLP swatch matches selected metal")

