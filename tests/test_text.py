import pytest
from plotcraft.types import (
    TextRole,
    AnchorName,
    Point,
    Size,
    BBox,
    TextStyle,
    TEXT_STYLE_DEFAULTS,
)
from plotcraft.text import measure_text, wrap_text, ARIAL_NORMAL, ARIAL_BOLD


class TestFontMetrics:
    """Test FontMetrics character width measurements."""

    def test_w_wider_than_i(self):
        """Measure 'W' vs 'i' at same font size."""
        font_size = 24.0

        # 'W' should be much wider than 'i'
        w_width = ARIAL_NORMAL.char_width("W", font_size)
        i_width = ARIAL_NORMAL.char_width("i", font_size)

        assert w_width > i_width
        # W is 0.94, i is 0.22 — roughly 4x wider
        assert w_width / i_width > 3.0

    def test_line_measurement_known_string(self):
        """Test 'Hello' produces expected width within 10% tolerance."""
        font_size = 14.0

        # 'Hello' = H(0.72) + e(0.56) + l(0.22) + l(0.22) + o(0.56) = 2.28
        expected_width = (0.72 + 0.56 + 0.22 + 0.22 + 0.56) * font_size
        actual_width = ARIAL_NORMAL.measure_line("Hello", font_size)

        assert abs(actual_width - expected_width) < expected_width * 0.1


class TestTextMeasurement:
    """Test the measure_text function."""

    def test_empty_string(self):
        """Empty string returns Size with width=0, height=one line height."""
        style = TextStyle("Arial", 14.0, "normal", 1.4)
        size = measure_text("", style)

        assert size.width == 0.0
        # Height should be one line height
        expected_height = 14.0 * 1.4
        assert size.height == pytest.approx(expected_height)

    def test_single_line(self):
        """Single line text returns correct dimensions."""
        style = TextStyle("Arial", 14.0, "normal", 1.4)
        size = measure_text("Hello", style)

        assert size.width > 0.0
        assert size.height == pytest.approx(14.0 * 1.4)

    def test_multiline(self):
        """Multiline text (explicit \\n) has height of multiple lines."""
        style = TextStyle("Arial", 14.0, "normal", 1.4)
        size = measure_text("Hello\nWorld", style)

        # Should have 2 lines
        expected_height = 2 * (14.0 * 1.4)
        assert size.height == pytest.approx(expected_height)

    def test_word_wrap(self):
        """Long string wraps, all lines <= max_width."""
        style = TextStyle("Arial", 12.0, "normal", 1.3)
        max_width = 100.0

        long_text = "This is a long string that should wrap to multiple lines"
        size = measure_text(long_text, style, max_width=max_width)

        # All lines should be <= max_width
        assert size.width <= max_width
        # Should have multiple lines
        assert size.height > 12.0 * 1.3

    def test_bold_wider_than_normal(self):
        """Same string, bold > normal."""
        text = "Hello"
        style_normal = TextStyle("Arial", 14.0, "normal", 1.4)
        style_bold = TextStyle("Arial", 14.0, "bold", 1.4)

        size_normal = measure_text(text, style_normal)
        size_bold = measure_text(text, style_bold)

        assert size_bold.width > size_normal.width


class TestTextRoles:
    """Test TextRole defaults."""

    def test_all_text_roles_have_defaults(self):
        """Every TextRole has an entry in TEXT_STYLE_DEFAULTS."""
        for role in TextRole:
            assert role in TEXT_STYLE_DEFAULTS
            style = TEXT_STYLE_DEFAULTS[role]
            assert isinstance(style, TextStyle)
            assert isinstance(style.font_family, str) and len(style.font_family) > 0
            assert style.font_size > 0
            assert style.font_weight in ("normal", "bold", "600")
            assert style.line_height > 0


class TestBBoxAnchors:
    """Test BBox.anchor() method for all 9 anchors."""

    def test_bbox_anchors(self):
        """Test that BBox.anchor returns correct points for all 9 anchors."""
        bbox = BBox(x=10.0, y=20.0, width=100.0, height=50.0)

        # TOP_LEFT = (x, y)
        assert bbox.anchor(AnchorName.TOP_LEFT) == Point(10.0, 20.0)

        # TOP_CENTER = (x + w/2, y)
        assert bbox.anchor(AnchorName.TOP_CENTER) == Point(60.0, 20.0)

        # TOP_RIGHT = (x+w, y)
        assert bbox.anchor(AnchorName.TOP_RIGHT) == Point(110.0, 20.0)

        # LEFT_CENTER = (x, y+h/2)
        assert bbox.anchor(AnchorName.LEFT_CENTER) == Point(10.0, 45.0)

        # CENTER = center
        assert bbox.anchor(AnchorName.CENTER) == Point(60.0, 45.0)

        # RIGHT_CENTER = (x+w, y+h/2)
        assert bbox.anchor(AnchorName.RIGHT_CENTER) == Point(110.0, 45.0)

        # BOTTOM_LEFT = (x, y+h)
        assert bbox.anchor(AnchorName.BOTTOM_LEFT) == Point(10.0, 70.0)

        # BOTTOM_CENTER = (x+w/2, y+h)
        assert bbox.anchor(AnchorName.BOTTOM_CENTER) == Point(60.0, 70.0)

        # BOTTOM_RIGHT = (x+w, y+h)
        assert bbox.anchor(AnchorName.BOTTOM_RIGHT) == Point(110.0, 70.0)


class TestImmutability:
    """Test that frozen dataclasses are immutable."""

    def test_point_frozen(self):
        """Point attributes can't be mutated."""
        point = Point(1.0, 2.0)
        with pytest.raises(Exception):  # FrozenInstanceError
            point.x = 3.0

    def test_size_frozen(self):
        """Size attributes can't be mutated."""
        size = Size(10.0, 20.0)
        with pytest.raises(Exception):  # FrozenInstanceError
            size.width = 30.0


class TestWrapText:
    """Test the wrap_text function."""

    def test_wrap_text_basic(self):
        """Basic word wrap test."""
        style = TextStyle("Arial", 12.0, "normal", 1.3)
        text = "This is a test"
        max_width = 50.0

        lines = wrap_text(text, style, max_width)

        # All lines should fit within max_width
        for line in lines:
            width = ARIAL_NORMAL.measure_line(line, style.font_size)
            assert width <= max_width

    def test_wrap_text_respects_explicit_newlines(self):
        """Explicit newlines are preserved."""
        style = TextStyle("Arial", 12.0, "normal", 1.3)
        text = "Hello\nWorld"
        max_width = 500.0

        lines = wrap_text(text, style, max_width)

        assert len(lines) >= 2
        assert lines[0] == "Hello"
        assert lines[1] == "World"
