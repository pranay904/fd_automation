from FD.pages.preset_page import Preset


def test_preset_filter(page):
    preset = Preset(page)

    preset.open_preset_url()

    preset.open_metal_filter()
    preset.verify_metal_options()

    selected_metal = preset.click_first_metal()

    preset.verify_applied_filter(selected_metal)
    preset.verify_plp_swatches(selected_metal)

    
