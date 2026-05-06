import re
from FD.utils.cyo_contract import CYOContract


class CYONormalizer:

    @staticmethod
    def normalize_text(text: str) -> str:
        text = text.lower().strip()

        text = text.replace("carat", "ct")
        text = re.sub(r"\bct\.?\b", "ct", text)

        # REMOVE NOISE
        text = text.replace("lab grown", "")
        text = text.replace("diamond", "")

        # FIX 1.06ct → 1.06 ct
        text = re.sub(r"(\d)(ct)", r"\1 ct", text)

        text = re.sub(r"[^\w\s.]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def normalize_cut(value: str) -> str:
        value = value.lower().strip()

        mapping = {
            "fr": "fair",
            "fair": "fair",
            "gd": "good",
            "good": "good",
            "vg": "very good",
            "very good": "very good",
            "ex": "excellent",
            "excellent": "excellent",
            "id": "ideal",
            "ideal": "ideal"
        }

        return mapping.get(value, value)

    @staticmethod
    def parse_diamond_title(text: str) -> dict:
        t = CYONormalizer.normalize_text(text)

        carat_match = re.search(r"\d+(\.\d+)?", t)
        carat = carat_match.group() if carat_match else ""

        shape = next((s for s in CYOContract.SHAPES if s in t), "")

        return {
            "carat": carat,
            "shape": shape
        }

    @staticmethod
    def parse_4cs(text: str) -> dict:
        raw = CYONormalizer.normalize_text(text)

        color = next((c for c in CYOContract.COLOR_VALUES if c.lower() in raw), "")
        clarity = next((c for c in CYOContract.CLARITY_VALUES if c.lower() in raw), "")

        cut_match = re.search(
            r"\b(excellent|very good|good|fair|ideal|ex|vg|gd|fr|id)\b",
            raw
        )

        cut_raw = cut_match.group() if cut_match else ""
        cut = CYONormalizer.normalize_cut(cut_raw)

        return {
            "color": color,
            "clarity": clarity,
            "cut": cut
        }