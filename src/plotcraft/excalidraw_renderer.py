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
    ArrowDirection,
    ConnectorStyle,
    LINE_WEIGHT_WIDTHS,
    ColorTheme,
    SectionStyle,
    Size,
    BBox,
)
from plotcraft.grid import Placement
from plotcraft.connectors import Connector


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

def _arrow_element(
    connector: Connector,
    placements_dict: dict[str, Placement],
    canvas_padding: float,
    roughness: int = 1,
    dark: bool = False,
) -> tuple[dict, dict | None]:
    """Convert a Connector into an Excalidraw arrow element and optional label.

    Returns (arrow_element, label_text_element_or_None).
    """
    source_p = placements_dict.get(connector.source_shape_id)
    target_p = placements_dict.get(connector.target_shape_id)

    if source_p is None or target_p is None:
        # Cannot render arrow without both endpoints; skip gracefully
        arrow = _make_base_element(connector.id, "arrow", 0, 0, 0, 0)
        arrow["points"] = [[0, 0], [0, 0]]
        arrow["startBinding"] = None
        arrow["endBinding"] = None
        arrow["startArrowhead"] = None
        arrow["endArrowhead"] = "arrow"
        return arrow, None

    # Source and target centers
    src_cx = source_p.position.x + source_p.shape.content_bbox.width / 2 + canvas_padding
    src_cy = source_p.position.y + source_p.shape.content_bbox.height / 2 + canvas_padding
    tgt_cx = target_p.position.x + target_p.shape.content_bbox.width / 2 + canvas_padding
    tgt_cy = target_p.position.y + target_p.shape.content_bbox.height / 2 + canvas_padding

    dx = tgt_cx - src_cx
    dy = tgt_cy - src_cy

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
    # NONE: both stay None

    source_shape_elem_id = f"exc_shape_{connector.source_shape_id}"
    target_shape_elem_id = f"exc_shape_{connector.target_shape_id}"

    arrow = _make_base_element(
        connector.id, "arrow",
        src_cx, src_cy,
        abs(dx), abs(dy),
        roughness=roughness,
        strokeColor=stroke_color,
        strokeWidth=stroke_width,
        strokeStyle=stroke_style,
        points=[[0, 0], [dx, dy]],
        startBinding={
            "elementId": source_shape_elem_id,
            "focus": 0,
            "gap": 2,
            "fixedPoint": None,
        },
        endBinding={
            "elementId": target_shape_elem_id,
            "focus": 0,
            "gap": 2,
            "fixedPoint": None,
        },
        startArrowhead=start_arrowhead,
        endArrowhead=end_arrowhead,
    )

    # Optional label at the midpoint
    label_elem = None
    if connector.label:
        label_id = f"{connector.id}_label"
        mid_x = src_cx + dx / 2
        mid_y = src_cy + dy / 2
        label_w = len(connector.label) * 8 + 16
        label_h = 24
        label_elem = _make_base_element(
            label_id, "text",
            mid_x - label_w / 2, mid_y - label_h / 2,
            label_w, label_h,
            roughness=0,
            strokeColor="#555555",
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

    # --- Pass 2: Arrows ---
    arrow_elements: list[dict] = []

    for connector in connectors:
        arrow_elem, label_elem = _arrow_element(
            connector, placements_dict, canvas_padding, roughness, dark=dark,
        )

        # Add arrow binding to source and target shape boundElements
        arrow_binding = {"id": connector.id, "type": "arrow"}

        source_shape = shape_elements_by_id.get(connector.source_shape_id)
        if source_shape is not None:
            bound = source_shape.get("boundElements")
            if bound is None:
                source_shape["boundElements"] = [arrow_binding]
            else:
                bound.append(arrow_binding)

        target_shape = shape_elements_by_id.get(connector.target_shape_id)
        if target_shape is not None:
            bound = target_shape.get("boundElements")
            if bound is None:
                target_shape["boundElements"] = [arrow_binding]
            else:
                bound.append(arrow_binding)

        arrow_elements.append(arrow_elem)
        if label_elem is not None:
            arrow_elements.append(label_elem)

    elements.extend(arrow_elements)

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
