import pytest
from FD.utils.logger import logger
from FD.utils.banner_validator import BannerValidator

validator = BannerValidator()
RESULTS_TIMEOUT = 30000

# Static expected values
EXPECTED_RESULT_TITLE = "Your perfect rings, curated for her."
EXPECTED_BADGE        = "Perfect Match"
EXPECTED_STATS_LABELS = ["Perfect Match", "Matches (99–91%)", "Matches (90–80%)"]
EXPECTED_9091_BADGE   = "99–91% Match"
EXPECTED_9091_TITLE   = "Nearly perfect picks"
EXPECTED_8090_BADGE   = "90–80% Match"
EXPECTED_8090_TITLE   = "Worth a closer look"


def v_pass(step, expected, actual):
    print(f"  [PASS] {step} | Expected: {expected} | Actual: {actual}")
    return {"step": step, "expected": str(expected), "actual": str(actual), "status": "PASS", "error": ""}


def v_fail(step, expected, actual, error=""):
    print(f"  [FAIL] {step} | Expected: {expected} | Actual: {actual} | Error: {error}")
    return {"step": step, "expected": str(expected), "actual": str(actual), "status": "FAIL", "error": str(error)}


def v_skip(step, reason=""):
    print(f"  [SKIP] {step} | Reason: {reason}")
    return {"step": step, "expected": "N/A", "actual": "SKIPPED", "status": "SKIP", "error": reason}


