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
