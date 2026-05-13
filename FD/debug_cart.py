"""
Debug script — inspects the page after Add to Bag to find correct cart locators.
"""
import re
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.launch(headless=False, slow_mo=300)
page = browser.new_page()

# Go to the CYO setting PLP
print("Navigating to CYO Setting PLP...")
page.goto("https://friendlydiamonds.com/cyo-setting")
page.wait_for_load_state("domcontentloaded")
page.wait_for_timeout(3000)

# Click first product
first = page.locator("div.product_box, div.prod_box, div.product-card").first
print(f"First product visible: {first.is_visible()}")
first.click()
page.wait_for_timeout(3000)
print(f"Setting details URL: {page.url}")

# Select this setting
btn = page.locator("button:has-text('Select This Setting'), a:has-text('Select This Setting')").first
print(f"Select setting btn visible: {btn.is_visible()}")
btn.click()
page.wait_for_timeout(3000)
print(f"Diamond PLP URL: {page.url}")

# Click first diamond
diamond = page.locator("div.product_box, div.prod_box, div.diamond-card").first
diamond.click()
page.wait_for_timeout(3000)
print(f"Diamond details URL: {page.url}")

# Add diamond to ring
add_btn = page.locator("button:has-text('Add Diamond to Ring'), button:has-text('Complete Ring')").first
add_btn.click()
page.wait_for_timeout(5000)
print(f"Complete page URL: {page.url}")

# Select ring size
try:
    dropdown = page.locator("(//div[contains(@class,'current_active')])[1]")
    dropdown.click()
    page.wait_for_timeout(1000)
    options = page.locator("ul.p-0:visible li span")
    options.nth(1).click()
    page.wait_for_timeout(1000)
    print("Ring size selected")
except Exception as e:
    print(f"Ring size error: {e}")

# Add to bag
try:
    bag_btn = page.locator("div.sticky_btns span:has-text('Add to bag')").first
    bag_btn.click()
    page.wait_for_timeout(4000)
    print(f"After Add to Bag URL: {page.url}")
except Exception as e:
    print(f"Add to bag error: {e}")

# Now inspect what's on the page
print("\n--- Current URL ---")
print(page.url)

print("\n--- Checking cart-related selectors ---")
selectors = [
    "a[href*='cart']",
    "div.cart_icon",
    "div.cart-icon",
    "a.cart-icon",
    "span.cart_count",
    "div.cart_container",
    "div.cart-container",
    "div.cart_items",
    "div.cart_item",
    "div.bag_items",
    "div.bag_item",
    "div.mini_cart",
    "div.minicart",
    "div.cart_popup",
    "div.cart_sidebar",
    "div.cart_drawer",
    "button:has-text('Checkout')",
    "a:has-text('Checkout')",
    "button:has-text('View Cart')",
    "a:has-text('View Cart')",
    "div.order_summary",
    "div.cart_total",
    "span.total-price",
    "div.price_box",
]
for sel in selectors:
    try:
        loc = page.locator(sel)
        count = loc.count()
        visible = loc.first.is_visible() if count > 0 else False
        if count > 0:
            txt = loc.first.inner_text().strip()[:60] if visible else ""
            print(f"  FOUND  {sel}: count={count}, visible={visible}, text='{txt}'")
    except Exception as e:
        print(f"  ERROR  {sel}: {e}")

# Dump all classes containing 'cart' or 'bag'
print("\n--- Classes containing cart/bag ---")
body = page.content()
classes = re.findall(r'class="([^"]*(?:cart|bag|checkout)[^"]*)"', body, re.IGNORECASE)
unique = sorted(set(classes))
for c in unique[:30]:
    print(f"  {c}")

print("\n--- IDs containing cart/bag ---")
ids = re.findall(r'id="([^"]*(?:cart|bag|checkout)[^"]*)"', body, re.IGNORECASE)
for i in sorted(set(ids))[:20]:
    print(f"  #{i}")

page.wait_for_timeout(3000)
browser.close()
p.stop()
print("\nDone.")
