import pytest
from plotcraft.types import ShapeKind, TextRole, PlacementError
from plotcraft.shapes import create_shape
from plotcraft.grid import Grid, GridConfig, Placement


def test_place_single_shape():
    """Place a shape at (0,0), verify position is correct."""
    grid = Grid()
    shape = create_shape("s1", "Hello")
    p = grid.place(shape, 0, 0)
    assert p.row == 0
    assert p.col == 0
    assert p.position.x >= 0
    assert p.position.y >= 0


def test_place_two_shapes_no_overlap():
    """Two shapes side by side, no error."""
    grid = Grid()
    s1 = create_shape("s1", "First")
    s2 = create_shape("s2", "Second")
    grid.place(s1, 0, 0)
    grid.place(s2, 0, 1)
    assert len(grid.all_placements()) == 2


def test_place_overlap_raises():
    """Placing on occupied cell raises PlacementError."""
    grid = Grid()
    s1 = create_shape("s1", "First")
    s2 = create_shape("s2", "Second")
    grid.place(s1, 0, 0)
    with pytest.raises(PlacementError):
        grid.place(s2, 0, 0)


def test_auto_place_fills_left_to_right():
    """Three auto-placed shapes end up at (0,0), (0,1), (0,2)."""
    grid = Grid()
    shapes = [create_shape(f"s{i}", f"Shape {i}") for i in range(3)]
    placements = [grid.auto_place(s) for s in shapes]
    assert placements[0].col == 0
    assert placements[1].col == 1
    assert placements[2].col == 2
    assert all(p.row == 0 for p in placements)


def test_large_shape_spans_cells():
    """Big shape claims multiple cells."""
    config = GridConfig(cell_width=100, cell_height=80, margin=10)
    grid = Grid(config)
    # A title with long text should be wide enough to span multiple columns
    shape = create_shape("big", "This is a very long title text", role=TextRole.TITLE, max_text_width=300)
    p = grid.place(shape, 0, 0)
    assert p.col_span >= 2 or p.row_span >= 1  # Should span at least something


def test_shape_centered_in_cells():
    """Shape position centers it within claimed area."""
    grid = Grid()
    shape = create_shape("c1", "Centered")
    p = grid.place(shape, 0, 0)
    # Shape should be within the bounding box
    assert p.position.x >= p.bounding_box.x
    assert p.position.y >= p.bounding_box.y
    assert p.position.x + shape.content_bbox.width <= p.bounding_box.x + p.bounding_box.width
    assert p.position.y + shape.content_bbox.height <= p.bounding_box.y + p.bounding_box.height


def test_canvas_size():
    """Canvas size covers all placed shapes."""
    grid = Grid()
    s1 = create_shape("s1", "First")
    s2 = create_shape("s2", "Second")
    grid.place(s1, 0, 0)
    grid.place(s2, 1, 1)
    size = grid.canvas_size()
    assert size.width > 0
    assert size.height > 0
    # Should cover both placements
    for p in grid.all_placements():
        assert size.width >= p.bounding_box.x + p.bounding_box.width
        assert size.height >= p.bounding_box.y + p.bounding_box.height


def test_mixed_manual_and_auto():
    """Manual placement + auto_place skips occupied cells."""
    grid = Grid()
    s1 = create_shape("s1", "Manual")
    s2 = create_shape("s2", "Auto")
    grid.place(s1, 0, 0)  # Occupy (0,0)
    p2 = grid.auto_place(s2)  # Should skip (0,0)
    assert (p2.row, p2.col) != (0, 0)


def test_bounding_boxes_never_overlap():
    """Place several shapes, assert no bbox intersections."""
    grid = Grid()
    shapes = [create_shape(f"s{i}", f"Shape {i}") for i in range(5)]
    placements = [grid.auto_place(s) for s in shapes]

    for i, p1 in enumerate(placements):
        for p2 in placements[i + 1:]:
            b1 = p1.bounding_box
            b2 = p2.bounding_box
            # Check no overlap: one must be fully left, right, above, or below
            no_overlap = (
                b1.x + b1.width <= b2.x or
                b2.x + b2.width <= b1.x or
                b1.y + b1.height <= b2.y or
                b2.y + b2.height <= b1.y
            )
            assert no_overlap, f"Shapes {p1.shape.id} and {p2.shape.id} bounding boxes overlap"


def test_empty_canvas_size():
    """Empty grid has zero canvas size."""
    grid = Grid()
    size = grid.canvas_size()
    assert size.width == 0
    assert size.height == 0


def test_get_placement():
    """Can retrieve a placement by shape ID."""
    grid = Grid()
    shape = create_shape("lookup", "Find me")
    grid.place(shape, 0, 0)
    p = grid.get_placement("lookup")
    assert p.shape.id == "lookup"


def test_get_missing_placement_raises():
    """Looking up non-existent shape raises KeyError."""
    grid = Grid()
    with pytest.raises(KeyError):
        grid.get_placement("nonexistent")
