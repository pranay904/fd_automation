import re
from utils.cyo_contract import CYOContract

class CYONormalizer:

    @staticmethod
    def normalize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip().lower()

    # ---------- SETTING ----------
    @staticmethod
    def normalize_setting_name(text: str) -> str:
        t = CYONormalizer.normalize_text(text)

        for w in CYOContract.SETTING_IGNORE_WORDS:
            t = t.replace(w, "")

        for s in CYOContract.STYLE_WORDS:
            t = t.replace(s, "")

        return t.strip().title()

    @staticmethod
    def extract_metal(text: str) -> str:
        t = CYONormalizer.normalize_text(text)
        for m in CYOContract.METAL_COLORS:
            if m in t:
                return m
        return ""

    # ---------- DIAMOND ----------
    @staticmethod
    def parse_diamond_title(text: str) -> dict:
        t = CYONormalizer.normalize_text(text)

        carat = re.search(r"\d+(\.\d+)?", t).group()
        shape = next(s for s in CYOContract.SHAPES if s in t)

        return {"carat": carat, "shape": shape}

    @staticmethod
    def parse_4cs(text: str) -> dict:
        raw = CYONormalizer.normalize_text(text)

        color = next(c for c in CYOContract.COLOR_VALUES if c.lower() in raw)
        clarity = next(c for c in CYOContract.CLARITY_VALUES if c.lower() in raw)

        cut_raw = re.search(r"(excellent|very good|good|fair|ex|vg)", raw).group()
        cut = CYOContract.CUT_MAP[cut_raw]

        return {"color": color, "clarity": clarity, "cut": cut}