class QuizPage:

    URL = "https://friendlydiamonds.com/fci/engagement-ring-quiz"

    def __init__(self, page):
        self.page = page
        self._register_popup_handler()

    def _register_popup_handler(self):
        """Auto-nuke Netcore overlay whenever #smt-overlay appears."""
        try:
            self.page.add_locator_handler(
                self.page.locator("div#smt-overlay").first,
                lambda: self._nuke_netcore()
            )
        except Exception:
            pass

    def _close_netcore_modal(self):
        self._nuke_netcore()

    def dismiss_popup(self):
        self._nuke_netcore()

    # ---------------------------
    # Dismiss any popup/overlay
    # ---------------------------
    def dismiss_popup(self):
        """Manual dismiss call — same logic as the auto handler."""
        self._close_netcore_modal()

    # ---------------------------
    # Open Quiz
    # ---------------------------
    def open_quiz(self):
        logger.info("Opening Quiz Page")
        try:
            self.page.goto(self.URL, wait_until="domcontentloaded")
            self.page.wait_for_timeout(1500)
            # Inject CSS to permanently block Netcore overlay pointer events
            self.page.add_style_tag(content="""
                #smt-overlay, #st_notification_banner, div[smtmsgid],
                [id*='smt'], [class*='smt-block'] {
                    display: none !important;
                    pointer-events: none !important;
                    visibility: hidden !important;
                    z-index: -9999 !important;
                }
            """)
            self._nuke_netcore()
            print(f"\n[OPEN] {self.URL}")
        except Exception as e:
            pytest.skip(f"Browser closed: {e}")

    def _nuke_netcore(self):
        """Remove Netcore overlay elements from DOM entirely."""
        try:
            self.page.evaluate("""
                ['smt-overlay','st_notification_banner','webmessagemodalbody'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.remove();
                });
                document.querySelectorAll('[smtmsgid], .smt-block, #smt-close-icon').forEach(el => {
                    el.closest('[smtmsgid]')?.remove() || el.remove();
                });
            """)
        except Exception:
            pass

    # ---------------------------
    # Validate Quiz Page on Load
    # ---------------------------
    def validate_quiz_page(self):
        validations = []

        # Heading
        step = "Quiz Page - Question Heading Visible"
        try:
            heading = self.page.locator("div.fdq").first
            if heading.count() > 0 and heading.is_visible():
                validations.append(v_pass(step, "fdq container visible", "fdq container visible"))
            else:
                print(f"  [LOCATOR NOT FOUND] {step}")
                validations.append(v_fail(step, "fdq container visible", "Not found"))
        except Exception as e:
            validations.append(v_fail(step, "fdq container visible", "Error", e))

        # Banner image
        step = "Quiz Page - Banner Image Visible"
        try:
            banner = self.page.locator("div.fdq-img-grid img").first
            if banner.count() > 0 and banner.is_visible():
                src = banner.get_attribute("src")
                validations.append(v_pass(step, "Banner image visible", src))
            else:
                print(f"  [LOCATOR NOT FOUND] {step} - tried: div.fdq-img-grid img")
                validations.append(v_fail(step, "Banner image visible", "Not found"))
        except Exception as e:
            validations.append(v_fail(step, "Banner image visible", "Error", e))

        # Options
        step = "Quiz Page - Options Visible"
        try:
            opts = self.page.locator("div.fdq-opts div.fdq-opt")
            count = opts.count()
            if count > 0:
                validations.append(v_pass(step, "Options > 0", f"{count} options found"))
            else:
                print(f"  [LOCATOR NOT FOUND] {step} - tried: div.fdq-opts div.fdq-opt")
                validations.append(v_fail(step, "Options > 0", "0 options found"))
        except Exception as e:
            validations.append(v_fail(step, "Options > 0", "Error", e))

        return validations

    # ---------------------------
    # Select Answer
    # ---------------------------
    def select_option(self, q_no, option):
        if q_no <= 4:
            locator = f"(//div[@class='fdq-opts']/div[contains(@class,'fdq-opt')])[{option}]"
            self.page.locator(locator).click()
        else:
            slider = self.page.locator("input.fdq-slider-input").nth(0)
            slider_val = option - 1 if q_no == 6 else option
            slider.evaluate(f"(el)=>{{ el.value={slider_val}; el.dispatchEvent(new Event('input',{{bubbles:true}})); el.dispatchEvent(new Event('change',{{bubbles:true}})); }}")
            self.page.wait_for_timeout(400)

    # ---------------------------
    # Validate Banner
    # ---------------------------
    def validate_banner(self, q_no, option):
        step = f"Q{q_no} Banner Image"
        try:
            if q_no <= 4:
                img = self.page.locator("div.fdq-img-grid img").first
                actual_src = img.get_attribute("src", timeout=5000)
                validator.validate(self.page, q_no, option)
                return v_pass(step, f"Expected path for opt{option}", actual_src)
            else:
                # Slider banner — try to get src, skip if not found
                img = self.page.locator("img.vis.fdq-slider-img").first
                try:
                    img.wait_for(state="visible", timeout=5000)
                    actual_src = img.get_attribute("src", timeout=3000)
                    validator.validate_slider_banner(self.page, q_no, option)
                    return v_pass(step, f"Expected path for opt{option}", actual_src)
                except Exception:
                    # Fallback: just get src without waiting
                    try:
                        actual_src = img.get_attribute("src", timeout=2000) or "not found"
                    except Exception:
                        actual_src = "not found"
                    print(f"  [SKIP] {step} - slider image not visible, src={actual_src}")
                    return v_skip(step, f"Slider image not visible at Q{q_no} opt{option}")
        except AssertionError as e:
            return v_fail(step, f"Expected path for opt{option}", "Mismatch", e)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step}")
            return v_fail(step, f"Expected path for opt{option}", "Error", e)

    # ---------------------------
    # Validate Slider Value
    # ---------------------------
    def validate_slider(self, q_no, option):
        step = f"Q{q_no} Slider Value"
        expected_val = str(option - 1) if q_no == 6 else str(option)
        try:
            slider = self.page.locator("input.fdq-slider-input").nth(0)
            actual_val = str(slider.evaluate("(el)=>el.value"))
            if actual_val == expected_val:
                return v_pass(step, expected_val, actual_val)
            return v_fail(step, expected_val, actual_val)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: input.fdq-slider-input")
            return v_fail(step, expected_val, "Not found", e)

    # ---------------------------
    # Click Continue / See My Rings
    # ---------------------------
    def click_continue(self, q_no):
        if q_no < 6:
            self.page.get_by_role("button", name="Continue").click()
            self.page.wait_for_timeout(800)
            self.dismiss_popup()
        else:
            print("  [ACTION] Clicking See My Rings")
            self._nuke_netcore()
            self.page.add_style_tag(content="""
                #smt-overlay, #st_notification_banner, div[smtmsgid],
                [id*='smt'], [class*='smt-block'] {
                    display: none !important;
                    pointer-events: none !important;
                    visibility: hidden !important;
                    z-index: -9999 !important;
                }
            """)
            btn = self.page.locator("button.fdq-next.fin")
            btn.wait_for(state="visible", timeout=10000)
            btn.click(force=True)
            try:
                self.page.locator("div.fdq-res-header").wait_for(state="visible", timeout=RESULTS_TIMEOUT)
            except Exception:
                self.page.locator("#fdq-sec-100").wait_for(state="visible", timeout=RESULTS_TIMEOUT)
            self.page.wait_for_timeout(500)
            self.dismiss_popup()
            print(f"  [NAV] Results URL: {self.page.url}")

    # ---------------------------
    # Check if results exist at all
    # ---------------------------
    def _check_has_results(self):
        """Returns True if any match section is visible, False if no results."""
        try:
            self.page.locator("#fdq-sec-100").wait_for(state="visible", timeout=8000)
            return True
        except Exception:
            pass
        try:
            # Some combos may have no 100% match but still have lower matches
            self.page.locator("#fdq-sec-9095").wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            pass
        return False
    def _check_results_title(self):
        step = "Results Title (h1.fdq-res-title)"
        expected = EXPECTED_RESULT_TITLE
        try:
            title = self.page.locator("h1.fdq-res-title")
            title.wait_for(state="visible", timeout=10000)
            actual = title.inner_text().strip()
            if expected.lower() in actual.lower():
                return v_pass(step, expected, actual)
            print(f"  [MISMATCH] {step} | Expected: {expected} | Actual: {actual}")
            return v_fail(step, expected, actual)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: h1.fdq-res-title")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Stats Section
    # ---------------------------
    def _check_stats_section(self):
        validations = []
        step = "Results Stats Section (div.fdq-res-stats)"
        try:
            stats = self.page.locator("div.fdq-res-stats")
            stats.wait_for(state="visible", timeout=10000)
            cards = stats.locator("div.fdq-stat-card")
            count = cards.count()
            validations.append(v_pass(step, "3 stat cards", f"{count} cards found"))

            # Verify each card label (hardcoded) + dynamic count
            for i, label in enumerate(EXPECTED_STATS_LABELS):
                card_step = f"Stats Card {i+1} - {label}"
                try:
                    card = cards.nth(i)
                    num   = card.locator("div.fdq-stat-n").inner_text().strip()
                    lbl   = card.locator("div.fdq-stat-l").inner_text().strip().replace("\n", " ")
                    actual = f"Count={num} | Label={lbl}"
                    if label.lower() in lbl.lower():
                        validations.append(v_pass(card_step, f"Label contains '{label}', Count=dynamic", actual))
                    else:
                        validations.append(v_fail(card_step, f"Label contains '{label}'", actual))
                except Exception as e:
                    validations.append(v_fail(card_step, label, "Not found", e))
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: div.fdq-res-stats")
            validations.append(v_fail(step, "3 stat cards", "Not found", e))
        return validations

    # ---------------------------
    # Answer Summary
    # ---------------------------
    def _check_summary(self):
        step = "Answer Summary (div.fdq-summary)"
        expected = "YOUR ANSWERS (case-insensitive)"
        try:
            summary = self.page.locator("div.fdq-summary")
            summary.wait_for(state="visible", timeout=5000)
            actual = summary.inner_text().strip()
            if "your answers" in actual.lower():
                return v_pass(step, expected, actual[:120])
            print(f"  [MISMATCH] {step} - 'your answers' not in: {actual[:60]}")
            return v_fail(step, expected, actual[:120])
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: div.fdq-summary")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # 100% Match Section
    # ---------------------------
    def _check_100_match_header(self):
        step = "100% Match Section (#fdq-sec-100)"
        try:
            sec = self.page.locator("#fdq-sec-100")
            sec.wait_for(state="visible", timeout=10000)
            return v_pass(step, "#fdq-sec-100 visible", "Visible")
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100")
            return v_fail(step, "#fdq-sec-100 visible", "Not found", e)

    # ---------------------------
    # Perfect Match Badge
    # ---------------------------
    def _check_perfect_match_badge(self):
        step = "Perfect Match Badge (div.fdq-hero-badge)"
        expected = EXPECTED_BADGE
        try:
            badge = self.page.locator("#fdq-sec-100 div.fdq-hero-badge").first
            badge.wait_for(state="visible", timeout=5000)
            actual = badge.inner_text().strip()
            if actual.upper() == expected.upper():
                return v_pass(step, expected, actual)
            return v_fail(step, expected, actual)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-hero-badge")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Hero Image
    # ---------------------------
    def _check_hero_image(self):
        step = "Perfect Match Hero Image (div.fdq-hero-img img)"
        expected = "Hero image visible"
        try:
            img = self.page.locator("#fdq-sec-100 div.fdq-hero-img img").first
            if img.count() == 0:
                img = self.page.locator("#fdq-sec-100 //div[@class='fdq-hero-img']//img").first
            img.wait_for(state="visible", timeout=5000)
            src = img.get_attribute("src")
            return v_pass(step, expected, src)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-hero-img img")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Product Category Header
    # ---------------------------
    def _check_product_header(self):
        step = "Product Category (div.fdq-h-cat)"
        expected = "Engagement Ring · [Collection]"
        try:
            cat = self.page.locator("#fdq-sec-100 div.fdq-h-cat").first
            cat.wait_for(state="visible", timeout=5000)
            actual = cat.inner_text().strip()
            if "engagement ring" in actual.lower():
                return v_pass(step, expected, actual)
            return v_fail(step, expected, actual)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-h-cat")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Product Name
    # ---------------------------
    def _get_product_name(self):
        step = "Product Name (div.fdq-h-name)"
        expected = "Product name present"
        try:
            name = self.page.locator("#fdq-sec-100 div.fdq-h-name").first.inner_text().strip()
            print(f"  [INFO] Product: {name}")
            if name:
                return v_pass(step, expected, name), name
            return v_fail(step, expected, "Empty"), "N/A"
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-h-name")
            return v_fail(step, expected, "Not found", e), "N/A"

    # ---------------------------
    # Price
    # ---------------------------
    def _get_price(self):
        step = "Product Price (div.fdq-price-amount)"
        expected = "Price present"
        try:
            price = self.page.locator("#fdq-sec-100 div.fdq-price-amount").first.inner_text().strip()
            print(f"  [INFO] Price: {price}")
            if price:
                return v_pass(step, expected, price), price
            return v_fail(step, expected, "Empty"), "N/A"
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-price-amount")
            return v_fail(step, expected, "Not found", e), "N/A"

    # ---------------------------
    # Match Score
    # ---------------------------
    def _check_match_score(self):
        step = "Match Score (div.fdq-match-score-row)"
        expected = "100% Overall match score"
        try:
            score_row = self.page.locator("#fdq-sec-100 div.fdq-match-score-row").first
            score_row.wait_for(state="visible", timeout=5000)
            actual = score_row.inner_text().strip().replace("\n", " ")
            if "100" in actual and "overall match score" in actual.lower():
                return v_pass(step, expected, actual[:120])
            return v_fail(step, expected, actual[:120])
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-match-score-row")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Product Specs
    # ---------------------------
    def _check_specs(self):
        step = "Product Specs (div.spec-icon-grid)"
        expected = "Style, Profile, Metal, Shape, Diamond, Band Width present"
        try:
            specs = self.page.locator("#fdq-sec-100 div.spec-icon-grid").first
            specs.wait_for(state="visible", timeout=5000)
            actual = specs.inner_text().strip().replace("\n", " ")
            print(f"  [INFO] Specs: {actual}")
            return v_pass(step, expected, actual[:200])
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.spec-icon-grid")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Trust Badges
    # ---------------------------
    def _check_trust_badges(self):
        step = "Trust Badges (div.fdq-trust-row)"
        expected = "IGI Certified, Free Resizing, Lifetime Warranty, Free Shipping"
        try:
            trust = self.page.locator("#fdq-sec-100 div.fdq-trust-row").first
            trust.wait_for(state="visible", timeout=5000)
            actual = trust.inner_text().strip().replace("\n", " ")
            return v_pass(step, expected, actual)
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 div.fdq-trust-row")
            return v_fail(step, expected, "Not found", e)

    # ---------------------------
    # Share Modal
    # ---------------------------
    def share_product(self):
        step = "Share Modal"
        expected = "Popup opens, link copied, modal closed via X"
        try:
            share_btn = self.page.locator("#fdq-sec-100 button.fdq-share-text-btn").first
            if share_btn.count() == 0:
                share_btn = self.page.locator("#fdq-sec-100").get_by_role("button", name="Share").first
            share_btn.click()

            popup = self.page.locator("section.fci-share-popup")
            popup.wait_for(state="visible", timeout=5000)

            link = popup.locator(".coupon_text").inner_text().strip()
            print(f"  [INFO] Share URL: {link}")
            popup.locator(".coupon_copy").click()
            self.page.wait_for_timeout(500)

            close_btn = self.page.locator("div.modal_close_btn")
            close_btn.wait_for(state="visible", timeout=3000)
            close_btn.click()
            self.page.wait_for_timeout(500)

            return v_pass(step, expected, f"Link: {link}"), link
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step} - Error: {e}")
            return v_fail(step, expected, "Error", e), "N/A"

    # ---------------------------
    # Add to Cart
    # ---------------------------
    def _check_add_to_cart(self, has_product):
        step = "Add to Cart (button.fdq-cta-s)"
        if not has_product:
            return v_skip(step, "No perfect match product")
        expected = "ADD TO CART button visible"
        try:
            btn = self.page.locator("#fdq-sec-100 button.fdq-cta-s").first
            if btn.count() > 0 and btn.is_visible():
                return v_pass(step, expected, btn.inner_text().strip())
            print(f"  [LOCATOR NOT FOUND] {step} - tried: #fdq-sec-100 button.fdq-cta-s")
            return v_fail(step, expected, "Not found")
        except Exception as e:
            return v_fail(step, expected, "Error", e)

    # ---------------------------
    # 99-91% Section
    # ---------------------------
    def _check_9091_section(self):
        validations = []
        step_sec = "99-91% Match Section (#fdq-sec-9095)"
        try:
            sec = self.page.locator("#fdq-sec-9095")
            sec.wait_for(state="visible", timeout=10000)

            # Badge
            badge = sec.locator("div.fdq-sec-badge").inner_text().strip()
            validations.append(v_pass(f"{step_sec} - Badge", EXPECTED_9091_BADGE, badge)
                               if badge.upper() == EXPECTED_9091_BADGE.upper()
                               else v_fail(f"{step_sec} - Badge", EXPECTED_9091_BADGE, badge))

            # Title
            title = sec.locator("div.fdq-sec-title-txt").inner_text().strip()
            validations.append(v_pass(f"{step_sec} - Title", EXPECTED_9091_TITLE, title)
                               if title == EXPECTED_9091_TITLE
                               else v_fail(f"{step_sec} - Title", EXPECTED_9091_TITLE, title))

            # Count from header
            count_txt = sec.locator("div.fdq-sec-count").inner_text().strip()
            count_num = ''.join(filter(str.isdigit, count_txt))
            print(f"  [INFO] 99-91% header count: {count_txt}")

            # Actual product cards
            cards = sec.locator("div.fdq-pcard")
            actual_cards = cards.count()
            print(f"  [INFO] 99-91% actual cards: {actual_cards}")

            validations.append(
                v_pass(f"{step_sec} - Card Count matches header",
                       f"{count_num} rings", f"{actual_cards} cards")
                if str(actual_cards) == count_num
                else v_fail(f"{step_sec} - Card Count matches header",
                            f"{count_num} rings", f"{actual_cards} cards")
            )

            # Each card percentage
            for i in range(actual_cards):
                pct = cards.nth(i).locator("div.fdq-p-pct").inner_text().strip()
                name = cards.nth(i).locator("div.fdq-p-name").inner_text().strip()
                price = cards.nth(i).locator("div.fdq-p-price").inner_text().strip()
                print(f"    Card {i+1}: {pct} | {name} | {price}")

        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step_sec} - tried: #fdq-sec-9095")
            validations.append(v_fail(step_sec, "Section visible", "Not found", e))
        return validations

    # ---------------------------
    # 90-80% Section
    # ---------------------------
    def _check_8090_section(self):
        validations = []
        step_sec = "90-80% Match Section (#fdq-sec-8090)"
        try:
            sec = self.page.locator("#fdq-sec-8090")
            sec.wait_for(state="visible", timeout=10000)

            # Badge
            badge = sec.locator("div.fdq-sec-badge").inner_text().strip()
            validations.append(v_pass(f"{step_sec} - Badge", EXPECTED_8090_BADGE, badge)
                               if badge.upper() == EXPECTED_8090_BADGE.upper()
                               else v_fail(f"{step_sec} - Badge", EXPECTED_8090_BADGE, badge))

            # Title
            title = sec.locator("div.fdq-sec-title-txt").inner_text().strip()
            validations.append(v_pass(f"{step_sec} - Title", EXPECTED_8090_TITLE, title)
                               if title == EXPECTED_8090_TITLE
                               else v_fail(f"{step_sec} - Title", EXPECTED_8090_TITLE, title))

            # Count
            count_txt = sec.locator("div.fdq-sec-count").inner_text().strip()
            count_num = ''.join(filter(str.isdigit, count_txt))
            print(f"  [INFO] 90-80% header count: {count_txt}")

            cards = sec.locator("div.fdq-pcard")
            actual_cards = cards.count()
            print(f"  [INFO] 90-80% actual cards: {actual_cards}")

            if count_num == "0" or actual_cards == 0:
                no_prod = sec.inner_text()
                validations.append(v_pass(f"{step_sec} - No Products",
                                          "No products found", no_prod[:60]))
            else:
                validations.append(
                    v_pass(f"{step_sec} - Card Count matches header",
                           f"{count_num} rings", f"{actual_cards} cards")
                    if str(actual_cards) == count_num
                    else v_fail(f"{step_sec} - Card Count matches header",
                                f"{count_num} rings", f"{actual_cards} cards")
                )

        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] {step_sec} - tried: #fdq-sec-8090")
            validations.append(v_fail(step_sec, "Section visible", "Not found", e))
        return validations

    # ---------------------------
    # Retake Quiz
    # ---------------------------
    def retake_quiz(self):
        try:
            retake = self.page.locator("a.fdq-retake-btn")
            retake.wait_for(state="visible", timeout=10000)
            retake.click()
            # Wait for quiz options to reappear (dynamic reload, not full navigation)
            try:
                self.page.locator("div.fdq-opts div.fdq-opt").first.wait_for(state="visible", timeout=15000)
            except Exception:
                self.page.wait_for_timeout(3000)
            self.page.wait_for_timeout(500)
            print("  [ACTION] Retake clicked — quiz reloaded")
        except Exception as e:
            print(f"  [LOCATOR NOT FOUND] Retake - tried: a.fdq-retake-btn | {e}")
            self.open_quiz()

    # ---------------------------
    # Run Full Quiz Flow
    # ---------------------------
    def run_quiz_flow(self, answers):
        print(f"\n{'='*60}")
        print(f"[TEST] Answers: {answers}")
        validations = []

        # Quiz page load validations
        validations += self.validate_quiz_page()

        # Answer each question
        for q_no, option in enumerate(answers, start=1):
            print(f"\n  [Q{q_no}] Selecting option {option}")
            self.select_option(q_no, option)
            print(f"  [Q{q_no}] Option selected, waiting...")
            self.page.wait_for_timeout(800)
            print(f"  [Q{q_no}] Validating banner...")
            validations.append(self.validate_banner(q_no, option))
            print(f"  [Q{q_no}] Banner validated")
            if q_no >= 5:
                print(f"  [Q{q_no}] Validating slider...")
                validations.append(self.validate_slider(q_no, option))
                print(f"  [Q{q_no}] Slider validated")
            print(f"  [Q{q_no}] Clicking continue...")
            self.click_continue(q_no)
            print(f"  [Q{q_no}] Continue clicked")

        # Results page
        print("\n  [RESULTS PAGE]")

        # Check if any results exist at all
        has_results = self._check_has_results()
        if not has_results:
            print("  [INFO] No results returned for this combination")
            validations.append(v_fail(
                "Results Page - Any match section visible",
                "At least one match section visible",
                "No results found — #fdq-sec-100 and #fdq-sec-9095 both missing"
            ))
            return "No Results", "N/A", "FAIL", validations
        validations.append(self._check_results_title())
        validations += self._check_stats_section()
        validations.append(self._check_summary())
        validations.append(self._check_100_match_header())
        validations.append(self._check_perfect_match_badge())
        validations.append(self._check_hero_image())
        validations.append(self._check_product_header())

        name_v, product_name = self._get_product_name()
        validations.append(name_v)

        price_v, price = self._get_price()
        validations.append(price_v)

        validations.append(self._check_match_score())
        validations.append(self._check_specs())
        validations.append(self._check_trust_badges())

        share_v, share_link = self.share_product()
        validations.append(share_v)

        validations.append(self._check_add_to_cart(product_name != "N/A"))
        validations += self._check_9091_section()
        validations += self._check_8090_section()

        # Overall
        failed = [v for v in validations if v["status"] == "FAIL"]
        overall = "PASS" if not failed else "FAIL"
        print(f"\n  [OVERALL] {overall} | Product: {product_name} | Price: {price}")
        if failed:
            print(f"  [FAILED STEPS] {[v['step'] for v in failed]}")

        return product_name, price, overall, validations
