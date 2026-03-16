import pandas as pd
import os
from datetime import datetime


class ExcelReporter:

    def __init__(self):
        self.rows = []

    def add_row(self, browser, answers, validations):
        """
        validations: list of dicts with keys:
          step, expected, actual, status (PASS/FAIL)
        """
        base = {
            "Browser":   browser,
            "Q1": answers[0], "Q2": answers[1], "Q3": answers[2],
            "Q4": answers[3], "Q5": answers[4], "Q6": answers[5],
        }
        for v in validations:
            row = dict(base)
            row["Step"]     = v.get("step", "")
            row["Expected"] = v.get("expected", "")
            row["Actual"]   = v.get("actual", "")
            row["Status"]   = v.get("status", "")
            row["Error"]    = v.get("error", "")
            self.rows.append(row)

    def export(self):
        out_dir = os.path.join("FD", "reports", "excel")
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(out_dir, f"quiz_results_{ts}.xlsx")

        df = pd.DataFrame(self.rows, columns=[
            "Browser", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6",
            "Step", "Expected", "Actual", "Status", "Error"
        ])

        # Color coding
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Results")
            wb = writer.book
            ws = writer.sheets["Results"]

            from openpyxl.styles import PatternFill, Font
            green = PatternFill("solid", fgColor="C6EFCE")
            red   = PatternFill("solid", fgColor="FFC7CE")
            bold  = Font(bold=True)

            # Header bold
            for cell in ws[1]:
                cell.font = bold

            # Color rows by status
            status_col = df.columns.get_loc("Status") + 1
            for row_idx in range(2, len(df) + 2):
                status_cell = ws.cell(row=row_idx, column=status_col)
                fill = green if status_cell.value == "PASS" else red
                for col_idx in range(1, len(df.columns) + 1):
                    ws.cell(row=row_idx, column=col_idx).fill = fill

            # Auto width
            for col in ws.columns:
                max_len = max(len(str(c.value or "")) for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 60)

        print(f"[Report saved] {path}")
        return path
