"""Excalidraw JSON renderer for PlotCraft diagrams.

Converts PlotCraft's internal model (Placement, Connector, sections) into
Excalidraw JSON format suitable for opening in the Excalidraw editor.
"""
from __future__ import annotations

import zlib

from plotcraft.types import (
    ShapeKind,
    TextRole,
    TextAlign,
    AnchorName,
    ArrowDirection,
    ConnectorStyle,
    LINE_WEIGHT_WIDTHS,
    ColorTheme,
    SectionStyle,
    Size,
    BBox,
    Point,
)
from plotcraft.grid import Placement
from plotcraft.connectors import Connector
from plotcraft.shapes import resolve_anchor
from plotcraft.routing import route_orthogonal


# ---------------------------------------------------------------------------
# Color mapping: ColorTheme → (backgroundColor, strokeColor)
# ---------------------------------------------------------------------------

EXCALIDRAW_COLORS: dict[ColorTheme, tuple[str, str]] = {
    ColorTheme.NEUTRAL:   ("#F3EFE8", "#757575"),
    ColorTheme.START:     ("#FCF0ED", "#A84F3B"),
    ColorTheme.END:       ("#E3E8DF", "#485240"),
    ColorTheme.DECISION:  ("#FDF8F0", "#5E422A"),
    ColorTheme.ERROR:     ("#FDF0EF", "#7F2A27"),
    ColorTheme.HIGHLIGHT: ("#D4745E", "#853D2D"),
    ColorTheme.INFO:      ("#F2F5F7", "#3B5160"),
    ColorTheme.SUCCESS:   ("#E3E8DF", "#485240"),
    ColorTheme.WARNING:   ("#F7E9D1", "#835C39"),
}

# Text colors: charcoal on light fills, sand on dark fills (HIGHLIGHT)
_TEXT_COLOR_LIGHT = "#2C2C2C"
_TEXT_COLOR_DARK = "#E8DCC4"
_DARK_FILL_THEMES = {ColorTheme.HIGHLIGHT}

CANVAS_BACKGROUND = "#F9F7F4"

# ---------------------------------------------------------------------------
# Dark theme colors
# ---------------------------------------------------------------------------

EXCALIDRAW_COLORS_DARK: dict[ColorTheme, tuple[str, str]] = {
    ColorTheme.NEUTRAL:   ("#2C2C2C", "#8B8B8B"),
    ColorTheme.START:     ("#3D1F17", "#D4745E"),
    ColorTheme.END:       ("#1E2B1E", "#8B9D83"),
    ColorTheme.DECISION:  ("#2E2214", "#D4A574"),
    ColorTheme.ERROR:     ("#3D1614", "#D4745E"),
    ColorTheme.HIGHLIGHT: ("#853D2D", "#D4745E"),
    ColorTheme.INFO:      ("#1A2830", "#6B8FA3"),
    ColorTheme.SUCCESS:   ("#1E2B1E", "#8B9D83"),
    ColorTheme.WARNING:   ("#2E2214", "#D4A574"),
}

CANVAS_BACKGROUND_DARK = "#1A1A1A"

_TEXT_COLOR_LIGHT_ON_DARK = "#E8DCC4"  # Sand 300 - for text on dark theme

# ---------------------------------------------------------------------------
# Font size mapping: TextRole → Excalidraw fontSize
# ---------------------------------------------------------------------------

FONT_SIZE_MAP: dict[TextRole, int] = {
    TextRole.TITLE: 28,
    TextRole.SUBTITLE: 22,
    TextRole.BODY: 16,
    TextRole.CAPTION: 14,
}

# Excalidraw fontFamily codes: 1 = Virgil (hand-drawn), 2 = Helvetica, 3 = Cascadia
_FONT_FAMILY = 3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _deterministic_seed(element_id: str) -> int:
    """Generate a stable seed from an element ID using Adler-32.

    This ensures reproducible roughness patterns across renders.
    """
    return zlib.adler32(element_id.encode())


