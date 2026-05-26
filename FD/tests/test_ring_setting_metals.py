import pytest

from FD.pages.metal_swatch_verify_on_pdp.ring_setting_page import (
    RingSettingPage
)


@pytest.mark.regression
class TestRingSettingMetals:

    def test_verify_all_products_all_metals(self, page):

        ring_page = RingSettingPage(page)

        failed = (
            ring_page.verify_all_products_metals()
        )

        assert not failed, (
            f"\nTOTAL FAILURES: {len(failed)}"
            f"\nFAIL DETAILS: {failed}"
        )