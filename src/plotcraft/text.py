from plotcraft.types import TextStyle, Size


class FontMetrics:
    """Per-character width ratios for a font family+weight."""

    def __init__(
        self,
        char_widths: dict[str, float],
        default_width: float = 0.6,
        cap_height_ratio: float = 0.72,
        descent_ratio: float = 0.25,
    ):
        self._char_widths = char_widths
        self._default_width = default_width
        self.cap_height_ratio = cap_height_ratio
        self.descent_ratio = descent_ratio

    def char_width(self, ch: str, font_size: float) -> float:
        return self._char_widths.get(ch, self._default_width) * font_size

    def measure_line(self, text: str, font_size: float) -> float:
        return sum(self.char_width(ch, font_size) for ch in text)

    def line_height(self, font_size: float, line_height_mult: float) -> float:
        return font_size * line_height_mult


# Arial character widths (as fraction of font_size)
_ARIAL_NORMAL_WIDTHS = {
    # Lowercase
    "a": 0.56,
    "b": 0.56,
    "c": 0.50,
    "d": 0.56,
    "e": 0.56,
    "f": 0.28,
    "g": 0.56,
    "h": 0.56,
    "i": 0.22,
    "j": 0.22,
    "k": 0.50,
    "l": 0.22,
    "m": 0.83,
    "n": 0.56,
    "o": 0.56,
    "p": 0.56,
    "q": 0.56,
    "r": 0.33,
    "s": 0.50,
    "t": 0.28,
    "u": 0.56,
    "v": 0.50,
    "w": 0.72,
    "x": 0.50,
    "y": 0.50,
    "z": 0.50,
    # Uppercase
    "A": 0.67,
    "B": 0.67,
    "C": 0.72,
    "D": 0.72,
    "E": 0.67,
    "F": 0.61,
    "G": 0.78,
    "H": 0.72,
    "I": 0.28,
    "J": 0.50,
    "K": 0.67,
    "L": 0.56,
    "M": 0.83,
    "N": 0.72,
    "O": 0.78,
    "P": 0.67,
    "Q": 0.78,
    "R": 0.72,
    "S": 0.67,
    "T": 0.61,
    "U": 0.72,
    "V": 0.67,
    "W": 0.94,
    "X": 0.67,
    "Y": 0.67,
    "Z": 0.61,
    # Digits
    "0": 0.56,
    "1": 0.56,
    "2": 0.56,
    "3": 0.56,
    "4": 0.56,
    "5": 0.56,
    "6": 0.56,
    "7": 0.56,
    "8": 0.56,
    "9": 0.56,
    # Punctuation/symbols
    " ": 0.28,
    "!": 0.28,
    '"': 0.35,
    "#": 0.56,
    "$": 0.56,
    "%": 0.89,
    "&": 0.67,
    "'": 0.19,
    "(": 0.33,
    ")": 0.33,
    "*": 0.39,
    "+": 0.58,
    ",": 0.28,
    "-": 0.33,
    ".": 0.28,
    "/": 0.28,
    ":": 0.28,
    ";": 0.28,
    "<": 0.58,
    "=": 0.58,
    ">": 0.58,
    "?": 0.56,
    "@": 1.02,
    "[": 0.28,
    "\\": 0.28,
    "]": 0.28,
    "^": 0.47,
    "_": 0.56,
    "`": 0.33,
    "{": 0.33,
    "|": 0.26,
    "}": 0.33,
    "~": 0.58,
}

# Arial Bold: multiply each ratio by 1.08 (8% wider)
_ARIAL_BOLD_WIDTHS = {ch: width * 1.08 for ch, width in _ARIAL_NORMAL_WIDTHS.items()}

ARIAL_NORMAL = FontMetrics(_ARIAL_NORMAL_WIDTHS)
ARIAL_BOLD = FontMetrics(_ARIAL_BOLD_WIDTHS)


