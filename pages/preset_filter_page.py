from componats.fillter_all import CommonFilters
from utils.config import PRESET_URL

class PresetPage(CommonFilters):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def open(self):
        self.page.goto(PRESET_URL)

    # Individual filter methods
    def select_metal_filter(self, metal):
        selected = self.select_filter(self.METAL_DROPDOWN, self.METAL_ITEMS, metal)
        self.assert_filter_tag_applied(selected)
        self.assert_plp_matches_filter("metal", selected)
        return selected

    def select_shape_filter(self, shape):
        selected = self.select_filter(self.SHAPE_DROPDOWN, self.SHAPE_ITEMS, shape)
        self.assert_filter_tag_applied(selected)
        self.assert_plp_matches_filter("shape", selected)
        return selected

    def select_style_filter(self, style):
        selected = self.select_filter(self.STYLE_DROPDOWN, self.STYLE_ITEMS, style)
        self.assert_filter_tag_applied(selected)
        self.assert_plp_matches_filter("style", selected)
        return selected

    def select_carat_filter(self, carat):
        selected = self.select_filter(self.CARAT_DROPDOWN, self.CARAT_ITEMS, carat)
        self.assert_filter_tag_applied(selected)
        self.assert_plp_matches_filter("carat", selected)
        return selected

    # Helper to apply multiple filters at once
    def apply_filters(self, filters: dict):
        """
        Apply multiple filters at once.
        Returns dict of selected filters.
        """
        selected_filters = {}
        for filter_type, value in filters.items():
            select_func = getattr(self, f"select_{filter_type}_filter")
            selected_filters[filter_type] = select_func(value)
        return selected_filters
