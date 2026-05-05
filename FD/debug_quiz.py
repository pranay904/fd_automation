"""
Debug script - runs quiz and dumps page state after clicking See My Rings
"""
import re
import sys
from playwright.sync_api import sync_playwright

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
page = browser.new_page()

print("Navigating to quiz...")
page.goto("https://friendlydiamonds.com/fci/engagement-ring-quiz")
page.wait_for_timeout(4000)
print(f"URL: {page.url}")

# Q1-Q4: click first option + continue
for q in range(1, 5):
    opts = page.locator("div.fdq-opts div.fdq-opt")
    opts.first.click()
    page.wait_for_timeout(800)
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(1500)
    print(f"Q{q} done")

# Q5: slider
slider = page.locator("input.fdq-slider-input").nth(0)
slider.evaluate("(el)=>el.value=1")
slider.dispatch_event("change")
page.wait_for_timeout(800)
page.get_by_role("button", name="Continue").click()
page.wait_for_timeout(1500)
print("Q5 done")

# Q6: slider
slider2 = page.locator("input.fdq-slider-input").nth(0)
slider2.evaluate("(el)=>el.value=1")
slider2.dispatch_event("change")
page.wait_for_timeout(800)

# Click See My Rings
btn = page.locator("button.fdq-next.fin")
print("Clicking See My Rings button...")
btn.click()
print("Clicked. Waiting 15s for results...")
page.wait_for_timeout(15000)

print(f"\nCurrent URL: {page.url}")

# Check selectors
print("\n--- Selector check ---")
selectors = [
    "div.fdq-res-header",
    "div.fdq-results",
    "#fdq-sec-100",
    "div.fdq-product-card",
    "div.fdq-res-wrap",
    "div.fdq-res",
    "div.fdq-hero-img",
    "div.fdq-h-name",
    "div.fdq-summary",
    "a.fdq-retake-btn",
    "div.fdq-wrap",
    "div.fdq-container",
]
for sel in selectors:
    loc = page.locator(sel)
    count = loc.count()
    visible = loc.first.is_visible() if count > 0 else False
    print(f"  {sel}: count={count}, visible={visible}")

# Dump unique fdq- classes
body_html = page.content()
classes = re.findall(r'class="([^"]*fdq[^"]*)"', body_html)
unique = sorted(set(classes))
print(f"\n--- FDQ classes on page ({len(unique)}) ---")
for c in unique[:50]:
    print(f"  {c}")

browser.close()
p.stop()
print("\nDone.")
