# import pytest
# from pages.preset_filter_page import PresetPage
# from test_data import preset_filter_data
#
# # Example: smaller subset for fast test
# TEST_CASES = [
#     ("14Kt White Gold", "Round", "Solitaire", "1/2 Ct."),
#     ("14Kt Yellow Gold", "Oval", "Halo", "1 Ct."),
#     ("18Kt White Gold", "Princess", "Hidden Halo", "2 Ct."),
# ]
#
# @pytest.mark.parametrize("metal,shape,style,carat", TEST_CASES)
# def test_preset_filters(page, metal, shape, style, carat):
#     preset = PresetPage(page)
#     preset.open()
#     preset.apply_and_verify_filters(metal, shape, style, carat)



# tests/test_preset_filters.py
import pytest
from pages.all_preset_page import PresetPage
from utils.excel_reader import read_excel
from utils.config import PRESET_FILTER_EXCEL

# Read test data from Excel
TEST_DATA = read_excel(PRESET_FILTER_EXCEL, "PresetFilters")

@pytest.mark.parametrize("data", TEST_DATA)
def test_preset_filters(page, data):
    preset = PresetPage(page)
    preset.open()

    filter_type = data.get("TestType")

    # filter values (lowercase keys)
    filter_values = {
        k.lower(): v
        for k, v in data.items()
        if k.lower() in ["metal", "shape", "style", "carat"] and v
    }

    if not filter_values:
        print(f"Skipping {data.get('TC_ID')} – no filter values")
        return

    print(f"\n🔹 Executing {data.get('TC_ID')} - {filter_type}")

    if filter_type.lower() == "mix":
        preset.apply_verify_mixed_filters(filter_values)
    else:
        # single filter can be any one of metal/shape/style/carat
        for k, v in filter_values.items():
            preset.apply_verify_single_filter(k, v)




