def validate_banner(page, expected_url):

    banner = page.locator("div.fdq-hero-img img").get_attribute("src")

    if expected_url not in banner:
        raise AssertionError(f"Image mismatch: {banner}")