"""draw.io XML renderer for PlotCraft diagrams.

Converts PlotCraft's internal model to .drawio XML (mxGraphModel format)
suitable for opening in the draw.io desktop app or web editor.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

from plotcraft.types import (
    ShapeKind,
    TextRole,
    AnchorName,
    ArrowDirection,
    ConnectorStyle,
    LineWeight,
    LINE_WEIGHT_WIDTHS,
    ColorTheme,
    COLOR_DEFAULTS,
    TEXT_STYLE_DEFAULTS,
    SectionStyle,
    Size,
    BBox,
)
from plotcraft.grid import Placement


# ---------------------------------------------------------------------------
# Anchor mapping: AnchorName → (exitX/entryX, exitY/entryY) fractions
# ---------------------------------------------------------------------------

ANCHOR_MAP: dict[AnchorName, tuple[float, float]] = {
    AnchorName.TOP_LEFT: (0, 0),
    AnchorName.TOP_CENTER: (0.5, 0),
    AnchorName.TOP_RIGHT: (1, 0),
    AnchorName.LEFT_CENTER: (0, 0.5),
    AnchorName.CENTER: (0.5, 0.5),
    AnchorName.RIGHT_CENTER: (1, 0.5),
    AnchorName.BOTTOM_LEFT: (0, 1),
    AnchorName.BOTTOM_CENTER: (0.5, 1),
    AnchorName.BOTTOM_RIGHT: (1, 1),
}


# ---------------------------------------------------------------------------
# Shape kind → draw.io base style fragment
# ---------------------------------------------------------------------------

SHAPE_STYLE_MAP: dict[ShapeKind, str] = {
    ShapeKind.RECT:    "rounded=1;arcSize=12",
    ShapeKind.SQUARE:  "rounded=1;arcSize=12",
    ShapeKind.CIRCLE:  "ellipse;aspect=fixed",
    ShapeKind.OVAL:    "ellipse",
    ShapeKind.DIAMOND: "rhombus",
    ShapeKind.NONE:    "text;fillColor=none;strokeColor=none",
}


# ---------------------------------------------------------------------------
# Canvas background
# ---------------------------------------------------------------------------

BACKGROUND_COLOR = "#fdf6e3"
CANVAS_PADDING = 60  # extra padding around the diagram content

# Draw.io needs gaps between shapes for clean arrow routing.
# Instead of scaling all coords (which distorts proportions),
# we add a fixed gap per grid cell so there's routing space.
CELL_GAP_X = 50  # extra horizontal px per grid column
CELL_GAP_Y = 40  # extra vertical px per grid row

# How far connectors extend from shapes before turning (in px).
JETTY_SIZE = 16


def _compute_best_anchors(
    src_p: Placement,
    tgt_p: Placement,
    user_src_anchor: AnchorName,
    user_tgt_anchor: AnchorName,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Compute draw.io anchor fractions based on relative shape positions.

    If the user-specified anchors would cause the arrow to exit AWAY from
    the target (causing a U-turn), override them with direction-correct
    anchors. Otherwise respect the user's choice.
    """
    # Center positions of source and target
    src_cx = src_p.position.x + src_p.shape.content_bbox.width / 2
    src_cy = src_p.position.y + src_p.shape.content_bbox.height / 2
    tgt_cx = tgt_p.position.x + tgt_p.shape.content_bbox.width / 2
    tgt_cy = tgt_p.position.y + tgt_p.shape.content_bbox.height / 2

    dx = tgt_cx - src_cx
    dy = tgt_cy - src_cy

    # Determine dominant direction from source to target
    if abs(dx) > abs(dy):
        # Primarily horizontal
        if dx > 0:
            best_src = (1, 0.5)    # exit right
            best_tgt = (0, 0.5)    # enter left
        else:
            best_src = (0, 0.5)    # exit left
            best_tgt = (1, 0.5)    # enter right
    else:
        # Primarily vertical
        if dy > 0:
            best_src = (0.5, 1)    # exit bottom
            best_tgt = (0.5, 0)    # enter top
        else:
            best_src = (0.5, 0)    # exit top
            best_tgt = (0.5, 1)    # enter bottom

    # Check if user-specified anchors would cause a U-turn.
    # A U-turn happens when the exit direction is opposite to the target direction.
    user_src = ANCHOR_MAP.get(user_src_anchor, (0.5, 0.5))
    user_tgt = ANCHOR_MAP.get(user_tgt_anchor, (0.5, 0.5))

    def _would_uturn(anchor: tuple[float, float], target_dx: float, target_dy: float) -> bool:
        """Check if this exit anchor points away from the target."""
        # Anchor (1, 0.5) = right side. If target is left (dx < 0), that's a U-turn.
        ax, ay = anchor
        if ax == 1 and target_dx < -20:    # exiting right, target is far left
            return True
        if ax == 0 and target_dx > 20:     # exiting left, target is far right
            return True
        if ay == 1 and target_dy < -20:    # exiting bottom, target is far above
            return True
        if ay == 0 and target_dy > 20:     # exiting top, target is far below
            return True
        return False

    # Override source anchor if it would U-turn
    src_result = user_src if not _would_uturn(user_src, dx, dy) else best_src

    # Override target anchor if it would U-turn (check from target's perspective)
    tgt_result = user_tgt if not _would_uturn(user_tgt, -dx, -dy) else best_tgt

    return src_result, tgt_result


