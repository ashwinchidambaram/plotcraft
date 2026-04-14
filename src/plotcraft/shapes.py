from __future__ import annotations
import math
from dataclasses import dataclass
from plotcraft.types import (
    ShapeKind, TextRole, TextAlign, AnchorName, Point, Size, BBox,
    TEXT_STYLE_DEFAULTS, ROLE_SCALE_DEFAULTS, ColorTheme,
)
from plotcraft.text import measure_text, wrap_text


@dataclass(frozen=True)
class Shape:
    """An immutable shape with auto-computed geometry."""
    id: str
    kind: ShapeKind
    text: str
    role: TextRole
    align: TextAlign
    text_size: Size          # measured text bounding box
    content_bbox: BBox       # shape boundary (includes padding around text)
    wrapped_lines: tuple[str, ...]  # text lines after wrapping
    color_theme: ColorTheme

    def anchor(self, name: AnchorName) -> Point:
        """Get anchor point position relative to shape origin."""
        return self.content_bbox.anchor(name)

    def anchors(self) -> dict[AnchorName, Point]:
        """All 9 anchor points."""
        return {name: self.anchor(name) for name in AnchorName}


def resolve_anchor(
    kind: ShapeKind,
    content_bbox: BBox,
    anchor: AnchorName,
    position: Point,
    gap: float = 4.0,
) -> Point:
    """Resolve an anchor to the actual visible shape edge.

    Args:
        kind: The shape type
        content_bbox: The shape's bounding box (origin at 0,0)
        anchor: Which anchor point
        position: The shape's absolute position on canvas (top-left of bbox)
        gap: Distance to stop before the shape edge (prevents arrow overlap with stroke)

    Returns:
        Absolute canvas position of the anchor on the visible shape edge,
        offset by gap in the outward direction.
    """
    w = content_bbox.width
    h = content_bbox.height
    cx = w / 2
    cy = h / 2

    # Compute local (relative to bbox origin) resolved point before gap
    if kind in (ShapeKind.RECT, ShapeKind.SQUARE, ShapeKind.NONE):
        # Shape fills the bbox — bbox anchors are exact
        local = content_bbox.anchor(anchor)

    elif kind == ShapeKind.DIAMOND:
        # Visible diamond has vertices at midpoints of bbox edges:
        #   top=(cx,0), right=(w,cy), bottom=(cx,h), left=(0,cy)
        top    = Point(cx, 0)
        right  = Point(w, cy)
        bottom = Point(cx, h)
        left   = Point(0, cy)

        match anchor:
            case AnchorName.TOP_CENTER:
                local = top
            case AnchorName.RIGHT_CENTER:
                local = right
            case AnchorName.BOTTOM_CENTER:
                local = bottom
            case AnchorName.LEFT_CENTER:
                local = left
            case AnchorName.CENTER:
                local = Point(cx, cy)
            case AnchorName.TOP_LEFT:
                # Midpoint of diamond edge from top vertex to left vertex
                local = Point((top.x + left.x) / 2, (top.y + left.y) / 2)
            case AnchorName.TOP_RIGHT:
                # Midpoint of diamond edge from top vertex to right vertex
                local = Point((top.x + right.x) / 2, (top.y + right.y) / 2)
            case AnchorName.BOTTOM_RIGHT:
                # Midpoint of diamond edge from bottom vertex to right vertex
                local = Point((bottom.x + right.x) / 2, (bottom.y + right.y) / 2)
            case AnchorName.BOTTOM_LEFT:
                # Midpoint of diamond edge from bottom vertex to left vertex
                local = Point((bottom.x + left.x) / 2, (bottom.y + left.y) / 2)

    elif kind == ShapeKind.CIRCLE:
        # Circle: center at (cx, cy), radius = w/2 (bbox is square for circles)
        r = w / 2
        # Direction from center to the corresponding bbox anchor
        bbox_pt = content_bbox.anchor(anchor)
        dx = bbox_pt.x - cx
        dy = bbox_pt.y - cy
        if anchor == AnchorName.CENTER or (dx == 0 and dy == 0):
            local = Point(cx, cy)
        else:
            length = math.sqrt(dx * dx + dy * dy)
            ux, uy = dx / length, dy / length
            local = Point(cx + r * ux, cy + r * uy)

    elif kind == ShapeKind.OVAL:
        # Ellipse: center at (cx, cy), rx = w/2, ry = h/2
        rx = w / 2
        ry = h / 2
        # Direction from center to the corresponding bbox anchor
        bbox_pt = content_bbox.anchor(anchor)
        dx = bbox_pt.x - cx
        dy = bbox_pt.y - cy
        if anchor == AnchorName.CENTER or (dx == 0 and dy == 0):
            local = Point(cx, cy)
        else:
            # Angle from center to bbox anchor point
            theta = math.atan2(dy, dx)
            local = Point(cx + rx * math.cos(theta), cy + ry * math.sin(theta))

    else:
        # Fallback: treat as rect
        local = content_bbox.anchor(anchor)

    # Apply outward gap: compute unit vector from shape center to the resolved local point
    center_local = Point(cx, cy)
    dx = local.x - center_local.x
    dy = local.y - center_local.y
    dist = math.sqrt(dx * dx + dy * dy)
    if dist > 0:
        ux, uy = dx / dist, dy / dist
        gapped_local = Point(local.x + gap * ux, local.y + gap * uy)
    else:
        gapped_local = local

    # Convert from local (bbox-relative) to absolute canvas coordinates
    return Point(position.x + gapped_local.x, position.y + gapped_local.y)