def _text_color_for_theme(theme: ColorTheme) -> str:
    """Return the appropriate text color for a given color theme."""
    if theme in _DARK_FILL_THEMES:
        return _TEXT_COLOR_DARK
    return _TEXT_COLOR_LIGHT


def _text_align_value(align: TextAlign) -> str:
    """Map PlotCraft TextAlign to Excalidraw textAlign string."""
    return align.value


def _make_base_element(
    elem_id: str,
    elem_type: str,
    x: float,
    y: float,
    width: float,
    height: float,
    roughness: int = 1,
    **kwargs: object,
) -> dict:
    """Create the common Excalidraw element dict with all shared properties.

    Additional or overriding properties can be passed via kwargs.
    """
    seed = _deterministic_seed(elem_id)
    element: dict = {
        "type": elem_type,
        "id": elem_id,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "strokeColor": "#757575",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": roughness,
        "opacity": 100,
        "angle": 0,
        "seed": seed,
        "version": 1,
        "versionNonce": seed ^ 0xFFFF,
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
    }
    element.update(kwargs)
    return element


# ---------------------------------------------------------------------------
# Shape elements
# ---------------------------------------------------------------------------

_SHAPE_TYPE_MAP: dict[ShapeKind, str] = {
    ShapeKind.RECT:    "rectangle",
    ShapeKind.SQUARE:  "rectangle",
    ShapeKind.CIRCLE:  "ellipse",
    ShapeKind.OVAL:    "ellipse",
    ShapeKind.DIAMOND: "diamond",
}


def _shape_element(
    placement: Placement,
    canvas_padding: float,
    roughness: int = 1,
    dark: bool = False,
) -> tuple[dict, dict | None]:
    """Convert a Placement into Excalidraw element(s).

    For ShapeKind.NONE: returns (free_floating_text_element, None).
    For all others: returns (shape_element, bound_text_element).
    """
    shape = placement.shape
    px = placement.position.x + canvas_padding
    py = placement.position.y + canvas_padding
    w = shape.content_bbox.width
    h = shape.content_bbox.height

    font_size = FONT_SIZE_MAP.get(shape.role, 16)
    theme = shape.color_theme
    text_color = _TEXT_COLOR_LIGHT_ON_DARK if dark else _text_color_for_theme(theme)

    if shape.kind == ShapeKind.NONE:
        # Free-floating text — no parent shape
        text_id = f"exc_text_{shape.id}"
        text_elem = _make_base_element(
            text_id, "text", px, py, w, h,
            roughness=0,
            strokeColor=text_color,
            backgroundColor="transparent",
            strokeWidth=1,
            text=shape.text,
            originalText=shape.text,
            fontSize=font_size,
            fontFamily=_FONT_FAMILY,
            textAlign=_text_align_value(shape.align),
            verticalAlign="middle",
            containerId=None,
            lineHeight=1.25,
        )
        return text_elem, None

    # Visible shape with bound text
    palette = EXCALIDRAW_COLORS_DARK if dark else EXCALIDRAW_COLORS
    bg_color, stroke_color = palette.get(
        theme, palette[ColorTheme.NEUTRAL]
    )
    excalidraw_type = _SHAPE_TYPE_MAP[shape.kind]
    shape_id = f"exc_shape_{shape.id}"
    text_id = f"exc_text_{shape.id}"

    # Roundness only for rectangles
    extra_shape_props: dict = {}
    if excalidraw_type == "rectangle":
        extra_shape_props["roundness"] = {"type": 3}

    shape_elem = _make_base_element(
        shape_id, excalidraw_type, px, py, w, h,
        roughness=roughness,
        strokeColor=stroke_color,
        backgroundColor=bg_color,
        boundElements=[{"id": text_id, "type": "text"}],
        **extra_shape_props,
    )

    # Bound text element centered inside the shape
    text_padding = 8
    text_elem = _make_base_element(
        text_id, "text",
        px + text_padding, py + text_padding,
        w - 2 * text_padding, h - 2 * text_padding,
        roughness=0,
        strokeColor=text_color,
        backgroundColor="transparent",
        strokeWidth=1,
        text=shape.text,
        originalText=shape.text,
        fontSize=font_size,
        fontFamily=_FONT_FAMILY,
        textAlign=_text_align_value(shape.align),
        verticalAlign="middle",
        containerId=shape_id,
        lineHeight=1.25,
    )

    return shape_elem, text_elem


