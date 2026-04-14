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


def measure_text(text: str, style: TextStyle, max_width: float | None = None) -> Size:
    """Measure text, optionally word-wrapping at max_width."""
    # Get the right FontMetrics based on style.font_weight
    if style.font_weight == "bold":
        metrics = ARIAL_BOLD
    else:
        metrics = ARIAL_NORMAL

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
    # Get the right FontMetrics based on style.font_weight
    if style.font_weight == "bold":
        metrics = ARIAL_BOLD
    else:
        metrics = ARIAL_NORMAL

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
