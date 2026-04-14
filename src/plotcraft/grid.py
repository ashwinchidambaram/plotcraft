from __future__ import annotations
import math
from dataclasses import dataclass
from plotcraft.types import Point, Size, BBox, PlacementError
from plotcraft.shapes import Shape


@dataclass(frozen=True)
class GridConfig:
    cell_width: float = 160.0
    cell_height: float = 120.0
    margin: float = 24.0  # margin around shape within bounding box


@dataclass(frozen=True)
class Placement:
    """A shape placed on the grid."""
    shape: Shape
    row: int
    col: int
    row_span: int
    col_span: int
    position: Point  # top-left pixel position of the shape (centered in cells)
    bounding_box: BBox  # full bounding box including margin (the grid cells area)


class Grid:
    def __init__(self, config: GridConfig = GridConfig()):
        self._config = config
        self._placements: dict[str, Placement] = {}  # shape_id -> Placement
        self._occupied: set[tuple[int, int]] = set()  # (row, col) cells taken

    def place(self, shape: Shape, row: int, col: int) -> Placement:
        """Place shape at (row, col). Raises PlacementError if cells occupied."""
        row_span, col_span = self._cells_needed(shape)
        if not self._check_available(row, col, row_span, col_span):
            raise PlacementError(
                f"Cannot place shape '{shape.id}' at ({row}, {col}): cells occupied"
            )
        self._claim_cells(row, col, row_span, col_span)
        placement = self._create_placement(shape, row, col, row_span, col_span)
        self._placements[shape.id] = placement
        return placement

    def auto_place(self, shape: Shape) -> Placement:
        """Place shape in first available position (left-to-right, top-to-bottom)."""
        row_span, col_span = self._cells_needed(shape)
        max_cols = 10
        for r in range(100):  # reasonable upper bound
            for c in range(max_cols):
                if self._check_available(r, c, row_span, col_span):
                    return self.place(shape, r, c)
        raise PlacementError(f"No available position for shape '{shape.id}'")

    def get_placement(self, shape_id: str) -> Placement:
        if shape_id not in self._placements:
            raise KeyError(f"Shape '{shape_id}' not placed on grid")
        return self._placements[shape_id]

    def all_placements(self) -> list[Placement]:
        return list(self._placements.values())

    def canvas_size(self) -> Size:
        """Total canvas dimensions covering all placed shapes."""
        if not self._placements:
            return Size(0, 0)
        max_x = 0.0
        max_y = 0.0
        for p in self._placements.values():
            max_x = max(max_x, p.bounding_box.x + p.bounding_box.width)
            max_y = max(max_y, p.bounding_box.y + p.bounding_box.height)
        return Size(max_x, max_y)

    def _cells_needed(self, shape: Shape) -> tuple[int, int]:
        """How many (row_span, col_span) this shape needs."""
        # Bounding box = shape content_bbox + margin on all sides
        total_w = shape.content_bbox.width + 2 * self._config.margin
        total_h = shape.content_bbox.height + 2 * self._config.margin
        col_span = max(1, math.ceil(total_w / self._config.cell_width))
        row_span = max(1, math.ceil(total_h / self._config.cell_height))
        return row_span, col_span

    def _check_available(self, row: int, col: int, row_span: int, col_span: int) -> bool:
        for r in range(row, row + row_span):
            for c in range(col, col + col_span):
                if (r, c) in self._occupied:
                    return False
        return True

    def _claim_cells(self, row: int, col: int, row_span: int, col_span: int) -> None:
        for r in range(row, row + row_span):
            for c in range(col, col + col_span):
                self._occupied.add((r, c))

    def _create_placement(self, shape: Shape, row: int, col: int,
                          row_span: int, col_span: int) -> Placement:
        """Create a Placement with the shape centered within its claimed cells."""
        cfg = self._config
        # Bounding box covers the full grid cells area
        bb_x = col * cfg.cell_width
        bb_y = row * cfg.cell_height
        bb_w = col_span * cfg.cell_width
        bb_h = row_span * cfg.cell_height

        # Shape position: centered within the bounding box
        shape_x = bb_x + (bb_w - shape.content_bbox.width) / 2
        shape_y = bb_y + (bb_h - shape.content_bbox.height) / 2

        return Placement(
            shape=shape,
            row=row,
            col=col,
            row_span=row_span,
            col_span=col_span,
            position=Point(shape_x, shape_y),
            bounding_box=BBox(bb_x, bb_y, bb_w, bb_h),
        )
