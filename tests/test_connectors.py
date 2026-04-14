import pytest
from plotcraft.types import AnchorName, ArrowDirection, ConnectorStyle, LineWeight, ConnectionError as PlotCraftConnectionError
from plotcraft.shapes import create_shape
from plotcraft.grid import Grid
from plotcraft.connectors import create_connector, route_connector, route_all


def _make_two_shapes_grid():
    """Helper: two shapes side by side on a grid."""
    grid = Grid()
    s1 = create_shape("left", "Left Shape")
    s2 = create_shape("right", "Right Shape")
    grid.place(s1, 0, 0)
    # s1 has col_span=2 at the new BODY font size (18px Patrick Hand), so s2
    # must start at column 2 to avoid a PlacementError.
    grid.place(s2, 0, 2)
    placements = {p.shape.id: p for p in grid.all_placements()}
    return placements


def _make_three_shapes_row():
    """Helper: three shapes in a row, connector from 1st to 3rd must route around 2nd."""
    grid = Grid()
    s1 = create_shape("first", "First")
    s2 = create_shape("middle", "Middle")
    s3 = create_shape("last", "Last")
    grid.place(s1, 0, 0)
    grid.place(s2, 0, 1)
    grid.place(s3, 0, 2)
    return {p.shape.id: p for p in grid.all_placements()}


def test_simple_connector():
    """Two shapes side by side, connector has valid path."""
    placements = _make_two_shapes_grid()
    conn = create_connector("c1", "left", AnchorName.RIGHT_CENTER, "right", AnchorName.LEFT_CENTER)
    routed = route_connector(conn, placements)
    assert len(routed.path_points) >= 4
    assert routed.path_points[0].x < routed.path_points[-1].x  # left to right


def test_path_avoids_obstacle():
    """Three shapes in a row, connector from 1st to 3rd routes around 2nd."""
    placements = _make_three_shapes_row()
    conn = create_connector("c1", "first", AnchorName.RIGHT_CENTER, "last", AnchorName.LEFT_CENTER)
    routed = route_connector(conn, placements)
    # Should have extra waypoint(s) to avoid the middle shape
    assert len(routed.path_points) >= 4


def test_connector_uses_correct_anchors():
    """Source/target points match anchor positions."""
    placements = _make_two_shapes_grid()
    conn = create_connector("c1", "left", AnchorName.RIGHT_CENTER, "right", AnchorName.LEFT_CENTER)
    routed = route_connector(conn, placements)

    # First point should be near right edge of left shape
    left_p = placements["left"]

    expected_start_x = left_p.position.x + left_p.shape.content_bbox.width
    assert abs(routed.path_points[0].x - expected_start_x) < 1.0


def test_bezier_control_points_exist():
    """Path has >= 4 points (start, cp1, cp2, end)."""
    placements = _make_two_shapes_grid()
    conn = create_connector("c1", "left", AnchorName.RIGHT_CENTER, "right", AnchorName.LEFT_CENTER)
    routed = route_connector(conn, placements)
    assert len(routed.path_points) >= 4


def test_route_all():
    """Multiple connectors all get valid paths."""
    placements = _make_two_shapes_grid()
    c1 = create_connector("c1", "left", AnchorName.RIGHT_CENTER, "right", AnchorName.LEFT_CENTER)
    c2 = create_connector("c2", "left", AnchorName.BOTTOM_CENTER, "right", AnchorName.TOP_CENTER)
    routed = route_all([c1, c2], placements)
    assert len(routed) == 2
    assert all(len(c.path_points) >= 4 for c in routed)


def test_label_preserved():
    """Connector label survives routing."""
    placements = _make_two_shapes_grid()
    conn = create_connector("c1", "left", AnchorName.RIGHT_CENTER, "right", AnchorName.LEFT_CENTER, label="Yes")
    routed = route_connector(conn, placements)
    assert routed.label == "Yes"


def test_self_connection_raises():
    """Same source and target shape raises error."""
    with pytest.raises(PlotCraftConnectionError):
        create_connector("c1", "same", AnchorName.TOP_CENTER, "same", AnchorName.BOTTOM_CENTER)


def test_direction_stored():
    """Connector stores the direction field."""
    conn = create_connector(
        "c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER,
        direction=ArrowDirection.BOTH,
    )
    assert conn.direction == ArrowDirection.BOTH


def test_direction_default_forward():
    """Connector defaults to FORWARD direction."""
    conn = create_connector("c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER)
    assert conn.direction == ArrowDirection.FORWARD


def test_style_stored():
    """Connector stores the style field."""
    conn = create_connector(
        "c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER,
        style=ConnectorStyle.DASHED,
    )
    assert conn.style == ConnectorStyle.DASHED


def test_style_default_solid():
    """Connector defaults to SOLID style."""
    conn = create_connector("c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER)
    assert conn.style == ConnectorStyle.SOLID


def test_line_weight_stored():
    """Connector stores the line_weight field."""
    conn = create_connector(
        "c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER,
        line_weight=LineWeight.BOLD,
    )
    assert conn.line_weight == LineWeight.BOLD


def test_line_weight_default_normal():
    """Connector defaults to NORMAL line weight."""
    conn = create_connector("c1", "a", AnchorName.RIGHT_CENTER, "b", AnchorName.LEFT_CENTER)
    assert conn.line_weight == LineWeight.NORMAL


def test_style_and_weight_preserved_after_routing():
    """Style and weight survive routing."""
    placements = _make_two_shapes_grid()
    conn = create_connector(
        "c1", "left", AnchorName.RIGHT_CENTER, "right", AnchorName.LEFT_CENTER,
        style=ConnectorStyle.DOTTED, line_weight=LineWeight.THIN,
    )
    routed = route_connector(conn, placements)
    assert routed.style == ConnectorStyle.DOTTED
    assert routed.line_weight == LineWeight.THIN
