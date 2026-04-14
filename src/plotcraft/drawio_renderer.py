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
CANVAS_PADDING = 40  # extra padding around the diagram content


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
    x = _fmt(placement.position.x)
    y = _fmt(placement.position.y)
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
    src_anchor = ANCHOR_MAP.get(connector.source_anchor, (0.5, 0.5))
    tgt_anchor = ANCHOR_MAP.get(connector.target_anchor, (0.5, 0.5))
    anchor_style = (
        f"exitX={src_anchor[0]};exitY={src_anchor[1]};exitDx=0;exitDy=0;"
        f"entryX={tgt_anchor[0]};entryY={tgt_anchor[1]};entryDx=0;entryDy=0;"
    )

    # --- Assemble edge style --------------------------------------------------
    style = (
        f"edgeStyle=orthogonalEdgeStyle;curved=1;rounded=1;"
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

    x = _fmt(bounds.x)
    y = _fmt(bounds.y)
    w = _fmt(bounds.width)
    h = _fmt(bounds.height)

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
    lx = _fmt(bounds.x + padding)
    ly = _fmt(bounds.y + 4)
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

    page_width = int(canvas_size.width) + CANVAS_PADDING * 2
    page_height = int(canvas_size.height) + CANVAS_PADDING * 2

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
