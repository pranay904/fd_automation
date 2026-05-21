from FD.pages.base_page import BasePage


class RingSettingPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.url = "https://friendlydiamonds.com/ring-settings"

        # ONLY real product cards
        self.product_box = "#list_top div.product_box"

    # -------------------------
    # OPEN PLP
    # -------------------------
    def open_plp(self):

        self.open_url(self.url)

        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(4000)

        self.page.wait_for_selector(self.product_box, timeout=60000)

    # -------------------------
    # GET PRODUCT LOCATOR
    # -------------------------
    def get_products(self):
        return self.page.locator(self.product_box)

    # -------------------------
    # MAIN TEST FLOW
    # -------------------------
    def verify_all_products_metals(self):

        self.open_plp()

        metals = ["white", "yellow", "rose"]

        processed_urls = set()
        failed = []

        index = 0
        completed = 0

        while True:

            products = self.get_products()
            count = products.count()

            print(f"\nVISIBLE PRODUCTS: {count}")

            new_found = False

            for i in range(count):

                card = products.nth(i)

                try:
                    anchor = card.locator("a.for_desktop.on_hover")

                    href = anchor.get_attribute("href")

                    if not href:
                        continue

                    full_url = "https://friendlydiamonds.com" + href

                    # avoid duplicate processing
                    if full_url in processed_urls:
                        continue

                    processed_urls.add(full_url)
                    new_found = True

                    index += 1

                    name = card.locator("h3").inner_text().strip()

                    print(f"\nPRODUCT {index}")
                    print(f"Product Name: {name}")

                    for metal in metals:

                        print(f"\nChecking Metal: {metal}")

                        swatch = card.locator(f"div.metal_box.{metal}")

                        try:
                            swatch.wait_for(timeout=5000)
                        except:
                            print(f"Swatch not found: {metal}")
                            continue

                        cls = swatch.get_attribute("class") or ""

                        # click only if not active
                        if "active" not in cls:
                            swatch.click(force=True)
                            self.page.wait_for_timeout(1500)

                        # open PDP
                        with self.page.expect_navigation():
                            anchor.click(force=True)

                        self.page.wait_for_load_state("domcontentloaded")
                        self.page.wait_for_timeout(3000)

                        current_url = self.page.url.lower()

                        print(f"PDP URL: {current_url}")

                        if metal not in current_url:

                            print("\n MISMATCH")
                            print(f"Expected: {metal}")
                            print(f"Actual URL: {current_url}")

                            failed.append({
                                "index": index,
                                "product": name,
                                "expected": metal,
                                "actual": current_url,
                                "url": current_url,
                                "error": "Metal mismatch"
                            })

                        else:
                            print(f"PASSED -> {metal}")

                        # go back to PLP
                        self.page.go_back()
                        self.page.wait_for_load_state("domcontentloaded")
                        self.page.wait_for_timeout(3000)

                        # re-locate product after back
                        products = self.get_products()
                        card = products.nth(i)

                        anchor = card.locator("a.for_desktop.on_hover")

                except Exception as e:

                    print("\n ERROR PRODUCT")
                    print(f"Index: {index}")
                    print(f"Error: {e}")

                    failed.append({
                        "index": index,
                        "product": "N/A",
                        "expected": "-",
                        "actual": "-",
                        "url": self.page.url,
                        "error": str(e)
                    })

            # -------------------------
            # SCROLL ONLY IF NEW ITEMS EXPECTED
            # -------------------------
            if not new_found:
                print("\nSCROLLING FOR MORE PRODUCTS...")
                self.page.mouse.wheel(0, 5000)
                self.page.wait_for_timeout(3000)

            # STOP CONDITION (safe)
            if len(processed_urls) >= 225:
                break

        # -------------------------
        # FINAL REPORT
        # -------------------------
        print("\n================ FINAL REPORT ================")
        print(f"TOTAL PRODUCTS CHECKED: {len(processed_urls)}")
        print(f"FAILED: {len(failed)}")

        for f in failed:
            print("\n-------------------")
            print(f"Index: {f['index']}")
            print(f"Product: {f['product']}")
            print(f"Expected: {f['expected']}")
            print(f"Actual: {f['actual']}")
            print(f"URL: {f['url']}")
            print(f"Error: {f['error']}")

        if not failed:
            print("\nALL PRODUCTS PASSED")