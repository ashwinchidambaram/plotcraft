from __future__ import annotations
from plotcraft.types import ShapeKind, TextAlign, ArrowDirection, Size, Point, BBox, TEXT_STYLE_DEFAULTS, COLOR_DEFAULTS, ConnectorStyle, LINE_WEIGHT_WIDTHS, SectionStyle, TextRole
from plotcraft.grid import Placement
from plotcraft.connectors import Connector
from plotcraft.wobble import Wobbler


_CORNER_RADIUS = 8.0
_SHAPE_FILL = "#f8f9fa"
_SHAPE_STROKE = "#333333"
_SHAPE_STROKE_WIDTH = 2.0
_TEXT_COLOR = "#222222"
_CONNECTOR_COLOR = "#555555"
_CONNECTOR_WIDTH = 2.0
_CANVAS_PADDING = 24.0
_CANVAS_COLOR = "#fdf6e3"


class SvgRenderer:
    def __init__(self, background: str = _CANVAS_COLOR, wobbler: Wobbler | None = None):
        self._background = background
        self._wobbler = wobbler

    def render_diagram(
        self,
        placements: list[Placement],
        connectors: list[Connector],
        canvas_size: Size,
        sections: list[tuple[str, BBox, SectionStyle]] | None = None,
        structure_fragments: list[str] | None = None,
    ) -> str:
        """Complete SVG document string."""
        w = canvas_size.width + 2 * _CANVAS_PADDING
        h = canvas_size.height + 2 * _CANVAS_PADDING

        parts = []
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        )

        # Defs (Google Fonts + arrowhead markers)
        parts.append("  <defs>")
        parts.append(
            "    <style>\n"
            "      @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=Patrick+Hand&amp;family=Indie+Flower&amp;display=swap');\n"
            "    </style>"
        )
        parts.append(self._arrowhead_marker())
        parts.append(self._arrowhead_marker_start())
        parts.append("  </defs>")

        # Background
        parts.append(
            f'  <rect width="{w}" height="{h}" fill="{self._background}" />'
        )

        # Group with padding offset
        parts.append(f'  <g transform="translate({_CANVAS_PADDING}, {_CANVAS_PADDING})">')

        # Render sections (behind everything)
        if sections:
            for label, bounds, style in sections:
                parts.append(self.render_section(label, bounds, style))

        # Render connectors first (behind shapes)
        for conn in connectors:
            parts.append(self.render_connector(conn))

        # Render shapes
        for placement in placements:
            parts.append(self.render_shape(placement))

        # Render structure fragments (timelines, trees)
        if structure_fragments:
            for fragment in structure_fragments:
                if fragment:
                    parts.append(fragment)

        parts.append("  </g>")
        parts.append("</svg>")

        return "\n".join(parts)

    def render_shape(self, placement: Placement) -> str:
        """SVG elements for a single placed shape."""
        shape = placement.shape
        pos = placement.position
        style = TEXT_STYLE_DEFAULTS[shape.role]
        palette = COLOR_DEFAULTS[shape.color_theme]
        fill = palette.fill
        stroke = palette.stroke
        fill_opacity = palette.fill_opacity

        parts = []
        parts.append(f'    <g id="shape-{shape.id}">')

        # Draw the shape (skip for NONE — free-floating text)
        if shape.kind == ShapeKind.NONE:
            pass  # No visible shape element
        elif shape.kind == ShapeKind.RECT or shape.kind == ShapeKind.SQUARE:
            parts.append(self._render_rect(
                BBox(pos.x, pos.y, shape.content_bbox.width, shape.content_bbox.height),
                fill=fill, stroke=stroke, fill_opacity=fill_opacity,
            ))
        elif shape.kind == ShapeKind.CIRCLE:
            center = Point(
                pos.x + shape.content_bbox.width / 2,
                pos.y + shape.content_bbox.height / 2,
            )
            radius = shape.content_bbox.width / 2
            parts.append(self._render_circle(center, radius, fill=fill, stroke=stroke, fill_opacity=fill_opacity))
        elif shape.kind == ShapeKind.DIAMOND:
            parts.append(self._render_diamond(
                BBox(pos.x, pos.y, shape.content_bbox.width, shape.content_bbox.height),
                fill=fill, stroke=stroke, fill_opacity=fill_opacity,
            ))
        elif shape.kind == ShapeKind.OVAL:
            center = Point(
                pos.x + shape.content_bbox.width / 2,
                pos.y + shape.content_bbox.height / 2,
            )
            rx = shape.content_bbox.width / 2
            ry = shape.content_bbox.height / 2
            parts.append(self._render_ellipse(center, rx, ry, fill=fill, stroke=stroke, fill_opacity=fill_opacity))

        # Draw the text (always vertically centered, horizontal per shape.align)
        text_center = Point(
            pos.x + shape.content_bbox.width / 2,
            pos.y + shape.content_bbox.height / 2,
        )
        parts.append(self._render_text(
            shape.wrapped_lines, style, text_center,
            shape.content_bbox.width, shape.align, pos.x,
        ))

        parts.append("    </g>")
        return "\n".join(parts)

    def render_connector(self, connector: Connector) -> str:
        """SVG path for a connector with arrowhead and optional label."""
        import math
        parts = []

        path_points = connector.path_points

        if self._is_orthogonal_path(path_points):
            # Apply wobble to orthogonal waypoints before converting to SVG path
            if self._wobbler:
                path_points = self._wobbler.wobble_bezier_points(path_points)
            path_d = self._render_orthogonal_path(path_points)
        else:
            # Apply wobble to bezier control points when wobbler is available
            if self._wobbler:
                path_points = self._wobbler.wobble_bezier_points(path_points)
            path_d = self._render_bezier_path(path_points)

        # Build marker attributes based on direction
        direction = getattr(connector, 'direction', ArrowDirection.FORWARD)
        marker_attrs = ""
        if direction == ArrowDirection.FORWARD:
            marker_attrs = ' marker-end="url(#arrowhead)"'
        elif direction == ArrowDirection.BACKWARD:
            marker_attrs = ' marker-start="url(#arrowhead-start)"'
        elif direction == ArrowDirection.BOTH:
            marker_attrs = ' marker-start="url(#arrowhead-start)" marker-end="url(#arrowhead)"'
        # NONE: no markers

        stroke_width = LINE_WEIGHT_WIDTHS[connector.line_weight]

        dasharray_attr = ""
        if connector.style == ConnectorStyle.DASHED:
            dasharray_attr = ' stroke-dasharray="8 4"'
        elif connector.style == ConnectorStyle.DOTTED:
            dasharray_attr = ' stroke-dasharray="2 4"'

        parts.append(
            f'    <path id="conn-{connector.id}" d="{path_d}" '
            f'fill="none" stroke="{_CONNECTOR_COLOR}" '
            f'stroke-width="{stroke_width}"{dasharray_attr}'
            f'{marker_attrs} />'
        )

        # Render label at the midpoint of the path
        if connector.label and len(connector.path_points) >= 2:
            if self._is_orthogonal_path(connector.path_points):
                mid = self._orthogonal_midpoint(path_points)
                # For orthogonal paths, offset label perpendicular to the dominant direction
                # Find segment containing the midpoint for tangent calculation
                tangent = self._orthogonal_tangent_at_midpoint(path_points)
            else:
                mid = self._bezier_midpoint(path_points)
                tangent = self._bezier_tangent(path_points)

            # Perpendicular to tangent (rotate 90° CCW → label goes "above/left")
            length = math.sqrt(tangent.x ** 2 + tangent.y ** 2) or 1.0
            perp_x = -tangent.y / length
            perp_y = tangent.x / length

            # Offset label away from the line by 14px
            offset = 14.0
            label_x = mid.x + perp_x * offset
            label_y = mid.y + perp_y * offset

            # Small background rect behind the text so the line never crosses it
            label_text = _escape_xml(connector.label)
            # Approximate label width: ~7px per char at font-size 12
            approx_w = len(connector.label) * 7.0 + 8
            approx_h = 16.0
            body_font = TEXT_STYLE_DEFAULTS[TextRole.BODY].font_family
            parts.append(
                f'    <rect x="{label_x - approx_w / 2}" y="{label_y - approx_h / 2}" '
                f'width="{approx_w}" height="{approx_h}" rx="3" ry="3" '
                f'fill="{_CANVAS_COLOR}" stroke="none" />'
            )
            parts.append(
                f'    <text x="{label_x}" y="{label_y}" '
                f'text-anchor="middle" dominant-baseline="central" '
                f'font-family="{body_font}" font-size="12" '
                f'fill="{_TEXT_COLOR}">{label_text}</text>'
            )

        return "\n".join(parts)

    def _render_rect(self, bbox: BBox, rx: float = _CORNER_RADIUS,
                     fill: str = _SHAPE_FILL, stroke: str = _SHAPE_STROKE,
                     fill_opacity: float = 1.0) -> str:
        opacity_attr = f' fill-opacity="{fill_opacity}"' if fill_opacity != 1.0 else f' fill-opacity="{fill_opacity}"'
        if self._wobbler:
            d = self._wobbler.wobble_rect(bbox.x, bbox.y, bbox.width, bbox.height, rx)
            return (
                f'      <path d="{d}" '
                f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
                f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
            )
        return (
            f'      <rect x="{bbox.x}" y="{bbox.y}" '
            f'width="{bbox.width}" height="{bbox.height}" '
            f'rx="{rx}" ry="{rx}" '
            f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
            f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
        )

    def _render_circle(self, center: Point, radius: float,
                       fill: str = _SHAPE_FILL, stroke: str = _SHAPE_STROKE,
                       fill_opacity: float = 1.0) -> str:
        opacity_attr = f' fill-opacity="{fill_opacity}"'
        if self._wobbler:
            d = self._wobbler.wobble_circle(center.x, center.y, radius)
            return (
                f'      <path d="{d}" '
                f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
                f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
            )
        return (
            f'      <circle cx="{center.x}" cy="{center.y}" r="{radius}" '
            f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
            f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
        )

    def _render_diamond(self, bbox: BBox,
                        fill: str = _SHAPE_FILL, stroke: str = _SHAPE_STROKE,
                        fill_opacity: float = 1.0) -> str:
        opacity_attr = f' fill-opacity="{fill_opacity}"'
        cx = bbox.x + bbox.width / 2
        cy = bbox.y + bbox.height / 2
        half_w = bbox.width / 2
        half_h = bbox.height / 2
        if self._wobbler:
            d = self._wobbler.wobble_diamond(cx, cy, half_w, half_h)
            return (
                f'      <path d="{d}" '
                f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
                f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
            )
        top = f"{cx},{bbox.y}"
        right = f"{bbox.x + bbox.width},{cy}"
        bottom = f"{cx},{bbox.y + bbox.height}"
        left = f"{bbox.x},{cy}"
        points = f"{top} {right} {bottom} {left}"
        return (
            f'      <polygon points="{points}" '
            f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
            f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
        )

    def _render_ellipse(self, center: Point, rx: float, ry: float,
                        fill: str = _SHAPE_FILL, stroke: str = _SHAPE_STROKE,
                        fill_opacity: float = 1.0) -> str:
        opacity_attr = f' fill-opacity="{fill_opacity}"'
        if self._wobbler:
            d = self._wobbler.wobble_ellipse(center.x, center.y, rx, ry)
            return (
                f'      <path d="{d}" '
                f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
                f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
            )
        return (
            f'      <ellipse cx="{center.x}" cy="{center.y}" '
            f'rx="{rx}" ry="{ry}" '
            f'fill="{fill}"{opacity_attr} stroke="{stroke}" '
            f'stroke-width="{_SHAPE_STROKE_WIDTH}" />'
        )

    def _render_text(
        self, lines: tuple[str, ...], style, center: Point,
        shape_width: float, align: TextAlign = TextAlign.CENTER,
        shape_x: float = 0.0,
    ) -> str:
        """Render text as <text> with <tspan> per line, always vertically centered."""
        font_weight = f' font-weight="{style.font_weight}"' if style.font_weight != "normal" else ""
        line_h = style.font_size * style.line_height
        total_height = len(lines) * line_h

        # Vertical centering: SVG <tspan y="..."> positions the text BASELINE,
        # not the visual center. To truly center, we need to shift down by
        # ~0.35 * font_size (approx half the cap height for Arial).
        baseline_offset = style.font_size * 0.35
        first_line_y = center.y - total_height / 2 + line_h / 2 + baseline_offset

        # Horizontal alignment
        padding = 20.0  # text inset from shape edge for left/right align
        if align == TextAlign.LEFT:
            svg_anchor = "start"
            tspan_x = shape_x + padding
        elif align == TextAlign.RIGHT:
            svg_anchor = "end"
            tspan_x = shape_x + shape_width - padding
        else:  # CENTER
            svg_anchor = "middle"
            tspan_x = center.x

        parts = []
        parts.append(
            f'      <text text-anchor="{svg_anchor}" '
            f'font-family="{style.font_family}" '
            f'font-size="{style.font_size}"{font_weight} '
            f'fill="{_TEXT_COLOR}">'
        )

        for i, line in enumerate(lines):
            y = first_line_y + i * line_h
            parts.append(
                f'        <tspan x="{tspan_x}" y="{y}">'
                f'{_escape_xml(line)}</tspan>'
            )

        parts.append("      </text>")
        return "\n".join(parts)

    def _is_orthogonal_path(self, points: tuple[Point, ...]) -> bool:
        """Check if path points form an orthogonal (all-right-angle) path.

        Bezier paths from route_connector always have exactly 4 or 5 points, so
        those are never treated as orthogonal even if their control points happen
        to be axis-aligned.
        """
        n = len(points)
        if n < 2:
            return False
        # 4-point and 5-point paths are cubic bezier curves from route_connector
        if n == 4 or n == 5:
            return False
        for i in range(n - 1):
            dx = abs(points[i + 1].x - points[i].x)
            dy = abs(points[i + 1].y - points[i].y)
            # Each segment must be primarily horizontal or vertical
            if dx > 1e-3 and dy > 1e-3:
                return False
        return True

    def _render_orthogonal_path(self, points: tuple[Point, ...]) -> str:
        """Generate SVG path d attribute from orthogonal waypoints with rounded corners."""
        from plotcraft.routing import orthogonal_path_to_svg
        waypoints = list(points)
        return orthogonal_path_to_svg(waypoints, corner_radius=8.0)

    def _orthogonal_midpoint(self, points: tuple[Point, ...]) -> Point:
        """Compute the midpoint of an orthogonal path by walking segment lengths."""
        import math
        if len(points) < 2:
            return points[0]

        # Compute total length
        total = 0.0
        lengths: list[float] = []
        for i in range(len(points) - 1):
            seg_len = math.sqrt(
                (points[i + 1].x - points[i].x) ** 2
                + (points[i + 1].y - points[i].y) ** 2
            )
            lengths.append(seg_len)
            total += seg_len

        # Walk to 50% of total length
        target = total / 2.0
        accumulated = 0.0
        for i, seg_len in enumerate(lengths):
            if accumulated + seg_len >= target:
                t = (target - accumulated) / seg_len if seg_len > 0 else 0.0
                x = points[i].x + t * (points[i + 1].x - points[i].x)
                y = points[i].y + t * (points[i + 1].y - points[i].y)
                return Point(x, y)
            accumulated += seg_len

        # Fallback: last point
        return points[-1]

    def _orthogonal_tangent_at_midpoint(self, points: tuple[Point, ...]) -> Point:
        """Return the tangent direction at the midpoint of an orthogonal path."""
        import math
        if len(points) < 2:
            return Point(1.0, 0.0)

        # Find the segment containing the midpoint
        total = 0.0
        lengths: list[float] = []
        for i in range(len(points) - 1):
            seg_len = math.sqrt(
                (points[i + 1].x - points[i].x) ** 2
                + (points[i + 1].y - points[i].y) ** 2
            )
            lengths.append(seg_len)
            total += seg_len

        target = total / 2.0
        accumulated = 0.0
        for i, seg_len in enumerate(lengths):
            if accumulated + seg_len >= target:
                dx = points[i + 1].x - points[i].x
                dy = points[i + 1].y - points[i].y
                return Point(dx, dy)
            accumulated += seg_len

        # Fallback: direction from first to last
        return Point(points[-1].x - points[0].x, points[-1].y - points[0].y)

    def _render_bezier_path(self, points: tuple[Point, ...]) -> str:
        """Generate SVG path d attribute from control points."""
        if len(points) < 2:
            return ""

        if len(points) == 4:
            # Single cubic bezier: M start C cp1 cp2 end
            return (
                f"M {points[0].x} {points[0].y} "
                f"C {points[1].x} {points[1].y}, "
                f"{points[2].x} {points[2].y}, "
                f"{points[3].x} {points[3].y}"
            )

        if len(points) == 5:
            # Two cubic beziers via waypoint
            # First: start -> cp1 -> waypoint (use cp1 as both control points for first curve)
            # Second: waypoint -> cp2 -> end
            return (
                f"M {points[0].x} {points[0].y} "
                f"C {points[1].x} {points[1].y}, "
                f"{points[2].x} {points[2].y}, "
                f"{points[2].x} {points[2].y} "
                f"C {points[2].x} {points[2].y}, "
                f"{points[3].x} {points[3].y}, "
                f"{points[4].x} {points[4].y}"
            )

        # Fallback: polyline through all points
        d = f"M {points[0].x} {points[0].y}"
        for p in points[1:]:
            d += f" L {p.x} {p.y}"
        return d

    def _bezier_tangent(self, points: tuple[Point, ...]) -> Point:
        """Approximate tangent vector at t=0.5 of the bezier curve."""
        if len(points) == 4:
            t = 0.5
            p0, p1, p2, p3 = points
            # Derivative of cubic bezier at t
            dx = 3*(1-t)**2*(p1.x-p0.x) + 6*(1-t)*t*(p2.x-p1.x) + 3*t**2*(p3.x-p2.x)
            dy = 3*(1-t)**2*(p1.y-p0.y) + 6*(1-t)*t*(p2.y-p1.y) + 3*t**2*(p3.y-p2.y)
            return Point(dx, dy)
        # Fallback: direction from first to last point
        return Point(points[-1].x - points[0].x, points[-1].y - points[0].y)

    def _bezier_midpoint(self, points: tuple[Point, ...]) -> Point:
        """Approximate midpoint of a bezier curve (t=0.5)."""
        if len(points) == 4:
            # Cubic bezier at t=0.5
            t = 0.5
            p0, p1, p2, p3 = points
            x = (1-t)**3 * p0.x + 3*(1-t)**2*t * p1.x + 3*(1-t)*t**2 * p2.x + t**3 * p3.x
            y = (1-t)**3 * p0.y + 3*(1-t)**2*t * p1.y + 3*(1-t)*t**2 * p2.y + t**3 * p3.y
            return Point(x, y)
        # For other lengths, use geometric center
        avg_x = sum(p.x for p in points) / len(points)
        avg_y = sum(p.y for p in points) / len(points)
        return Point(avg_x, avg_y)

    def _arrowhead_marker(self) -> str:
        if self._wobbler:
            d = self._wobbler.wobble_polygon([(0, 0), (12, 4), (0, 8)], use_lines=True)
            inner = f'      <path d="{d}" fill="{_CONNECTOR_COLOR}" />'
        else:
            inner = f'      <polygon points="0 0, 12 4, 0 8" fill="{_CONNECTOR_COLOR}" />'
        return (
            '    <marker id="arrowhead" markerWidth="12" markerHeight="8" '
            'refX="12" refY="4" orient="auto" markerUnits="strokeWidth">\n'
            f'{inner}\n'
            '    </marker>'
        )

    def render_section(self, label: str, bounds: BBox, style: SectionStyle) -> str:
        """Render a section background rectangle with a label."""
        parts = []
        if self._wobbler:
            d = self._wobbler.wobble_rect(
                bounds.x, bounds.y, bounds.width, bounds.height, style.corner_radius
            )
            parts.append(
                f'      <path d="{d}" '
                f'fill="{style.fill}" stroke="{style.stroke}" '
                f'stroke-width="{style.stroke_width}" />'
            )
        else:
            parts.append(
                f'      <rect x="{bounds.x}" y="{bounds.y}" '
                f'width="{bounds.width}" height="{bounds.height}" '
                f'rx="{style.corner_radius}" ry="{style.corner_radius}" '
                f'fill="{style.fill}" stroke="{style.stroke}" '
                f'stroke-width="{style.stroke_width}" />'
            )
        # Label at top-left inside the section
        label_x = bounds.x + style.padding
        label_y = bounds.y + style.label_font_size + 4.0
        title_font = TEXT_STYLE_DEFAULTS[TextRole.TITLE].font_family
        parts.append(
            f'      <text x="{label_x}" y="{label_y}" '
            f'font-family="{title_font}" font-size="{style.label_font_size}" '
            f'font-weight="bold" fill="{style.label_color}">'
            f'{_escape_xml(label)}</text>'
        )
        return "\n".join(parts)

    def _arrowhead_marker_start(self) -> str:
        if self._wobbler:
            d = self._wobbler.wobble_polygon([(0, 0), (12, 4), (0, 8)], use_lines=True)
            inner = f'      <path d="{d}" fill="{_CONNECTOR_COLOR}" />'
        else:
            inner = f'      <polygon points="0 0, 12 4, 0 8" fill="{_CONNECTOR_COLOR}" />'
        return (
            '    <marker id="arrowhead-start" markerWidth="12" markerHeight="8" '
            'refX="0" refY="4" orient="auto-start-reverse" markerUnits="strokeWidth">\n'
            f'{inner}\n'
            '    </marker>'
        )


def _escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
