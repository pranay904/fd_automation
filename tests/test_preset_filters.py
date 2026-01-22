import pytest
from pages.preset_filter_page import PresetPage
from test_data import preset_filter_data

# Example: smaller subset for fast test
TEST_CASES = [
    ("14Kt White Gold", "Round", "Solitaire", "1/2 Ct."),
    ("14Kt Yellow Gold", "Oval", "Halo", "1 Ct."),
    ("18Kt White Gold", "Princess", "Hidden Halo", "2 Ct."),
]

@pytest.mark.parametrize("metal,shape,style,carat", TEST_CASES)
def test_preset_filters(page, metal, shape, style, carat):
    preset = PresetPage(page)
    preset.open()
    preset.apply_and_verify_filters(metal, shape, style, carat)
