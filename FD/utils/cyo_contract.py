class CYOContract:
    SETTING_IGNORE_WORDS = ["mm","lab","diamond","ring","earring","pendant"]
    STYLE_WORDS = ["solitaire","halo","hidden halo","side stone","three stone","vintage"]
    METAL_COLORS = ["white","yellow","rose"]
    DEFAULT_METAL = "10kt white gold"

    SHAPES = ["round","oval","pear","cushion","princess","radiant","emerald","heart","asscher","marquise"]
    COLOR_VALUES = ["D","E","F","G","H","I","J","K","L","M"]
    CLARITY_VALUES = ["FL","IF","VVS1","VVS2","VS1","VS2","SI1","SI2","I1"]

    CUT_MAP = {
        "excellent": "EX", "very good": "VG", "good": "GD", "fair": "FR",
        "ex": "EX", "vg": "VG"
    }

    ROUND_BASE = 10
