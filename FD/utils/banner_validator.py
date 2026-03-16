# FD/utils/banner_validator.py

import json
import os
from playwright.sync_api import expect

class BannerValidator:
    def __init__(self):
        # Load expected banner images from JSON
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(base_path, "..", "test_data", "banner_images.json")
        with open(json_file) as f:
            self.images = json.load(f)

    # For clickable questions (Q1-Q4)
    def validate(self, page, question, option, timeout=20000):
        expected_url = self.images[f"Q{question}"][str(option)]
        # Convert relative URLs to full URLs if needed
        if expected_url.startswith("/"):
            expected_url = "https://cl.ap-diam.com" + expected_url

        banner_locator = page.locator("div.fdq-img-grid img")
        expect(banner_locator).to_be_visible(timeout=timeout)

        actual_src = banner_locator.get_attribute("src")
        if actual_src.startswith("/"):
            actual_src = "https://cl.ap-diam.com" + actual_src

        assert expected_url == actual_src, (
            f"Banner mismatch Q{question} Option {option} "
            f"\nExpected: {expected_url} \nActual: {actual_src}"
        )

    # For slider questions (Q5-Q6)
    def validate_slider_banner(self, page, question, option, timeout=20000):
        expected_url = self.images[f"Q{question}"][str(option)]
        if expected_url.startswith("/"):
            expected_url = "https://cl.ap-diam.com" + expected_url

        # Correct locator for slider images (PNG)
        slider_img = page.locator("(//img[@class='vis fdq-slider-img'])[1]")
        expect(slider_img).to_be_visible(timeout=timeout)

        actual_src = slider_img.get_attribute("src")
        if actual_src.startswith("/"):
            actual_src = "https://cl.ap-diam.com" + actual_src

        assert expected_url == actual_src, (
            f"Slider banner mismatch Q{question} Option {option} "
            f"\nExpected: {expected_url} \nActual: {actual_src}"
        )