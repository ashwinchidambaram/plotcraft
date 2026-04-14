import xml.etree.ElementTree as ET
import pytest
from plotcraft.types import ShapeKind, TextRole, AnchorName, ArrowDirection
from plotcraft.shapes import create_shape
from plotcraft.grid import Grid
from plotcraft.connectors import create_connector, route_connector
from plotcraft.svg import SvgRenderer


def _make_simple_diagram():
    """Helper: 2 shapes + 1 connector, returns (placements, connectors, canvas_size)."""
    grid = Grid()
    s1 = create_shape("a", "Hello", kind=ShapeKind.RECT)
    s2 = create_shape("b", "World", kind=ShapeKind.RECT)
    grid.place(s1, 0, 0)
    grid.place(s2, 0, 1)
    placements_dict = {p.shape.id: p for p in grid.all_placements()}

    conn = create_connector("c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER)
    conn = route_connector(conn, placements_dict)

    return grid.all_placements(), [conn], grid.canvas_size()


def test_render_single_rect():
    """Output contains <rect with rx, ry attributes."""
    grid = Grid()
    shape = create_shape("r1", "Test", kind=ShapeKind.RECT)
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    assert "<rect" in svg
    assert 'rx="8' in svg
    assert 'ry="8' in svg


def test_render_text_inside_shape():
    """<text> element present with correct content."""
    grid = Grid()
    shape = create_shape("t1", "Hello World")
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    assert "Hello World" in svg
    assert "<text" in svg
    assert "<tspan" in svg


def test_render_circle():
    """<circle> element with correct r."""
    grid = Grid()
    shape = create_shape("c1", "Round", kind=ShapeKind.CIRCLE)
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    assert "<circle" in svg


def test_render_ellipse():
    """<ellipse> element for oval shapes."""
    grid = Grid()
    shape = create_shape("o1", "Oval Shape", kind=ShapeKind.OVAL)
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    assert "<ellipse" in svg


def test_render_connector_path():
    """<path> with bezier d attribute."""
    placements, connectors, canvas_size = _make_simple_diagram()

    renderer = SvgRenderer()
    svg = renderer.render_diagram(placements, connectors, canvas_size)

    assert "<path" in svg
    assert " C " in svg or " C" in svg  # cubic bezier command


def test_render_arrowhead():
    """<defs> contains <marker>."""
    placements, connectors, canvas_size = _make_simple_diagram()

    renderer = SvgRenderer()
    svg = renderer.render_diagram(placements, connectors, canvas_size)

    assert "<defs>" in svg
    assert "<marker" in svg
    assert 'id="arrowhead"' in svg


def test_full_diagram_valid_xml():
    """Parse output with xml.etree, no errors."""
    placements, connectors, canvas_size = _make_simple_diagram()

    renderer = SvgRenderer()
    svg = renderer.render_diagram(placements, connectors, canvas_size)

    # Should parse without errors
    root = ET.fromstring(svg)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"


def test_svg_has_xmlns():
    """Contains xmlns for SVG namespace."""
    renderer = SvgRenderer()
    from plotcraft.types import Size
    svg = renderer.render_diagram([], [], Size(100, 100))

    assert 'xmlns="http://www.w3.org/2000/svg"' in svg


def test_connector_label_rendered():
    """Label text appears in SVG."""
    grid = Grid()
    s1 = create_shape("a", "Start")
    s2 = create_shape("b", "End")
    grid.place(s1, 0, 0)
    grid.place(s2, 0, 1)
    placements_dict = {p.shape.id: p for p in grid.all_placements()}

    conn = create_connector("c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER, label="Yes")
    conn = route_connector(conn, placements_dict)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [conn], grid.canvas_size())

    assert "Yes" in svg


def test_render_diamond():
    """DIAMOND renders <polygon> with 4 points."""
    grid = Grid()
    shape = create_shape("d1", "Decision?", kind=ShapeKind.DIAMOND)
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    assert "<polygon" in svg
    # Find the polygon inside the shape group (not the arrowhead marker)
    root = ET.fromstring(svg)
    ns = {"svg": "http://www.w3.org/2000/svg"}
    group = root.find(".//svg:g[@id='shape-d1']", ns)
    assert group is not None
    polygon = group.find("svg:polygon", ns)
    assert polygon is not None
    points_str = polygon.get("points", "")
    # Diamond has 4 coordinate pairs like "cx,y rx,cy cx,by bx,cy"
    points = points_str.strip().split()
    assert len(points) == 4, f"Expected 4 points, got {len(points)}: {points_str}"


def test_none_renders_text_but_no_shape():
    """NONE renders text but no shape element (no rect/circle/ellipse)."""
    grid = Grid()
    shape = create_shape("none1", "Free Label", kind=ShapeKind.NONE)
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    # Text should be rendered
    assert "Free Label" in svg
    assert "<text" in svg

    # Parse and check: no shape elements inside the shape group
    import xml.etree.ElementTree as ET
    root = ET.fromstring(svg)
    ns = {"svg": "http://www.w3.org/2000/svg"}
    # Find the shape group
    groups = root.findall(".//svg:g[@id='shape-none1']", ns)
    assert len(groups) == 1
    group = groups[0]
    # No rect/circle/ellipse inside the shape group
    assert group.find("svg:rect", ns) is None
    assert group.find("svg:circle", ns) is None
    assert group.find("svg:ellipse", ns) is None
    # But text is present
    assert group.find("svg:text", ns) is not None


def test_no_sharp_corners():
    """All <rect> elements have rx > 0."""
    grid = Grid()
    s1 = create_shape("r1", "Rect 1", kind=ShapeKind.RECT)
    s2 = create_shape("r2", "Rect 2", kind=ShapeKind.SQUARE)
    grid.place(s1, 0, 0)
    grid.place(s2, 0, 1)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    root = ET.fromstring(svg)
    ns = {"svg": "http://www.w3.org/2000/svg"}
    rects = root.findall(".//svg:rect", ns)

    # Filter out the background rect (no rx)
    shape_rects = [r for r in rects if r.get("rx") is not None]
    assert len(shape_rects) >= 2
    for rect in shape_rects:
        rx = float(rect.get("rx", "0"))
        assert rx > 0, "Found a rect without rounded corners"


def test_xml_special_chars_escaped():
    """Text with < > & is properly escaped in SVG."""
    grid = Grid()
    shape = create_shape("esc", "A < B & C > D")
    grid.place(shape, 0, 0)

    renderer = SvgRenderer()
    svg = renderer.render_diagram(grid.all_placements(), [], grid.canvas_size())

    # Should be escaped, not raw
    assert "&lt;" in svg
    assert "&amp;" in svg
    assert "&gt;" in svg
    # Should still be valid XML
    ET.fromstring(svg)
