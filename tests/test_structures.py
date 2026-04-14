import re
import xml.etree.ElementTree as ET
from plotcraft import Diagram, GridConfig, TimelineOrientation, TimelineEntry, TreeNode


NS = {"svg": "http://www.w3.org/2000/svg"}

# Wobble renders dots as <path fill="#007bff"> inside <g class="timeline"> or <g class="tree">
DOT_FILL = "#007bff"


def _parse_svg(svg: str):
    return ET.fromstring(svg)


def _get_dot_paths(group):
    """Return path elements that represent wobble dots (blue fill)."""
    return [p for p in group.findall("svg:path", NS) if p.get("fill") == DOT_FILL]


def _path_start_xy(path_elem):
    """Extract the M x y start coordinate from a path d attribute."""
    m = re.match(r"M ([\d.]+) ([\d.]+)", path_elem.get("d", ""))
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


def test_timeline_three_entries_produces_circles_and_line():
    """Timeline with 3 entries produces SVG with 3 dot paths and a line."""
    entries = [
        TimelineEntry("Alpha"),
        TimelineEntry("Beta"),
        TimelineEntry("Gamma"),
    ]
    svg = Diagram().timeline(entries).render()
    root = _parse_svg(svg)

    tl_g = root.find(".//svg:g[@class='timeline']", NS)
    assert tl_g is not None, "Expected a <g class='timeline'> group"

    dots = _get_dot_paths(tl_g)
    lines = tl_g.findall("svg:line", NS)
    assert len(dots) >= 3
    assert len(lines) >= 1


def test_horizontal_timeline_dots_left_to_right():
    """Horizontal timeline places dots left-to-right (increasing x, same rough y)."""
    entries = [
        TimelineEntry("A"),
        TimelineEntry("B"),
        TimelineEntry("C"),
    ]
    svg = Diagram().timeline(entries, orientation=TimelineOrientation.HORIZONTAL).render()
    root = _parse_svg(svg)

    tl_g = root.find(".//svg:g[@class='timeline']", NS)
    assert tl_g is not None
    dots = _get_dot_paths(tl_g)
    assert len(dots) == 3

    xs = [_path_start_xy(d)[0] for d in dots]
    # x values should be strictly increasing (wobble doesn't reorder dots)
    assert xs[0] < xs[1] < xs[2]


def test_vertical_timeline_dots_top_to_bottom():
    """Vertical timeline places dots top-to-bottom (increasing y)."""
    entries = [
        TimelineEntry("A"),
        TimelineEntry("B"),
        TimelineEntry("C"),
    ]
    svg = Diagram().timeline(entries, orientation=TimelineOrientation.VERTICAL).render()
    root = _parse_svg(svg)

    tl_g = root.find(".//svg:g[@class='timeline']", NS)
    assert tl_g is not None
    dots = _get_dot_paths(tl_g)
    assert len(dots) == 3

    ys = [_path_start_xy(d)[1] for d in dots]
    # y values should be strictly increasing
    assert ys[0] < ys[1] < ys[2]


def test_tree_root_with_two_children():
    """Tree with root + 2 children produces dot paths and line structure."""
    tree = TreeNode("Root", children=(
        TreeNode("Child A"),
        TreeNode("Child B"),
    ))
    svg = Diagram().tree(tree).render()
    root = _parse_svg(svg)

    tree_g = root.find(".//svg:g[@class='tree']", NS)
    assert tree_g is not None, "Expected a <g class='tree'> group"

    dots = _get_dot_paths(tree_g)
    assert len(dots) == 3

    # Should have lines for trunk + branches
    lines = tree_g.findall("svg:line", NS)
    assert len(lines) >= 3  # 1 vertical trunk + 2 horizontal branches


def test_labels_appear_in_svg():
    """Labels appear as text in the SVG output."""
    entries = [
        TimelineEntry("Phase One"),
        TimelineEntry("Phase Two"),
    ]
    svg = Diagram().timeline(entries).render()

    assert "Phase One" in svg
    assert "Phase Two" in svg

    tree = TreeNode("Root Node", children=(
        TreeNode("Leaf"),
    ))
    svg2 = Diagram().tree(tree).render()
    assert "Root Node" in svg2
    assert "Leaf" in svg2


def test_grid_alignment_dots_roughly_at_cell_centers():
    """Dot start positions are roughly near grid cell centers (within wobble tolerance)."""
    cfg = GridConfig(cell_width=200, cell_height=100, margin=20)
    entries = [
        TimelineEntry("A"),
        TimelineEntry("B"),
    ]
    svg = Diagram(grid_config=cfg).timeline(
        entries, orientation=TimelineOrientation.HORIZONTAL,
        start_row=0, start_col=0,
    ).render()
    root = _parse_svg(svg)

    tl_g = root.find(".//svg:g[@class='timeline']", NS)
    assert tl_g is not None
    dots = _get_dot_paths(tl_g)
    assert len(dots) == 2

    x0, y0 = _path_start_xy(dots[0])
    x1, _ = _path_start_xy(dots[1])

    # Cell centers: col=0 -> x=100, col=1 -> x=300, row=0 -> y=50
    # Wobble perturbs start point slightly — allow ±20px tolerance
    assert abs(x0 - 100.0) < 20, f"First dot x {x0} not near 100"
    assert abs(y0 - 50.0) < 20, f"First dot y {y0} not near 50"
    assert abs(x1 - 300.0) < 20, f"Second dot x {x1} not near 300"