def create_shape(
    id: str,
    text: str,
    kind: ShapeKind = ShapeKind.RECT,
    role: TextRole = TextRole.BODY,
    align: TextAlign = TextAlign.CENTER,
    max_text_width: float = 200.0,
    padding: float = 20.0,
    color_theme: ColorTheme = ColorTheme.NEUTRAL,
) -> Shape:
    """Create a shape that auto-sizes around its text content."""
    style = TEXT_STYLE_DEFAULTS[role]
    role_scale = ROLE_SCALE_DEFAULTS[role]

    # Measure and wrap text
    lines = wrap_text(text, style, max_text_width)
    text_size = measure_text(text, style, max_width=max_text_width)

    # Apply padding multiplier from role scale
    scaled_padding = padding * role_scale.padding_multiplier

    # Compute content_bbox based on shape kind
    if kind == ShapeKind.RECT:
        width = text_size.width + 2 * scaled_padding
        height = text_size.height + 2 * scaled_padding
        content_bbox = BBox(0, 0, width, height)

    elif kind == ShapeKind.SQUARE:
        side = max(text_size.width, text_size.height) + 2 * scaled_padding
        content_bbox = BBox(0, 0, side, side)

    elif kind == ShapeKind.CIRCLE:
        # Diameter must enclose the text diagonal
        diagonal = math.sqrt(text_size.width**2 + text_size.height**2)
        diameter = diagonal + 2 * scaled_padding
        content_bbox = BBox(0, 0, diameter, diameter)

    elif kind == ShapeKind.OVAL:
        # Like rect but with extra padding (1.4x) to keep text inside ellipse
        oval_padding = scaled_padding * 1.4
        width = text_size.width + 2 * oval_padding
        height = text_size.height + 2 * oval_padding
        content_bbox = BBox(0, 0, width, height)

    elif kind == ShapeKind.DIAMOND:
        width = text_size.width * 1.5 + 2 * scaled_padding
        height = text_size.height * 1.5 + 2 * scaled_padding
        content_bbox = BBox(0, 0, width, height)

    elif kind == ShapeKind.NONE:
        # Free-floating text: minimal padding for bounding box only
        none_padding = scaled_padding * 0.3
        width = text_size.width + 2 * none_padding
        height = text_size.height + 2 * none_padding
        content_bbox = BBox(0, 0, width, height)

    # Apply minimum dimensions from role scale
    final_width = max(content_bbox.width, role_scale.min_width)
    final_height = max(content_bbox.height, role_scale.min_height)
    content_bbox = BBox(0, 0, final_width, final_height)

    return Shape(
        id=id,
        kind=kind,
        text=text,
        role=role,
        align=align,
        text_size=text_size,
        content_bbox=content_bbox,
        wrapped_lines=tuple(lines),
        color_theme=color_theme,
    )