def _fmt(v: float) -> str:
    """Format a float, omitting the decimal point when the value is a whole number."""
    return str(int(v)) if v == int(v) else f"{v:.2f}".rstrip("0").rstrip(".")


def _shape_cell(placement: Placement) -> str:
    """Render a single shape placement as an mxCell vertex string."""
    shape = placement.shape
    kind = shape.kind

    # Colours
    palette = COLOR_DEFAULTS.get(shape.color_theme, COLOR_DEFAULTS[ColorTheme.NEUTRAL])
    fill_color = palette.fill
    stroke_color = palette.stroke
    opacity = int(palette.fill_opacity * 100)

    # Typography
    text_style = TEXT_STYLE_DEFAULTS.get(shape.role, TEXT_STYLE_DEFAULTS[TextRole.BODY])
    font_family = text_style.font_family
    font_size = text_style.font_size
    # draw.io uses a numeric bold flag: 1 = bold, 0 = normal
    is_bold = 1 if text_style.font_weight not in ("normal", "400") else 0

    # Base shape style
    base = SHAPE_STYLE_MAP[kind]

    if kind == ShapeKind.NONE:
        # Free-floating text: no fill/stroke decoration
        style = (
            f"{base};"
            f"html=1;"
            f"fontFamily={font_family};"
            f"fontSize={_fmt(font_size)};"
            f"fontStyle={is_bold};"
            f"fontColor=#2C2C2C;"
        )
    else:
        style = (
            f"{base};"
            f"whiteSpace=wrap;"
            f"html=1;"
            f"fillColor={fill_color};"
            f"strokeColor={stroke_color};"
            f"strokeWidth=2;"
            f"opacity={opacity};"
            f"fontFamily={font_family};"
            f"fontSize={_fmt(font_size)};"
            f"fontStyle={is_bold};"
            f"fontColor=#2C2C2C;"
        )

    cell_id = f"shape_{shape.id}"
    value = escape(shape.text)
    # Add per-cell gaps so draw.io has room to route arrows between shapes.
    # Each grid column adds CELL_GAP_X, each row adds CELL_GAP_Y.
    x = _fmt(placement.position.x + placement.col * CELL_GAP_X + CANVAS_PADDING)
    y = _fmt(placement.position.y + placement.row * CELL_GAP_Y + CANVAS_PADDING)
    w = _fmt(shape.content_bbox.width)
    h = _fmt(shape.content_bbox.height)

    lines = [
        f'        <mxCell id="{cell_id}" value="{value}" style="{style}" vertex="1" parent="1">',
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />',
        f'        </mxCell>',
    ]
    return "\n".join(lines)


