import pytest
from FD.pages.fci_quiz.quiz_page import QuizPage
from FD.utils.quiz_combinations import combinations
from FD.utils.excel_reporter import ExcelReporter

report = ExcelReporter()


class TestQuizFlow:

    @pytest.mark.parametrize("answers", combinations)
    def test_quiz(self, page, answers):
        quiz = QuizPage(page)
        browser = page.context.browser.browser_type.name

        quiz.open_quiz()

        product, price, overall, validations = quiz.run_quiz_flow(answers)

        report.add_row(browser, answers, validations, overall=overall, product=product, price=price)

        # Log result but don't hard-fail — keep running all 1215
        if overall == "FAIL":
            failed_steps = [v["step"] for v in validations if v["status"] == "FAIL"]
            pytest.fail(f"answers={answers} | Product={product} | Failed steps: {failed_steps}", pytrace=False)


def teardown_module():
    report.export()
