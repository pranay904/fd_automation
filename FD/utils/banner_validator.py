import json
import os
from urllib.parse import urlparse
from playwright.sync_api import expect


def _path_only(url):
    """Strip domain — compare only the path portion of the URL."""
    if url.startswith("/"):
        return url
    return urlparse(url).path


class BannerValidator:
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(base_path, "..", "test_data", "banner_images.json")
        with open(json_file) as f:
            self.images = json.load(f)

    def validate(self, page, question, option, timeout=20000):
        expected_url = self.images[f"Q{question}"][str(option)]
        banner_locator = page.locator("div.fdq-img-grid img")
        expect(banner_locator).to_be_visible(timeout=timeout)
        actual_src = banner_locator.get_attribute("src")

        expected_path = _path_only(expected_url)
        actual_path = _path_only(actual_src)

        assert expected_path == actual_path, (
            f"Banner mismatch Q{question} Option {option}"
            f"\nExpected path: {expected_path}"
            f"\nActual path:   {actual_path}"
        )

    def validate_slider_banner(self, page, question, option, timeout=20000):
        expected_url = self.images[f"Q{question}"][str(option)]
        slider_img = page.locator("(//img[@class='vis fdq-slider-img'])[1]")
        expect(slider_img).to_be_visible(timeout=timeout)
        actual_src = slider_img.get_attribute("src")

        expected_path = _path_only(expected_url)
        actual_path = _path_only(actual_src)

        assert expected_path == actual_path, (
            f"Slider banner mismatch Q{question} Option {option}"
            f"\nExpected path: {expected_path}"
            f"\nActual path:   {actual_path}"
        )