def _connector_cells(connector, placements_dict: dict[str, Placement]) -> str:
    """Render a connector as one (or two, if labelled) mxCell elements."""
    conn_id = connector.id
    source_id = f"shape_{connector.source_shape_id}"
    target_id = f"shape_{connector.target_shape_id}"

    # --- Arrow style ----------------------------------------------------------
    direction = connector.direction
    if direction == ArrowDirection.FORWARD:
        arrow_style = "endArrow=blockThin;endFill=1;"
    elif direction == ArrowDirection.BACKWARD:
        arrow_style = "startArrow=blockThin;startFill=1;endArrow=none;"
    elif direction == ArrowDirection.BOTH:
        arrow_style = "startArrow=blockThin;startFill=1;endArrow=blockThin;endFill=1;"
    else:  # NONE
        arrow_style = "endArrow=none;"

    # --- Line style -----------------------------------------------------------
    line_style_fragment = ""
    if connector.style == ConnectorStyle.DASHED:
        line_style_fragment = "dashed=1;dashPattern=8 4;"
    elif connector.style == ConnectorStyle.DOTTED:
        line_style_fragment = "dashed=1;dashPattern=2 4;"

    # --- Stroke width ---------------------------------------------------------
    stroke_width = _fmt(LINE_WEIGHT_WIDTHS.get(connector.line_weight, 2.0))

    # --- Stroke colour from source shape theme --------------------------------
    source_placement = placements_dict.get(connector.source_shape_id)
    if source_placement:
        palette = COLOR_DEFAULTS.get(
            source_placement.shape.color_theme,
            COLOR_DEFAULTS[ColorTheme.NEUTRAL],
        )
        stroke_color = palette.stroke
    else:
        stroke_color = "#555555"

    # --- Anchor exit/entry ----------------------------------------------------
    # Auto-compute best anchors from relative positions of source and target.
    # This overrides user-specified anchors when they would cause U-turn routing
    # (e.g., exiting RIGHT when the target is to the LEFT).
    target_placement = placements_dict.get(connector.target_shape_id)
    if source_placement and target_placement:
        src_anchor, tgt_anchor = _compute_best_anchors(
            source_placement, target_placement,
            connector.source_anchor, connector.target_anchor,
        )
    else:
        src_anchor = ANCHOR_MAP.get(connector.source_anchor, (0.5, 0.5))
        tgt_anchor = ANCHOR_MAP.get(connector.target_anchor, (0.5, 0.5))
    anchor_style = (
        f"exitX={src_anchor[0]};exitY={src_anchor[1]};exitDx=0;exitDy=0;"
        f"entryX={tgt_anchor[0]};entryY={tgt_anchor[1]};entryDx=0;entryDy=0;"
    )

    # --- Assemble edge style --------------------------------------------------
    style = (
        f"edgeStyle=orthogonalEdgeStyle;curved=1;rounded=1;"
        f"jettySize={JETTY_SIZE};"
        f"strokeColor={stroke_color};strokeWidth={stroke_width};"
        f"{arrow_style}"
        f"{line_style_fragment}"
        f"{anchor_style}"
    )

    lines = [
        f'        <mxCell id="{conn_id}" style="{style}" edge="1" source="{source_id}" target="{target_id}" parent="1">',
        f'          <mxGeometry relative="1" as="geometry" />',
        f'        </mxCell>',
    ]

    # --- Optional edge label --------------------------------------------------
    if connector.label:
        label_value = escape(connector.label)
        label_style = (
            "edgeLabel;html=1;fontSize=12;"
            "fontFamily=Patrick Hand;fontColor=#555555;align=center;"
        )
        lines += [
            f'        <mxCell id="{conn_id}_label" value="{label_value}" style="{label_style}" vertex="1" connectable="0" parent="{conn_id}">',
            f'          <mxGeometry x="-0.1" relative="1" as="geometry">',
            f'            <mxPoint as="offset" />',
            f'          </mxGeometry>',
            f'        </mxCell>',
        ]

    return "\n".join(lines)