# ---------------------------------------------------------------------------
# Arrow elements
# ---------------------------------------------------------------------------

def _compute_best_anchor(
    src_p: Placement,
    tgt_p: Placement,
    user_anchor: AnchorName,
    is_source: bool,
) -> AnchorName:
    """Pick direction-correct anchor, overriding if user's would U-turn."""
    src_cx = src_p.position.x + src_p.shape.content_bbox.width / 2
    src_cy = src_p.position.y + src_p.shape.content_bbox.height / 2
    tgt_cx = tgt_p.position.x + tgt_p.shape.content_bbox.width / 2
    tgt_cy = tgt_p.position.y + tgt_p.shape.content_bbox.height / 2
    dx = tgt_cx - src_cx
    dy = tgt_cy - src_cy

    if abs(dx) > abs(dy):
        if dx > 0:
            best_src, best_tgt = AnchorName.RIGHT_CENTER, AnchorName.LEFT_CENTER
        else:
            best_src, best_tgt = AnchorName.LEFT_CENTER, AnchorName.RIGHT_CENTER
    else:
        if dy > 0:
            best_src, best_tgt = AnchorName.BOTTOM_CENTER, AnchorName.TOP_CENTER
        else:
            best_src, best_tgt = AnchorName.TOP_CENTER, AnchorName.BOTTOM_CENTER

    best = best_src if is_source else best_tgt

    # Check if user anchor would U-turn
    _UTURN = {
        AnchorName.RIGHT_CENTER: lambda ddx, ddy: ddx < -20,
        AnchorName.LEFT_CENTER: lambda ddx, ddy: ddx > 20,
        AnchorName.BOTTOM_CENTER: lambda ddx, ddy: ddy < -20,
        AnchorName.TOP_CENTER: lambda ddx, ddy: ddy > 20,
    }
    check_dx = dx if is_source else -dx
    check_dy = dy if is_source else -dy
    checker = _UTURN.get(user_anchor)
    if checker and checker(check_dx, check_dy):
        return best
    return user_anchor


