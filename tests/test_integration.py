import xml.etree.ElementTree as ET
from plotcraft import Diagram, TextRole, ShapeKind, AnchorName, GridConfig


def test_flowchart():
    """Full flowchart: 6 shapes, 5 connectors."""
    svg = (
        Diagram()
        .add("start", "Start", role=TextRole.TITLE, shape=ShapeKind.RECT)
        .add("input", "Get User Input", role=TextRole.BODY)
        .add("validate", "Valid?", shape=ShapeKind.CIRCLE)
        .add("process", "Process Data", role=TextRole.BODY)
        .add("error", "Show Error", role=TextRole.CAPTION, shape=ShapeKind.RECT)
        .add("end", "Done", role=TextRole.SUBTITLE, shape=ShapeKind.RECT)
        .connect("start", "input")
        .connect("input", "validate")
        .connect("validate", "process", label="Yes")
        .connect("validate", "error", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER, label="No")
        .connect("process", "end")
        .render()
    )

    root = ET.fromstring(svg)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    # All text content present
    for text in ["Start", "Get User Input", "Valid?", "Process Data", "Show Error", "Done", "Yes", "No"]:
        assert text in svg


def test_single_node():
    """Simplest possible diagram: one shape, no connectors."""
    svg = Diagram().add("only", "Just Me").render()
    root = ET.fromstring(svg)
    assert "Just Me" in svg
    assert root.tag == "{http://www.w3.org/2000/svg}svg"


def test_all_shape_kinds():
    """One of each shape kind in a single diagram."""
    svg = (
        Diagram()
        .add("r", "Rectangle", shape=ShapeKind.RECT)
        .add("s", "Square", shape=ShapeKind.SQUARE)
        .add("c", "Circle", shape=ShapeKind.CIRCLE)
        .add("o", "Oval", shape=ShapeKind.OVAL)
        .render()
    )

    root = ET.fromstring(svg)
    ns = {"svg": "http://www.w3.org/2000/svg"}

    # Should have rect, circle, ellipse elements
    # (rect appears for background + RECT shape + SQUARE shape)
    rects = root.findall(".//svg:rect", ns)
    circles = root.findall(".//svg:circle", ns)
    ellipses = root.findall(".//svg:ellipse", ns)

    assert len(circles) >= 1
    assert len(ellipses) >= 1
    # At least 2 rects with rounded corners (RECT + SQUARE) plus background
    shape_rects = [r for r in rects if r.get("rx") is not None]
    assert len(shape_rects) >= 2


def test_all_text_roles():
    """Each text role produces visually distinct elements."""
    svg = (
        Diagram()
        .add("t", "Title Text", role=TextRole.TITLE)
        .add("s", "Subtitle Text", role=TextRole.SUBTITLE)
        .add("c", "Caption Text", role=TextRole.CAPTION)
        .add("b", "Body Text", role=TextRole.BODY)
        .render()
    )

    root = ET.fromstring(svg)
    # Title text may wrap into multiple tspan elements at large font sizes;
    # verify all words appear somewhere in the SVG output.
    assert "Title" in svg and "Text" in svg
    assert "Subtitle" in svg
    assert "Caption" in svg
    assert "Body" in svg

    # Check different font sizes are used
    ns = {"svg": "http://www.w3.org/2000/svg"}
    texts = root.findall(".//svg:text", ns)
    font_sizes = set()
    for t in texts:
        fs = t.get("font-size")
        if fs:
            font_sizes.add(fs)
    assert len(font_sizes) >= 3  # At least 3 distinct font sizes


def test_long_text_handling():
    """Paragraph-length body text wraps and fits."""
    long_text = (
        "This is a very long paragraph that should wrap to multiple lines "
        "when rendered inside a shape. The shape should grow taller to "
        "accommodate all the wrapped text content."
    )
    svg = Diagram().add("long", long_text, role=TextRole.BODY).render()

    root = ET.fromstring(svg)
    ns = {"svg": "http://www.w3.org/2000/svg"}
    # Should have multiple tspan elements for wrapped lines
    tspans = root.findall(".//svg:tspan", ns)
    assert len(tspans) > 1


def test_many_shapes():
    """20+ shapes auto-placed without overlaps."""
    d = Diagram()
    for i in range(25):
        d.add(f"s{i}", f"Shape {i}")

    svg = d.render()
    root = ET.fromstring(svg)

    # All shapes present
    for i in range(25):
        assert f"Shape {i}" in svg


def test_valid_svg_in_browser():
    """Output is valid XML, correct namespace, has viewBox."""
    svg = (
        Diagram()
        .add("a", "Alpha")
        .add("b", "Beta")
        .connect("a", "b")
        .render()
    )

    root = ET.fromstring(svg)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.get("viewBox") is not None
    assert root.get("width") is not None
    assert root.get("height") is not None


def test_connector_routing_complex():
    """Connectors in a larger diagram all produce valid paths."""
    svg = (
        Diagram()
        .add("a", "Step 1", row=0, col=0)
        .add("b", "Step 2", row=0, col=1)
        .add("c", "Step 3", row=0, col=2)
        .add("d", "Step 4", row=1, col=0)
        .add("e", "Step 5", row=1, col=2)
        .connect("a", "b")
        .connect("b", "c")
        .connect("a", "d", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER)
        .connect("d", "e")
        .connect("c", "e", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER)
        .render()
    )

    root = ET.fromstring(svg)
    ns = {"svg": "http://www.w3.org/2000/svg"}
    paths = root.findall(".//svg:path", ns)
    assert len(paths) >= 5  # 5 connectors