def _section_cells(index: int, label: str, bounds: BBox, style: SectionStyle) -> str:
    """Render a section as a labelled background rectangle."""
    fill = style.fill
    stroke = style.stroke
    sw = _fmt(style.stroke_width)
    fs = _fmt(style.label_font_size)
    color = style.label_color
    padding = style.padding

    # Sections need the same gap-based offset as shapes.
    # Estimate the column/row range from bounds position.
    # bounds.x / cell_width gives approximate column.
    approx_col = max(0, int(bounds.x / 260)) if bounds.x > 0 else 0
    approx_row = max(0, int(bounds.y / 160)) if bounds.y > 0 else 0
    approx_col_end = max(0, int((bounds.x + bounds.width) / 260))
    approx_row_end = max(0, int((bounds.y + bounds.height) / 160))
    x = _fmt(bounds.x + approx_col * CELL_GAP_X + CANVAS_PADDING)
    y = _fmt(bounds.y + approx_row * CELL_GAP_Y + CANVAS_PADDING)
    w = _fmt(bounds.width + (approx_col_end - approx_col) * CELL_GAP_X)
    h = _fmt(bounds.height + (approx_row_end - approx_row) * CELL_GAP_Y)

    bg_style = (
        f"rounded=1;dashed=1;dashPattern=8 4;"
        f"fillColor={fill};strokeColor={stroke};strokeWidth={sw};"
        f"arcSize=8;opacity=80;"
    )
    lbl_style = (
        f"text;html=1;fontSize={fs};fontFamily=Caveat;"
        f"fontColor={color};align=left;verticalAlign=top;"
    )

    # Label positioned inside the top-left of the section box
    lx = _fmt(bounds.x + approx_col * CELL_GAP_X + CANVAS_PADDING + padding)
    ly = _fmt(bounds.y + approx_row * CELL_GAP_Y + CANVAS_PADDING + 4)
    lbl_value = escape(label)

    lines = [
        f'        <mxCell id="section_{index}" value="" style="{bg_style}" vertex="1" parent="1">',
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />',
        f'        </mxCell>',
        f'        <mxCell id="section_{index}_label" value="{lbl_value}" style="{lbl_style}" vertex="1" parent="1">',
        f'          <mxGeometry x="{lx}" y="{ly}" width="200" height="25" as="geometry" />',
        f'        </mxCell>',
    ]
    return "\n".join(lines)


def render_drawio_xml(
    placements: list[Placement],
    connectors: list,  # list of Connector stubs (unrouted)
    canvas_size: Size,
    sections: list[tuple[str, BBox, SectionStyle]] | None = None,
) -> str:
    """Convert PlotCraft's internal model to .drawio XML (mxGraphModel format).

    Args:
        placements: All placed shapes from the grid.
        connectors: Connector stubs (source/target/anchor metadata; path_points unused).
        canvas_size: Total canvas dimensions.
        sections: Optional list of (label, bounds_bbox, style) tuples.

    Returns:
        A UTF-8 string containing valid .drawio XML.
    """
    sections = sections or []

    # Estimate max column/row from canvas size for gap calculation
    max_cols = max(1, int(canvas_size.width / 260)) + 1
    max_rows = max(1, int(canvas_size.height / 160)) + 1
    page_width = int(canvas_size.width) + max_cols * CELL_GAP_X + CANVAS_PADDING * 2
    page_height = int(canvas_size.height) + max_rows * CELL_GAP_Y + CANVAS_PADDING * 2

    # Build a lookup for connectors to resolve stroke colours
    placements_dict: dict[str, Placement] = {p.shape.id: p for p in placements}

    # Collect all body XML lines
    body_lines: list[str] = []

    # 1. Sections go first so they render behind shapes
    for i, (label, bounds, style) in enumerate(sections):
        body_lines.append(_section_cells(i, label, bounds, style))

    # 2. Shape vertices
    for placement in placements:
        body_lines.append(_shape_cell(placement))

    # 3. Connector edges (and optional labels)
    for connector in connectors:
        body_lines.append(_connector_cells(connector, placements_dict))

    body = "\n".join(body_lines)

    xml = (
        f'<mxfile host="plotcraft" version="1.0">\n'
        f'  <diagram id="diagram" name="PlotCraft Diagram">\n'
        f'    <mxGraphModel'
        f' dx="1200" dy="800"'
        f' grid="1" gridSize="10"'
        f' guides="1" tooltips="1" connect="1" arrows="1" fold="1"'
        f' page="1" pageScale="1"'
        f' pageWidth="{page_width}" pageHeight="{page_height}"'
        f' math="0" shadow="0"'
        f' background="{BACKGROUND_COLOR}">\n'
        f'      <root>\n'
        f'        <mxCell id="0" />\n'
        f'        <mxCell id="1" parent="0" />\n'
        f'{body}\n'
        f'      </root>\n'
        f'    </mxGraphModel>\n'
        f'  </diagram>\n'
        f'</mxfile>\n'
    )
    return xml