def _arrow_element(
    connector: Connector,
    placements_dict: dict[str, Placement],
    canvas_padding: float,
    roughness: int = 1,
    dark: bool = False,
) -> tuple[dict, dict | None]:
    """Convert a Connector into an Excalidraw arrow element with orthogonal routing.

    Uses PlotCraft's orthogonal router to compute obstacle-avoiding waypoints,
    producing clean right-angle paths that don't cut through shapes.

    Returns (arrow_element, label_text_element_or_None).
    """
    source_p = placements_dict.get(connector.source_shape_id)
    target_p = placements_dict.get(connector.target_shape_id)

    if source_p is None or target_p is None:
        arrow = _make_base_element(connector.id, "arrow", 0, 0, 0, 0)
        arrow["points"] = [[0, 0], [0, 0]]
        arrow["startBinding"] = None
        arrow["endBinding"] = None
        arrow["startArrowhead"] = None
        arrow["endArrowhead"] = "arrow"
        return arrow, None

    # Compute direction-aware anchors (override user anchors if they'd U-turn)
    src_anchor = _compute_best_anchor(source_p, target_p, connector.source_anchor, is_source=True)
    tgt_anchor = _compute_best_anchor(source_p, target_p, connector.target_anchor, is_source=False)

    # Resolve anchors to absolute canvas positions on shape edges
    start = resolve_anchor(
        source_p.shape.kind, source_p.shape.content_bbox,
        src_anchor, source_p.position, gap=6.0,
    )
    end = resolve_anchor(
        target_p.shape.kind, target_p.shape.content_bbox,
        tgt_anchor, target_p.position, gap=6.0,
    )

    # Add canvas padding to get final positions
    start_x = start.x + canvas_padding
    start_y = start.y + canvas_padding
    end_x = end.x + canvas_padding
    end_y = end.y + canvas_padding

    # Collect obstacles (all shapes except source and target)
    obstacles: list[BBox] = []
    for sid, p in placements_dict.items():
        if sid != connector.source_shape_id and sid != connector.target_shape_id:
            if p.shape.kind != ShapeKind.NONE:
                obstacles.append(BBox(
                    p.position.x + canvas_padding,
                    p.position.y + canvas_padding,
                    p.shape.content_bbox.width,
                    p.shape.content_bbox.height,
                ))

    # Route orthogonally around obstacles
    waypoints = route_orthogonal(
        Point(start_x, start_y),
        Point(end_x, end_y),
        obstacles,
    )

    # Convert waypoints to relative points (relative to arrow origin)
    origin_x = waypoints[0].x
    origin_y = waypoints[0].y
    points = [[wp.x - origin_x, wp.y - origin_y] for wp in waypoints]

    # Compute bounding box of points for arrow width/height
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    arr_w = max(all_x) - min(all_x) if all_x else 0
    arr_h = max(all_y) - min(all_y) if all_y else 0

    # Stroke color from source shape theme
    source_theme = source_p.shape.color_theme
    palette = EXCALIDRAW_COLORS_DARK if dark else EXCALIDRAW_COLORS
    _, stroke_color = palette.get(
        source_theme, palette[ColorTheme.NEUTRAL]
    )

    # Line style
    style_map = {
        ConnectorStyle.SOLID: "solid",
        ConnectorStyle.DASHED: "dashed",
        ConnectorStyle.DOTTED: "dotted",
    }
    stroke_style = style_map.get(connector.style, "solid")

    # Line weight
    stroke_width = LINE_WEIGHT_WIDTHS.get(connector.line_weight, 2.0)

    # Arrowheads
    start_arrowhead = None
    end_arrowhead = None
    if connector.direction == ArrowDirection.FORWARD:
        end_arrowhead = "arrow"
    elif connector.direction == ArrowDirection.BACKWARD:
        start_arrowhead = "arrow"
    elif connector.direction == ArrowDirection.BOTH:
        start_arrowhead = "arrow"
        end_arrowhead = "arrow"

    # No bindings — we've computed exact edge positions and routed paths.
    # Bindings would override our carefully routed waypoints.
    arrow = _make_base_element(
        connector.id, "arrow",
        origin_x, origin_y,
        arr_w, arr_h,
        roughness=roughness,
        strokeColor=stroke_color,
        strokeWidth=stroke_width,
        strokeStyle=stroke_style,
        points=points,
        startBinding=None,
        endBinding=None,
        startArrowhead=start_arrowhead,
        endArrowhead=end_arrowhead,
    )

    # Optional label at the path midpoint
    label_elem = None
    if connector.label:
        label_id = f"{connector.id}_label"
        # Find midpoint of the path
        mid_idx = len(waypoints) // 2
        mid_wp = waypoints[mid_idx]
        label_w = len(connector.label) * 8 + 16
        label_h = 24
        label_elem = _make_base_element(
            label_id, "text",
            mid_wp.x - label_w / 2, mid_wp.y - label_h / 2,
            label_w, label_h,
            roughness=0,
            strokeColor=_TEXT_COLOR_LIGHT_ON_DARK if dark else "#555555",
            backgroundColor="transparent",
            strokeWidth=1,
            text=connector.label,
            originalText=connector.label,
            fontSize=14,
            fontFamily=_FONT_FAMILY,
            textAlign="center",
            verticalAlign="middle",
            containerId=None,
            lineHeight=1.25,
        )

    return arrow, label_elem


# ---------------------------------------------------------------------------
# Section elements
# ---------------------------------------------------------------------------

