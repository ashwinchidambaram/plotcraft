"""Line-based structures: timelines and trees."""

from __future__ import annotations

from plotcraft.types import TimelineEntry, TimelineOrientation, TreeNode
from plotcraft.grid import GridConfig


# Style constants
_DOT_RADIUS = 6
_DOT_FILL = "#007bff"
_DOT_STROKE = "#0056b3"
_LINE_STROKE = "#999"
_LINE_STROKE_WIDTH = 1.5
_LABEL_FONT_SIZE = 14


def _escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _cell_center_x(col: int, cfg: GridConfig) -> float:
    return col * cfg.cell_width + cfg.cell_width / 2


def _cell_center_y(row: int, cfg: GridConfig) -> float:
    return row * cfg.cell_height + cfg.cell_height / 2


def build_timeline(
    entries: list[TimelineEntry],
    orientation: TimelineOrientation,
    start_row: int,
    start_col: int,
    grid_config: GridConfig,
) -> str:
    """Return SVG fragment for a timeline with dots, a connecting line, and labels."""
    if not entries:
        return ""

    cfg = grid_config
    parts: list[str] = []
    parts.append('    <g class="timeline">')

    if orientation == TimelineOrientation.HORIZONTAL:
        # Dots go left-to-right along the same row
        y = _cell_center_y(start_row, cfg)
        xs = [_cell_center_x(start_col + i, cfg) for i in range(len(entries))]

        # Main line
        parts.append(
            f'      <line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" '
            f'stroke="{_LINE_STROKE}" stroke-width="{_LINE_STROKE_WIDTH}" />'
        )

        # Dots and labels
        for i, entry in enumerate(entries):
            cx = xs[i]
            parts.append(
                f'      <circle cx="{cx}" cy="{y}" r="{_DOT_RADIUS}" '
                f'fill="{_DOT_FILL}" stroke="{_DOT_STROKE}" />'
            )
            # Label below the dot
            label_y = y + _DOT_RADIUS + _LABEL_FONT_SIZE + 4
            parts.append(
                f'      <text x="{cx}" y="{label_y}" '
                f'text-anchor="middle" font-family="Arial" '
                f'font-size="{_LABEL_FONT_SIZE}" fill="#222222">'
                f'{_escape_xml(entry.label)}</text>'
            )

    else:  # VERTICAL
        # Dots go top-to-bottom along the same column
        x = _cell_center_x(start_col, cfg)
        ys = [_cell_center_y(start_row + i, cfg) for i in range(len(entries))]

        # Main line
        parts.append(
            f'      <line x1="{x}" y1="{ys[0]}" x2="{x}" y2="{ys[-1]}" '
            f'stroke="{_LINE_STROKE}" stroke-width="{_LINE_STROKE_WIDTH}" />'
        )

        # Dots and labels
        for i, entry in enumerate(entries):
            cy = ys[i]
            parts.append(
                f'      <circle cx="{x}" cy="{cy}" r="{_DOT_RADIUS}" '
                f'fill="{_DOT_FILL}" stroke="{_DOT_STROKE}" />'
            )
            # Label to the right of the dot
            label_x = x + _DOT_RADIUS + 10
            parts.append(
                f'      <text x="{label_x}" y="{cy}" '
                f'text-anchor="start" dominant-baseline="central" '
                f'font-family="Arial" font-size="{_LABEL_FONT_SIZE}" '
                f'fill="#222222">{_escape_xml(entry.label)}</text>'
            )

    parts.append("    </g>")
    return "\n".join(parts)


def build_tree(
    root: TreeNode,
    start_row: int,
    start_col: int,
    grid_config: GridConfig,
) -> str:
    """Return SVG fragment for a tree with lines and labels (no boxes)."""
    cfg = grid_config
    parts: list[str] = []
    parts.append('    <g class="tree">')
    _render_tree_node(root, start_row, start_col, cfg, parts, _count_rows=[0])
    parts.append("    </g>")
    return "\n".join(parts)


def _tree_row_count(node: TreeNode) -> int:
    """Count total rows needed for this subtree."""
    if not node.children:
        return 1
    return sum(_tree_row_count(child) for child in node.children)


def _render_tree_node(
    node: TreeNode,
    row: int,
    col: int,
    cfg: GridConfig,
    parts: list[str],
    _count_rows: list[int],
) -> None:
    """Recursively render tree nodes. Each node gets its own row; children indent by one column."""
    x = _cell_center_x(col, cfg)
    y = _cell_center_y(row, cfg)

    # Dot for this node
    parts.append(
        f'      <circle cx="{x}" cy="{y}" r="{_DOT_RADIUS}" '
        f'fill="{_DOT_FILL}" stroke="{_DOT_STROKE}" />'
    )

    # Label to the right of the dot
    label_x = x + _DOT_RADIUS + 10
    parts.append(
        f'      <text x="{label_x}" y="{y}" '
        f'text-anchor="start" dominant-baseline="central" '
        f'font-family="Arial" font-size="{_LABEL_FONT_SIZE}" '
        f'fill="#222222">{_escape_xml(node.label)}</text>'
    )

    if not node.children:
        return

    child_col = col + 1
    child_row = row + 1
    child_x = _cell_center_x(child_col, cfg)

    # Vertical trunk line from this node down to span of children
    first_child_y = _cell_center_y(child_row, cfg)

    # Calculate where each child goes
    child_rows: list[int] = []
    current_row = child_row
    for child in node.children:
        child_rows.append(current_row)
        current_row += _tree_row_count(child)

    last_child_y = _cell_center_y(child_rows[-1], cfg)

    # Vertical line from parent down to children level
    parts.append(
        f'      <line x1="{x}" y1="{y}" x2="{x}" y2="{last_child_y}" '
        f'stroke="{_LINE_STROKE}" stroke-width="{_LINE_STROKE_WIDTH}" />'
    )

    # Horizontal branch to each child + recurse
    for i, child in enumerate(node.children):
        cy = _cell_center_y(child_rows[i], cfg)
        # Horizontal branch line
        parts.append(
            f'      <line x1="{x}" y1="{cy}" x2="{child_x}" y2="{cy}" '
            f'stroke="{_LINE_STROKE}" stroke-width="{_LINE_STROKE_WIDTH}" />'
        )
        _render_tree_node(child, child_rows[i], child_col, cfg, parts, _count_rows)