# Caveat character widths (as fraction of font_size)
# Handwriting font — generally wider than Arial, especially lowercase
_CAVEAT_NORMAL_WIDTHS = {
    # Lowercase
    "a": 0.52, "b": 0.54, "c": 0.48, "d": 0.54, "e": 0.52,
    "f": 0.32, "g": 0.54, "h": 0.55, "i": 0.26, "j": 0.26,
    "k": 0.52, "l": 0.26, "m": 0.82, "n": 0.55, "o": 0.54,
    "p": 0.54, "q": 0.54, "r": 0.38, "s": 0.48, "t": 0.34,
    "u": 0.55, "v": 0.52, "w": 0.74, "x": 0.52, "y": 0.52,
    "z": 0.50,
    # Uppercase
    "A": 0.68, "B": 0.66, "C": 0.70, "D": 0.72, "E": 0.65,
    "F": 0.62, "G": 0.76, "H": 0.72, "I": 0.32, "J": 0.52,
    "K": 0.68, "L": 0.58, "M": 0.82, "N": 0.72, "O": 0.76,
    "P": 0.66, "Q": 0.76, "R": 0.70, "S": 0.65, "T": 0.64,
    "U": 0.72, "V": 0.68, "W": 0.90, "X": 0.68, "Y": 0.68,
    "Z": 0.64,
    # Digits
    "0": 0.56, "1": 0.46, "2": 0.54, "3": 0.54, "4": 0.56,
    "5": 0.54, "6": 0.56, "7": 0.52, "8": 0.56, "9": 0.56,
    # Punctuation/symbols
    " ": 0.30, "!": 0.30, '"': 0.38, "#": 0.58, "$": 0.56,
    "%": 0.84, "&": 0.68, "'": 0.22, "(": 0.34, ")": 0.34,
    "*": 0.42, "+": 0.58, ",": 0.30, "-": 0.36, ".": 0.30,
    "/": 0.32, ":": 0.30, ";": 0.30, "?": 0.54, "@": 0.96,
    "_": 0.56,
}

# Caveat Bold: multiply by 1.06 (6% wider)
_CAVEAT_BOLD_WIDTHS = {ch: width * 1.06 for ch, width in _CAVEAT_NORMAL_WIDTHS.items()}

CAVEAT_NORMAL = FontMetrics(
    _CAVEAT_NORMAL_WIDTHS,
    default_width=0.55,
    cap_height_ratio=0.70,
    descent_ratio=0.28,
)
CAVEAT_BOLD = FontMetrics(
    _CAVEAT_BOLD_WIDTHS,
    default_width=0.55 * 1.06,
    cap_height_ratio=0.70,
    descent_ratio=0.28,
)


# Patrick Hand character widths (as fraction of font_size)
# Slightly wider than Arial overall, more uniform (handwriting)
_PATRICK_HAND_NORMAL_WIDTHS = {
    # Lowercase
    "a": 0.58, "b": 0.58, "c": 0.54, "d": 0.58, "e": 0.58,
    "f": 0.34, "g": 0.58, "h": 0.58, "i": 0.28, "j": 0.28,
    "k": 0.54, "l": 0.28, "m": 0.86, "n": 0.58, "o": 0.58,
    "p": 0.58, "q": 0.58, "r": 0.38, "s": 0.52, "t": 0.34,
    "u": 0.58, "v": 0.54, "w": 0.76, "x": 0.54, "y": 0.54,
    "z": 0.52,
    # Uppercase
    "A": 0.68, "B": 0.68, "C": 0.72, "D": 0.74, "E": 0.68,
    "F": 0.62, "G": 0.78, "H": 0.74, "I": 0.32, "J": 0.52,
    "K": 0.68, "L": 0.58, "M": 0.84, "N": 0.74, "O": 0.78,
    "P": 0.68, "Q": 0.78, "R": 0.72, "S": 0.68, "T": 0.64,
    "U": 0.74, "V": 0.68, "W": 0.92, "X": 0.68, "Y": 0.68,
    "Z": 0.64,
    # Digits
    "0": 0.58, "1": 0.50, "2": 0.56, "3": 0.56, "4": 0.58,
    "5": 0.56, "6": 0.58, "7": 0.54, "8": 0.58, "9": 0.58,
    # Punctuation/symbols
    " ": 0.30, "!": 0.32, '"': 0.40, "#": 0.60, "$": 0.58,
    "%": 0.88, "&": 0.70, "'": 0.24, "(": 0.36, ")": 0.36,
    "*": 0.44, "+": 0.60, ",": 0.30, "-": 0.36, ".": 0.30,
    "/": 0.34, ":": 0.30, ";": 0.30, "?": 0.56, "@": 1.00,
    "_": 0.58,
}

PATRICK_HAND_NORMAL = FontMetrics(
    _PATRICK_HAND_NORMAL_WIDTHS,
    default_width=0.58,
    cap_height_ratio=0.73,
    descent_ratio=0.25,
)


