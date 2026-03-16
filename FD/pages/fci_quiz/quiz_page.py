from FD.utils.logger import logger
from FD.utils.banner_validator import BannerValidator

validator = BannerValidator()
RESULTS_TIMEOUT = 30000


def v_pass(step, expected, actual):
    return {"step": step, "expected": expected, "actual": actual, "status": "PASS", "error": ""}


def v_fail(step, expected, actual, error=""):
    return {"step": step, "expected": expected, "actual": actual, "status": "FAIL", "error": str(error)}


class QuizPage:

    URL = "https://friendlydiamonds.com/fci/engagement-ring-quiz"

    def __init__(self, page):
        self.page = page

    def open_quiz(self):
        logger.info("Opening Quiz Page")
        self.page.goto(self.URL)
        self.page.wait_for_timeout(3000)

    def select_option(self, q_no, option):
        if q_no <= 4:
            locator = f"(//div[@class='fdq-opts']/div[contains(@class,'fdq-opt')])[{option}]"
            logger.info(f"Q{q_no} selecting option {option}")
            self.page.locator(locator).click()
        else:
            slider = self.page.locator("input.fdq-slider-input").nth(0)
            logger.info(f"Q{q_no} slider -> {option}")
            slider.evaluate(f"(el)=>el.value={option}")
            slider.dispatch_event("change")
            self.page.wait_for_timeout(500)

    def validate_banner(self, q_no, option):
        step = f"Q{q_no} Banner"
        try:
            if q_no <= 4:
                validator.validate(self.page, q_no, option)
            else:
                validator.validate_slider_banner(self.page, q_no, option)
            return v_pass(step, f"Correct banner for Q{q_no} opt{option}", "Matched")
        except AssertionError as e:
            return v_fail(step, f"Correct banner for Q{q_no} opt{option}", "Mismatch", e)
        except Exception as e:
            return v_fail(step, f"Correct banner for Q{q_no} opt{option}", "Error", e)

    def click_continue(self, q_no):
        if q_no < 6:
            self.page.get_by_role("button", name="Continue").click()
            self.page.wait_for_timeout(1500)
        else:
            logger.info("Q6 clicking See My Rings")
            btn = self.page.locator("button.fdq-next.fin")
            btn.wait_for(state="visible", timeout=10000)
            btn.click()
            # Wait for URL to change to result page
            self.page.wait_for_url("**/result**", timeout=RESULTS_TIMEOUT)
            self.page.wait_for_timeout(3000)
            logger.info(f"Results URL: {self.page.url}")

    # ---------------------------
    # Individual validations
    # ---------------------------
    def _check_results_header(self):
        step = "Results Header"
        expected = "Results header visible"
        try:
            header = self.page.locator("div.fdq-res-header")
            header.wait_for(state="visible", timeout=10000)
            actual = header.inner_text().strip()
            if actual:
                return v_pass(step, expected, actual[:80])
            return v_fail(step, expected, "Empty text")
        except Exception as e:
            return v_fail(step, expected, "Not found", e)

    def _check_summary(self):
        step = "Answer Summary"
        expected = "Summary section visible"
        try:
            summary = self.page.locator("div.fdq-summary")
            summary.wait_for(state="visible", timeout=5000)
            actual = summary.inner_text().strip()
            if actual:
                return v_pass(step, expected, actual[:80])
            return v_fail(step, expected, "Empty text")
        except Exception as e:
            return v_fail(step, expected, "Not found", e)

    def _check_100_match_header(self):
        step = "100% Match Section"
        expected = "#fdq-sec-100 visible"
        try:
            sec = self.page.locator("#fdq-sec-100")
            sec.wait_for(state="visible", timeout=10000)
            return v_pass(step, expected, "Visible")
        except Exception as e:
            return v_fail(step, expected, "Not visible", e)

    def _get_product_name(self):
        step = "Product Name"
        expected = "Product name present"
        try:
            sec = self.page.locator("#fdq-sec-100")
            name = sec.locator("div.fdq-h-name").first.inner_text().strip()
            if name:
                return v_pass(step, expected, name), name
            return v_fail(step, expected, "Empty"), "N/A"
        except Exception as e:
            return v_fail(step, expected, "Not found", e), "N/A"

    def _get_price(self):
        step = "Product Price"
        expected = "Price present"
        try:
            sec = self.page.locator("#fdq-sec-100")
            price = sec.locator("div.fdq-price-amount").first.inner_text().strip()
            if price:
                return v_pass(step, expected, price), price
            return v_fail(step, expected, "Empty"), "N/A"
        except Exception as e:
            return v_fail(step, expected, "Not found", e), "N/A"

    def _check_match_score(self):
        step = "Match Score"
        expected = "100% Overall match score"
        try:
            sec = self.page.locator("#fdq-sec-100")
            score = sec.locator("div.fdq-match-score-row").first.inner_text().strip()
            if "100%" in score:
                return v_pass(step, expected, score[:80])
            return v_fail(step, expected, score[:80])
        except Exception as e:
            return v_fail(step, expected, "Not found", e)

    def _check_trust_badges(self):
        step = "Trust Badges"
        expected = "Trust badges visible"
        try:
            sec = self.page.locator("#fdq-sec-100")
            trust = sec.locator("div.fdq-trust-row").first
            if trust.count() > 0 and trust.is_visible():
                return v_pass(step, expected, "Visible")
            return v_fail(step, expected, "Not found")
        except Exception as e:
            return v_fail(step, expected, "Error", e)

    def _check_9091_section(self):
        step = "99-91% Match Section"
        expected = "Section visible"
        try:
            sec = self.page.locator("#fdq-sec-9095")
            if sec.count() > 0:
                text = sec.inner_text().strip()
                return v_pass(step, expected, text[:80])
            return v_fail(step, expected, "Not found")
        except Exception as e:
            return v_fail(step, expected, "Error", e)

    def _check_8090_section(self):
        step = "90-80% Match Section"
        expected = "Section visible or No products found"
        try:
            sec = self.page.locator("#fdq-sec-8090")
            if sec.count() > 0:
                text = sec.inner_text().strip()
                return v_pass(step, expected, text[:80])
            return v_fail(step, expected, "Not found")
        except Exception as e:
            return v_fail(step, expected, "Error", e)

    def _check_retake_btn(self):
        step = "Retake Quiz Button"
        expected = "a.fdq-retake-btn visible"
        try:
            retake = self.page.locator("a.fdq-retake-btn")
            if retake.count() > 0 and retake.is_visible():
                return v_pass(step, expected, "Visible")
            return v_fail(step, expected, "Not found")
        except Exception as e:
            return v_fail(step, expected, "Error", e)

    # ---------------------------
    # Share Product
    # ---------------------------
    def share_product(self):
        step = "Share Modal"
        expected = "Share popup opens, link copied, modal closed"
        try:
            share_btn = self.page.locator("#fdq-sec-100").get_by_role("button", name="Share").first
            if share_btn.count() == 0:
                return v_fail(step, expected, "Share button not found"), "N/A"
            share_btn.click()

            popup = self.page.locator("section.fci-share-popup")
            popup.wait_for(state="visible", timeout=5000)

            link = popup.locator(".coupon_text").inner_text().strip()
            popup.locator(".coupon_copy").click()
            self.page.wait_for_timeout(500)

            # Close via X button
            close_btn = self.page.locator("div.modal_close_btn")
            close_btn.wait_for(state="visible", timeout=3000)
            close_btn.click()
            self.page.wait_for_timeout(500)

            logger.info(f"Share link: {link}")
            return v_pass(step, expected, f"Link: {link[:60]}"), link
        except Exception as e:
            return v_fail(step, expected, "Error", e), "N/A"

    # ---------------------------
    # Retake Quiz
    # ---------------------------
    def retake_quiz(self):
        try:
            retake = self.page.locator("a.fdq-retake-btn")
            retake.wait_for(state="visible", timeout=10000)
            retake.click()
            # Wait for quiz page to reload — don't use expect_navigation (can close context)
            self.page.wait_for_url("**/engagement-ring-quiz", timeout=15000)
            self.page.wait_for_timeout(2000)
            logger.info("Retake clicked, back on quiz page")
        except Exception as e:
            logger.warning(f"Retake failed, navigating directly: {e}")
            self.page.goto(self.URL)
            self.page.wait_for_timeout(3000)

    # ---------------------------
    # Run Full Quiz Flow
    # ---------------------------
    def run_quiz_flow(self, answers):
        logger.info(f"Running quiz: {answers}")
        validations = []

        # Answer each question
        for q_no, option in enumerate(answers, start=1):
            self.select_option(q_no, option)
            self.page.wait_for_timeout(800)
            validations.append(self.validate_banner(q_no, option))
            self.click_continue(q_no)

        # Results page validations
        validations.append(self._check_results_header())
        validations.append(self._check_summary())
        validations.append(self._check_100_match_header())

        name_v, product_name = self._get_product_name()
        validations.append(name_v)

        price_v, price = self._get_price()
        validations.append(price_v)

        validations.append(self._check_match_score())
        validations.append(self._check_trust_badges())

        share_v, share_link = self.share_product()
        validations.append(share_v)

        validations.append(self._check_9091_section())
        validations.append(self._check_8090_section())
        validations.append(self._check_retake_btn())

        # Overall status
        overall = "PASS" if all(v["status"] == "PASS" for v in validations) else "FAIL"
        logger.info(f"Overall: {overall} | Product: {product_name} | Price: {price}")

        self.retake_quiz()
        return product_name, price, overall, validations
