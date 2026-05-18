import pytest
from FD.pages.all_preset_page import PresetPage
from FD.utils.excel_reader import read_excel
from FD.utils.config import PRESET_FILTER_EXCEL

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


