from FD.pages.base_page import BasePage


class RingSettingPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.url = "https://friendlydiamonds.com/ring-settings"

        # real product cards only
        self.product_box = "#list_top div.product_box"

        # 500 error page
        self.error_500 = "h2:text('Internal Server Error')"

    # ---------------------------------------------------
    # CHECK 500 PAGE
    # ---------------------------------------------------
    def is_500_page(self):

        try:
            return self.page.locator(
                self.error_500
            ).is_visible(timeout=3000)

        except:
            return False

    # ---------------------------------------------------
    # OPEN PLP WITH RETRY
    # ---------------------------------------------------
    def open_plp(self, retry=3):

        for attempt in range(1, retry + 1):

            try:

                print(f"\nOPENING PLP -> Attempt {attempt}")

                self.open_url(self.url)

                self.page.wait_for_load_state(
                    "domcontentloaded"
                )

                self.page.wait_for_timeout(5000)

                # ----------------------------------------
                # 500 CHECK
                # ----------------------------------------
                if self.is_500_page():

                    print("\n500 PAGE FOUND ON PLP")

                    if attempt == retry:

                        raise Exception(
                            "PLP opened with 500 page"
                        )

                    print("Retrying PLP...")
                    self.page.reload()

                    self.page.wait_for_timeout(5000)

                    continue

                # ----------------------------------------
                # WAIT PRODUCTS
                # ----------------------------------------
                self.page.wait_for_selector(
                    self.product_box,
                    timeout=60000
                )

                print("\nPLP LOADED SUCCESSFULLY")

                return

            except Exception as e:

                print(f"\nPLP LOAD FAILED: {str(e)}")

                if attempt == retry:

                    raise Exception(
                        f"PLP failed after retries: {str(e)}"
                    )

    # ---------------------------------------------------
    # GET PRODUCTS
    # ---------------------------------------------------
    def get_products(self):

        return self.page.locator(self.product_box)

    # ---------------------------------------------------
    # MAIN FLOW
    # ---------------------------------------------------
    def verify_all_products_metals(self):

        self.open_plp()

        metals = ["white", "yellow", "rose"]

        processed_urls = set()

        failed = []

        index = 0

        previous_count = 0

        stuck_scroll = 0

        while True:

            products = self.get_products()

            count = products.count()

            print(f"\nVISIBLE PRODUCTS: {count}")

            # ------------------------------------------------
            # STUCK PAGE DETECTION
            # ------------------------------------------------
            if count == previous_count:

                stuck_scroll += 1

            else:

                stuck_scroll = 0

            previous_count = count

            if stuck_scroll >= 3:

                print("\nPAGE STUCK AFTER MULTIPLE SCROLLS")

                failed.append({
                    "index": "-",
                    "product": "-",
                    "expected": "-",
                    "actual": "-",
                    "url": self.page.url,
                    "error": "PLP scrolling stuck"
                })

                break

            new_found = False

            for i in range(count):

                products = self.get_products()

                card = products.nth(i)

                try:

                    # ------------------------------------------------
                    # SAVE SCROLL POSITION
                    # ------------------------------------------------
                    scroll_y = self.page.evaluate(
                        "() => window.scrollY"
                    )

                    # ------------------------------------------------
                    # SKIP SHOP THE LOOK
                    # ------------------------------------------------
                    shop_the_look = card.locator(
                        "img[alt*='shop the look' i]"
                    )

                    if shop_the_look.count() > 0:

                        print("\nSkipping Shop The Look")

                        continue

                    anchor = card.locator(
                        "a.for_desktop.on_hover"
                    )

                    href = anchor.get_attribute("href")

                    if not href:
                        continue

                    full_url = (
                        "https://friendlydiamonds.com" + href
                    )

                    # ------------------------------------------------
                    # SKIP DUPLICATE
                    # ------------------------------------------------
                    if full_url in processed_urls:
                        continue

                    processed_urls.add(full_url)

                    new_found = True

                    index += 1

                    name = card.locator(
                        "h3"
                    ).inner_text().strip()

                    print(f"\nPRODUCT {index}")
                    print(f"Product Name: {name}")

                    # ------------------------------------------------
                    # METALS LOOP
                    # ------------------------------------------------
                    for metal in metals:

                        print(f"\nChecking Metal: {metal}")

                        swatch = card.locator(
                            f"div.metal_box.{metal}"
                        )

                        # --------------------------------------------
                        # SWATCH EXIST CHECK
                        # --------------------------------------------
                        if swatch.count() == 0:

                            print(
                                f"Swatch Missing -> {metal}"
                            )

                            failed.append({
                                "index": index,
                                "product": name,
                                "expected": metal,
                                "actual": "-",
                                "url": full_url,
                                "error": "Swatch missing"
                            })

                            continue

                        # --------------------------------------------
                        # CLICK SWATCH
                        # --------------------------------------------
                        cls = (
                            swatch.get_attribute("class")
                            or ""
                        )

                        if "active" not in cls:

                            swatch.click(force=True)

                            self.page.wait_for_timeout(1500)

                        # --------------------------------------------
                        # OPEN PDP
                        # --------------------------------------------
                        with self.page.expect_navigation():

                            anchor.click(force=True)

                        self.page.wait_for_load_state(
                            "domcontentloaded"
                        )

                        self.page.wait_for_timeout(3000)

                        # --------------------------------------------
                        # PDP 500 CHECK
                        # --------------------------------------------
                        if self.is_500_page():

                            print("\nPDP 500 ERROR")

                            failed.append({
                                "index": index,
                                "product": name,
                                "expected": metal,
                                "actual": "-",
                                "url": self.page.url,
                                "error": (
                                    "PDP Internal Server Error"
                                )
                            })

                            self.page.go_back()

                            self.page.wait_for_timeout(3000)

                            continue

                        current_url = (
                            self.page.url.lower()
                        )

                        print(f"PDP URL: {current_url}")

                        # --------------------------------------------
                        # METAL VALIDATION
                        # --------------------------------------------
                        if metal not in current_url:

                            print("\nMISMATCH FOUND")

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

                        # --------------------------------------------
                        # GO BACK TO PLP
                        # --------------------------------------------
                        self.page.go_back()

                        self.page.wait_for_load_state(
                            "domcontentloaded"
                        )

                        self.page.wait_for_timeout(4000)

                        # --------------------------------------------
                        # HANDLE 500 AFTER GO BACK
                        # --------------------------------------------
                        if self.is_500_page():

                            print(
                                "\n500 AFTER GO BACK"
                            )

                            retry_success = False

                            for retry in range(2):

                                print(
                                    f"Retry After Back "
                                    f"Attempt: {retry + 1}"
                                )

                                try:

                                    self.page.reload(
                                        wait_until=(
                                            "domcontentloaded"
                                        )
                                    )

                                    self.page.wait_for_timeout(
                                        5000
                                    )

                                    # still 500 ?
                                    if self.is_500_page():

                                        print(
                                            "Still getting "
                                            "500 page"
                                        )

                                        continue

                                    # products restored ?
                                    self.page.wait_for_selector(
                                        self.product_box,
                                        timeout=15000
                                    )

                                    print(
                                        "PLP restored "
                                        "successfully"
                                    )

                                    retry_success = True

                                    break

                                except Exception as e:

                                    print(
                                        f"Retry failed: "
                                        f"{str(e)}"
                                    )

                            # ----------------------------------------
                            # RECOVERY FAILED
                            # ----------------------------------------
                            if not retry_success:

                                print(
                                    "\nFAILED TO RECOVER "
                                    "PLP AFTER GO BACK"
                                )

                                failed.append({
                                    "index": index,
                                    "product": name,
                                    "expected": metal,
                                    "actual": "-",
                                    "url": self.page.url,
                                    "error": (
                                        "500/Internal issue "
                                        "after go_back and "
                                        "retry recovery failed"
                                    )
                                })

                                print(
                                    "\nRe-opening fresh PLP"
                                )

                                self.open_plp()

                                self.page.wait_for_timeout(
                                    4000
                                )

                                self.page.evaluate(
                                    f"window.scrollTo("
                                    f"0, {scroll_y})"
                                )

                                self.page.wait_for_timeout(
                                    2000
                                )

                                continue

                        # --------------------------------------------
                        # RESTORE SCROLL POSITION
                        # --------------------------------------------
                        self.page.evaluate(
                            f"window.scrollTo("
                            f"0, {scroll_y})"
                        )

                        self.page.wait_for_timeout(2000)

                except Exception as e:

                    print("\nERROR PRODUCT")

                    print(f"- Index: {index}")

                    print(
                        f"- Product: "
                        f"{name if 'name' in locals() else '-'}"
                    )

                    print(f"- URL: {self.page.url}")

                    print(f"- Error: {str(e)}")

                    failed.append({
                        "index": index,
                        "product": (
                            name
                            if 'name' in locals()
                            else "-"
                        ),
                        "expected": "-",
                        "actual": "-",
                        "url": self.page.url,
                        "error": str(e)
                    })

            # ------------------------------------------------
            # SCROLL FOR MORE PRODUCTS
            # ------------------------------------------------
            if not new_found:

                print(
                    "\nSCROLLING FOR MORE PRODUCTS..."
                )

                old_height = self.page.evaluate(
                    "() => document.body.scrollHeight"
                )

                self.page.mouse.wheel(0, 5000)

                self.page.wait_for_timeout(4000)

                new_height = self.page.evaluate(
                    "() => document.body.scrollHeight"
                )

                if old_height == new_height:

                    print(
                        "\nNO NEW PRODUCTS LOADED"
                    )

            # ------------------------------------------------
            # STOP CONDITION
            # ------------------------------------------------
            if len(processed_urls) >= 225:

                print(
                    "\nALL PRODUCTS COVERED"
                )

                break

        # ------------------------------------------------
        # FINAL REPORT
        # ------------------------------------------------
        print(
            "\n================ FINAL REPORT "
            "================"
        )

        print(
            f"TOTAL PRODUCTS CHECKED: "
            f"{len(processed_urls)}"
        )

        print(f"FAILED: {len(failed)}")

        for f in failed:

            print("\n-------------------")

            print(f"- Index: {f['index']}")

            print(f"- Product: {f['product']}")

            print(f"- Expected: {f['expected']}")

            print(f"- Actual: {f['actual']}")

            print(f"- URL: {f['url']}")

            print(f"- Error: {f['error']}")

        if not failed:

            print("\nALL PRODUCTS PASSED")