def _section_element(
    index: int,
    label: str,
    bounds: BBox,
    style: SectionStyle,
    canvas_padding: float,
    roughness: int = 1,
    dark: bool = False,
) -> list[dict]:
    """Create section background rectangle and label text elements.

    Returns a list of [background_rect, label_text].
    """
    section_id = f"section_{index}"
    label_id = f"section_{index}_label"

    sx = bounds.x + canvas_padding
    sy = bounds.y + canvas_padding

    if dark:
        section_fill = "#2C2C2C"
        section_stroke = "#8B8B8B"
        label_color = _TEXT_COLOR_LIGHT_ON_DARK
    else:
        section_fill = style.fill
        section_stroke = style.stroke
        label_color = style.label_color

    bg_rect = _make_base_element(
        section_id, "rectangle",
        sx, sy,
        bounds.width, bounds.height,
        roughness=roughness,
        strokeColor=section_stroke,
        backgroundColor=section_fill,
        strokeWidth=style.stroke_width,
        strokeStyle="dashed",
        opacity=80,
        roundness={"type": 3},
    )

    label_text = _make_base_element(
        label_id, "text",
        sx + style.padding, sy + 4,
        200, style.label_font_size * 1.5,
        roughness=0,
        strokeColor=label_color,
        backgroundColor="transparent",
        strokeWidth=1,
        text=label,
        originalText=label,
        fontSize=style.label_font_size,
        fontFamily=_FONT_FAMILY,
        textAlign="left",
        verticalAlign="top",
        containerId=None,
        lineHeight=1.25,
    )

    return [bg_rect, label_text]


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def render_excalidraw_json(
    placements: list[Placement],
    connectors: list[Connector],
    canvas_size: Size,
    sections: list[tuple[str, BBox, SectionStyle]] | None = None,
    roughness: int = 1,
    canvas_padding: float = 60.0,
    dark: bool = False,
) -> dict:
    """Convert PlotCraft's internal model to an Excalidraw JSON document.

    Two-pass element construction:
      Pass 1 — Create all shape elements, store in dict by PlotCraft shape ID.
      Pass 2 — Create all arrow elements. For each arrow, append the arrow
               binding to the source and target shapes' boundElements lists.

    Assembly order: sections -> shapes (with text) -> arrows (with labels).

    Args:
        placements: All placed shapes from the grid.
        connectors: Connector stubs (source/target/anchor metadata).
        canvas_size: Total canvas dimensions.
        sections: Optional list of (label, bounds_bbox, style) tuples.
        roughness: Excalidraw roughness level (0=smooth, 1=hand-drawn, 2=rough).
        canvas_padding: Extra padding around the diagram content in pixels.

    Returns:
        A dict representing a complete Excalidraw JSON document.
    """
    sections = sections or []
    elements: list[dict] = []

    # Build lookup from PlotCraft shape ID to placement
    placements_dict: dict[str, Placement] = {p.shape.id: p for p in placements}

    # --- Sections (drawn first, behind everything) ---
    for i, (label, bounds, style) in enumerate(sections):
        section_elems = _section_element(i, label, bounds, style, canvas_padding, roughness, dark=dark)
        elements.extend(section_elems)

    # --- Pass 1: Shapes ---
    # Track shape elements by PlotCraft shape ID for arrow binding updates
    shape_elements_by_id: dict[str, dict] = {}

    for placement in placements:
        shape_elem, text_elem = _shape_element(placement, canvas_padding, roughness, dark=dark)

        if placement.shape.kind == ShapeKind.NONE:
            # shape_elem is the free-floating text; no shape container
            elements.append(shape_elem)
        else:
            shape_elements_by_id[placement.shape.id] = shape_elem
            elements.append(shape_elem)
            if text_elem is not None:
                elements.append(text_elem)

    # --- Pass 2: Arrows (orthogonally routed, no bindings needed) ---
    for connector in connectors:
        arrow_elem, label_elem = _arrow_element(
            connector, placements_dict, canvas_padding, roughness, dark=dark,
        )
        elements.append(arrow_elem)
        if label_elem is not None:
            elements.append(label_elem)

    # --- Assemble document ---
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "plotcraft",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": CANVAS_BACKGROUND_DARK if dark else CANVAS_BACKGROUND,
            "gridSize": None,
        },
        "files": {},
    }