# Indie Flower character widths (as fraction of font_size)
# Widest and most irregular of the handwriting fonts
_INDIE_FLOWER_NORMAL_WIDTHS = {
    # Lowercase — more variable widths
    "a": 0.60, "b": 0.62, "c": 0.56, "d": 0.62, "e": 0.60,
    "f": 0.36, "g": 0.62, "h": 0.62, "i": 0.32, "j": 0.30,
    "k": 0.58, "l": 0.32, "m": 0.90, "n": 0.62, "o": 0.62,
    "p": 0.62, "q": 0.62, "r": 0.42, "s": 0.54, "t": 0.38,
    "u": 0.62, "v": 0.58, "w": 0.82, "x": 0.58, "y": 0.58,
    "z": 0.54,
    # Uppercase
    "A": 0.72, "B": 0.70, "C": 0.74, "D": 0.76, "E": 0.70,
    "F": 0.66, "G": 0.80, "H": 0.76, "I": 0.36, "J": 0.56,
    "K": 0.72, "L": 0.62, "M": 0.88, "N": 0.76, "O": 0.82,
    "P": 0.70, "Q": 0.82, "R": 0.76, "S": 0.70, "T": 0.68,
    "U": 0.76, "V": 0.72, "W": 0.96, "X": 0.72, "Y": 0.72,
    "Z": 0.68,
    # Digits
    "0": 0.62, "1": 0.52, "2": 0.60, "3": 0.60, "4": 0.62,
    "5": 0.60, "6": 0.62, "7": 0.58, "8": 0.62, "9": 0.62,
    # Punctuation/symbols
    " ": 0.32, "!": 0.34, '"': 0.44, "#": 0.64, "$": 0.62,
    "%": 0.92, "&": 0.74, "'": 0.26, "(": 0.38, ")": 0.38,
    "*": 0.48, "+": 0.64, ",": 0.32, "-": 0.40, ".": 0.32,
    "/": 0.36, ":": 0.32, ";": 0.32, "?": 0.60, "@": 1.04,
    "_": 0.62,
}

INDIE_FLOWER_NORMAL = FontMetrics(
    _INDIE_FLOWER_NORMAL_WIDTHS,
    default_width=0.62,
    cap_height_ratio=0.68,
    descent_ratio=0.30,
)


# Metrics lookup table keyed by (font_family_lower, weight)
_METRICS_MAP: dict[tuple[str, str], FontMetrics] = {
    ("arial", "normal"): ARIAL_NORMAL,
    ("arial", "bold"): ARIAL_BOLD,
    ("caveat", "normal"): CAVEAT_NORMAL,
    ("caveat", "bold"): CAVEAT_BOLD,
    ("caveat", "600"): CAVEAT_BOLD,  # semi-bold maps to bold metrics
    ("patrick hand", "normal"): PATRICK_HAND_NORMAL,
    ("indie flower", "normal"): INDIE_FLOWER_NORMAL,
}


def _get_metrics(style: TextStyle) -> FontMetrics:
    """Look up FontMetrics for a TextStyle, with fallbacks."""
    family = style.font_family.lower()
    weight = style.font_weight
    # Exact match
    metrics = _METRICS_MAP.get((family, weight))
    if metrics is not None:
        return metrics
    # Fall back to normal weight for this family
    metrics = _METRICS_MAP.get((family, "normal"))
    if metrics is not None:
        return metrics
    # Final fallback: Arial Normal
    return ARIAL_NORMAL


def measure_text(text: str, style: TextStyle, max_width: float | None = None) -> Size:
    """Measure text, optionally word-wrapping at max_width."""
    metrics = _get_metrics(style)

    # If max_width, wrap text first
    if max_width is not None:
        lines = wrap_text(text, style, max_width)
    else:
        # Split on explicit \n for line breaks
        lines = text.split("\n")

    # Calculate width and height
    max_line_width = 0.0
    for line in lines:
        line_width = metrics.measure_line(line, style.font_size)
        max_line_width = max(max_line_width, line_width)

    line_height = metrics.line_height(style.font_size, style.line_height)
    total_height = len(lines) * line_height

    return Size(max_line_width, total_height)


def wrap_text(text: str, style: TextStyle, max_width: float) -> list[str]:
    """Greedy word-wrap. Returns list of lines."""
    metrics = _get_metrics(style)

    if not text:
        return [""]

    lines: list[str] = []
    # Handle explicit line breaks first
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split(" ")
        current_line = ""

        for word in words:
            test_line = (
                current_line + " " + word if current_line else word
            )
            test_width = metrics.measure_line(test_line, style.font_size)

            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        lines.append(current_line)

    return lines
