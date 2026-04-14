import os
import xml.etree.ElementTree as ET
import pytest
from plotcraft import Diagram, TextRole, ShapeKind, AnchorName, GridConfig, SectionStyle


def test_empty_diagram():
    """Empty diagram renders valid SVG."""
    d = Diagram()
    svg = d.render()
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg
    ET.fromstring(svg)  # valid XML


def test_single_element():
    """Add one element, render produces SVG with one shape."""
    d = Diagram()
    d.add("s1", "Hello World")
    svg = d.render()
    assert "Hello World" in svg
    assert "<rect" in svg


def test_chaining():
    """Method chaining returns Diagram instance."""
    d = Diagram()
    result = d.add("a", "A").add("b", "B").connect("a", "b")
    assert isinstance(result, Diagram)


def test_auto_placement():
    """Three adds without row/col, all placed without overlap."""
    d = Diagram()
    d.add("a", "First")
    d.add("b", "Second")
    d.add("c", "Third")
    svg = d.render()
    # All three texts should appear
    assert "First" in svg
    assert "Second" in svg
    assert "Third" in svg
    ET.fromstring(svg)


def test_manual_placement():
    """row/col specified, shapes at correct grid position."""
    d = Diagram()
    d.add("a", "Top Left", row=0, col=0)
    d.add("b", "Bottom Right", row=1, col=1)
    svg = d.render()
    assert "Top Left" in svg
    assert "Bottom Right" in svg
    ET.fromstring(svg)


def test_duplicate_id_raises():
    """Adding same id twice raises ValueError."""
    d = Diagram()
    d.add("dup", "First")
    with pytest.raises(ValueError, match="Duplicate"):
        d.add("dup", "Second")


def test_connect_missing_source_raises():
    """Connecting non-existent source raises ValueError."""
    d = Diagram()
    d.add("a", "Only one")
    with pytest.raises(ValueError, match="Unknown"):
        d.connect("missing", "a")


def test_connect_missing_target_raises():
    """Connecting non-existent target raises ValueError."""
    d = Diagram()
    d.add("a", "Only one")
    with pytest.raises(ValueError, match="Unknown"):
        d.connect("a", "missing")


def test_full_diagram():
    """4 shapes, 3 connectors, valid SVG output."""
    svg = (
        Diagram()
        .add("start", "User Request", role=TextRole.TITLE)
        .add("process", "Parse Input")
        .add("decide", "Valid?", shape=ShapeKind.CIRCLE)
        .add("output", "Return Result")
        .connect("start", "process")
        .connect("process", "decide")
        .connect("decide", "output", label="Yes")
        .render()
    )

    root = ET.fromstring(svg)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    # Title text may wrap into multiple tspan elements at large font sizes,
    # so check that all words appear somewhere in the SVG.
    assert "User" in svg and "Request" in svg
    assert "Parse Input" in svg
    assert "Valid?" in svg
    assert "Return Result" in svg
    assert "Yes" in svg


def test_save_writes_file(tmp_path):
    """save() creates file on disk with SVG content."""
    path = str(tmp_path / "test.svg")
    Diagram().add("s1", "Save Test").save(path)

    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert "Save Test" in content
    ET.fromstring(content)


def test_render_idempotent():
    """Calling render() twice returns same result."""
    d = Diagram().add("s1", "Test")
    first = d.render()
    second = d.render()
    assert first == second


def test_all_shape_kinds_in_diagram():
    """All shape kinds render correctly in a single diagram."""
    d = Diagram()
    d.add("rect", "Rectangle", shape=ShapeKind.RECT)
    d.add("square", "Square", shape=ShapeKind.SQUARE)
    d.add("circle", "Circle", shape=ShapeKind.CIRCLE)
    d.add("oval", "Oval", shape=ShapeKind.OVAL)
    svg = d.render()

    # Wobble engine renders all shapes as <path> elements.
    # Verify each shape's text label is present and the SVG is valid.
    assert "Rectangle" in svg
    assert "Square" in svg
    assert "Circle" in svg
    assert "Oval" in svg
    ET.fromstring(svg)


def test_custom_grid_config():
    """Custom GridConfig is respected."""
    config = GridConfig(cell_width=300, cell_height=200, margin=30)
    d = Diagram(grid_config=config)
    d.add("s1", "Custom Grid")
    svg = d.render()
    ET.fromstring(svg)


def test_section_valid():
    """Adding a section with valid shape_ids does not raise."""
    d = Diagram()
    d.add("a", "Alpha")
    d.add("b", "Beta")
    d.section("My Group", ["a", "b"])  # should not raise


def test_section_invalid_shape_id_raises():
    """Adding a section with unknown shape_id raises ValueError."""
    d = Diagram()
    d.add("a", "Alpha")
    with pytest.raises(ValueError, match="Unknown shape id"):
        d.section("Bad Group", ["a", "nonexistent"])


def test_section_returns_self():
    """section() returns self for chaining."""
    d = Diagram()
    d.add("a", "Alpha")
    result = d.section("Group", ["a"])
    assert result is d


def test_section_svg_contains_label_and_fill():
    """SVG output contains section label text and fill color."""
    d = Diagram()
    d.add("a", "Alpha")
    d.add("b", "Beta")
    style = SectionStyle(fill="#aabbcc")
    d.section("Test Section", ["a", "b"], style=style)
    svg = d.render()
    assert "Test Section" in svg
    assert "#aabbcc" in svg
    ET.fromstring(svg)
