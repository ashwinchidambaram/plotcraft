"""Wobble engine — seeded random noise for hand-drawn SVG paths.

Converts geometric SVG primitives (rect, circle, ellipse, diamond, polygon)
into <path> elements with wobbly edges, using a seeded RNG so the same diagram
always produces the same output.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from plotcraft.types import Point


@dataclass(frozen=True)
class WobbleConfig:
    """Configuration for the wobble engine."""
    seed: int = 42
    amplitude: float = 2.0  # max noise in pixels (1-3px range typical)
    enabled: bool = True


def _smooth_bezier_path(points: list[Point], closed: bool = True) -> str:
    """Convert a list of points into a smooth cubic bezier SVG path string.

    Uses a Catmull-Rom-like approach: for each point, control points are placed
    along the direction from the previous to the next point, at ~1/3 of the
    segment length. This produces smooth curves through all points.
    """
    n = len(points)
    if n < 2:
        return ""

    def ctrl_points(prev: Point, curr: Point, nxt: Point, tension: float = 0.33) -> tuple[Point, Point]:
        """Return (cp_in, cp_out) for curr, given prev and next points."""
        dx = nxt.x - prev.x
        dy = nxt.y - prev.y
        d_in = math.hypot(curr.x - prev.x, curr.y - prev.y)
        d_out = math.hypot(nxt.x - curr.x, nxt.y - curr.y)
        total = math.hypot(dx, dy)
        if total == 0:
            return curr, curr
        # Unit tangent direction
        ux, uy = dx / total, dy / total
        cp_in = Point(curr.x - ux * d_in * tension, curr.y - uy * d_in * tension)
        cp_out = Point(curr.x + ux * d_out * tension, curr.y + uy * d_out * tension)
        return cp_in, cp_out

    # Pre-compute control points for each point
    cps_out: list[Point] = []
    cps_in: list[Point] = []

    for i in range(n):
        if closed:
            prev = points[(i - 1) % n]
            nxt = points[(i + 1) % n]
        else:
            prev = points[max(i - 1, 0)]
            nxt = points[min(i + 1, n - 1)]
        cp_in, cp_out = ctrl_points(prev, points[i], nxt)
        cps_in.append(cp_in)
        cps_out.append(cp_out)

    def fmt(v: float) -> str:
        return f"{v:.2f}"

    p0 = points[0]
    parts = [f"M {fmt(p0.x)} {fmt(p0.y)}"]

    if closed:
        segments = n
    else:
        segments = n - 1

    for i in range(segments):
        curr_idx = i
        next_idx = (i + 1) % n
        cp1 = cps_out[curr_idx]
        cp2 = cps_in[next_idx]
        p = points[next_idx]
        parts.append(
            f"C {fmt(cp1.x)} {fmt(cp1.y)} {fmt(cp2.x)} {fmt(cp2.y)} {fmt(p.x)} {fmt(p.y)}"
        )

    if closed:
        parts.append("Z")

    return " ".join(parts)


class Wobbler:
    """Applies seeded random noise to SVG geometric primitives, producing
    hand-drawn-style <path> d-attribute strings.
    """

    def __init__(self, config: WobbleConfig | None = None) -> None:
        if config is None:
            config = WobbleConfig()
        self._config = config
        self._rng = random.Random(config.seed)

    # ------------------------------------------------------------------
    # Core noise primitive
    # ------------------------------------------------------------------

    def wobble_point(self, point: Point, amplitude: float | None = None) -> Point:
        """Add random noise in [-amp, +amp] to both x and y coordinates.

        If amplitude is None, uses self._config.amplitude.
        If not enabled, returns point unchanged.
        """
        if not self._config.enabled:
            return point
        amp = amplitude if amplitude is not None else self._config.amplitude
        dx = self._rng.uniform(-amp, amp)
        dy = self._rng.uniform(-amp, amp)
        return Point(point.x + dx, point.y + dy)

    # ------------------------------------------------------------------
    # Shape path generators
    # ------------------------------------------------------------------

    def wobble_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        corner_radius: float = 8.0,
        segments_per_side: int = 4,
    ) -> str:
        """Return SVG path d-string for a wobbly rounded rectangle.

        Samples segments_per_side points along each of the 4 straight sides,
        plus a few points around each rounded corner arc, then connects them
        with cubic bezier curves for a smooth hand-drawn look.
        """
        r = min(corner_radius, width / 2, height / 2)
        # Corner arc sampling: number of intermediate points per corner arc
        arc_segments = max(2, int(r / 4))

        points: list[Point] = []

        def sample_arc(
            cx: float, cy: float, start_angle: float, end_angle: float, n: int
        ) -> list[Point]:
            """Sample n+1 points along an arc (inclusive of start, exclusive of end)."""
            pts = []
            for k in range(n):
                t = k / n
                angle = start_angle + t * (end_angle - start_angle)
                pts.append(self.wobble_point(Point(cx + r * math.cos(angle), cy + r * math.sin(angle))))
            return pts

        def sample_side(p0: Point, p1: Point, n: int) -> list[Point]:
            """Sample n-1 interior points between p0 and p1 (exclusive of endpoints)."""
            pts = []
            for k in range(1, n):
                t = k / n
                raw = Point(p0.x + t * (p1.x - p0.x), p0.y + t * (p1.y - p0.y))
                pts.append(self.wobble_point(raw))
            return pts

        # Rectangle corners (centers of the rounding arcs)
        # top-left corner arc: from left-side tangent to top-side tangent
        # angles: π → 3π/2  (going from left to top)
        # We go clockwise: top-right → bottom-right → bottom-left → top-left

        # Top side: from (x+r, y) to (x+w-r, y)
        tl = Point(x + r, y)
        tr = Point(x + width - r, y)
        # Right side: from (x+w, y+r) to (x+w, y+h-r)
        rt = Point(x + width, y + r)
        rb = Point(x + width, y + height - r)
        # Bottom side: from (x+w-r, y+h) to (x+r, y+h)
        br = Point(x + width - r, y + height)
        bl = Point(x + r, y + height)
        # Left side: from (x, y+h-r) to (x, y+r)
        lb = Point(x, y + height - r)
        la = Point(x, y + r)

        # Top-right corner center
        c_tr = (x + width - r, y + r)
        # Bottom-right corner center
        c_br = (x + width - r, y + height - r)
        # Bottom-left corner center
        c_bl = (x + r, y + height - r)
        # Top-left corner center
        c_tl = (x + r, y + r)

        # Top side (left to right)
        points.append(self.wobble_point(tl))
        points.extend(sample_side(tl, tr, segments_per_side))
        points.append(self.wobble_point(tr))

        # Top-right corner arc: -π/2 → 0
        points.extend(sample_arc(c_tr[0], c_tr[1], -math.pi / 2, 0, arc_segments))

        # Right side (top to bottom)
        points.append(self.wobble_point(rt))
        points.extend(sample_side(rt, rb, segments_per_side))
        points.append(self.wobble_point(rb))

        # Bottom-right corner arc: 0 → π/2
        points.extend(sample_arc(c_br[0], c_br[1], 0, math.pi / 2, arc_segments))

        # Bottom side (right to left)
        points.append(self.wobble_point(br))
        points.extend(sample_side(br, bl, segments_per_side))
        points.append(self.wobble_point(bl))

        # Bottom-left corner arc: π/2 → π
        points.extend(sample_arc(c_bl[0], c_bl[1], math.pi / 2, math.pi, arc_segments))

        # Left side (bottom to top)
        points.append(self.wobble_point(lb))
        points.extend(sample_side(lb, la, segments_per_side))
        points.append(self.wobble_point(la))

        # Top-left corner arc: π → 3π/2
        points.extend(sample_arc(c_tl[0], c_tl[1], math.pi, 3 * math.pi / 2, arc_segments))

        return _smooth_bezier_path(points, closed=True)

    def wobble_circle(self, cx: float, cy: float, radius: float, segments: int = 24) -> str:
        """Return SVG path d-string for a wobbly circle.

        Samples `segments` points around the circumference, applies wobble,
        then connects them with cubic bezier curves.
        """
        return self.wobble_ellipse(cx, cy, radius, radius, segments)

    def wobble_ellipse(
        self, cx: float, cy: float, rx: float, ry: float, segments: int = 24
    ) -> str:
        """Return SVG path d-string for a wobbly ellipse.

        Samples `segments` points around the circumference, applies wobble,
        then connects them with cubic bezier curves.
        """
        points: list[Point] = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            raw = Point(cx + rx * math.cos(angle), cy + ry * math.sin(angle))
            points.append(self.wobble_point(raw))
        return _smooth_bezier_path(points, closed=True)

    def wobble_diamond(
        self, cx: float, cy: float, half_w: float, half_h: float,
        segments_per_side: int = 3,
    ) -> str:
        """Return SVG path d-string for a wobbly diamond.

        Vertices: top (cx, cy-half_h), right (cx+half_w, cy),
                  bottom (cx, cy+half_h), left (cx-half_w, cy).
        Samples intermediate points along each edge to preserve the angular
        diamond shape when smoothed by bezier curves.
        """
        vertices = [
            Point(cx, cy - half_h),       # top
            Point(cx + half_w, cy),        # right
            Point(cx, cy + half_h),        # bottom
            Point(cx - half_w, cy),        # left
        ]
        points: list[Point] = []
        for i in range(4):
            p0 = vertices[i]
            p1 = vertices[(i + 1) % 4]
            # Add the vertex
            points.append(self.wobble_point(p0))
            # Add intermediate points along the edge
            for k in range(1, segments_per_side):
                t = k / segments_per_side
                mid = Point(p0.x + t * (p1.x - p0.x), p0.y + t * (p1.y - p0.y))
                points.append(self.wobble_point(mid))
        return _smooth_bezier_path(points, closed=True)

    def wobble_polygon(self, points: list[tuple[float, float]], use_lines: bool = False) -> str:
        """Return SVG path d-string for a wobbly polygon.

        General wobbly polygon from a list of (x, y) points. When use_lines
        is True, connects with straight lines (better for small shapes like
        arrowheads). Otherwise uses cubic bezier curves.
        """
        wobbled = [self.wobble_point(Point(x, y)) for x, y in points]
        if use_lines:
            def fmt(v: float) -> str:
                return f"{v:.2f}"
            p0 = wobbled[0]
            d = f"M {fmt(p0.x)} {fmt(p0.y)}"
            for p in wobbled[1:]:
                d += f" L {fmt(p.x)} {fmt(p.y)}"
            d += " Z"
            return d
        return _smooth_bezier_path(wobbled, closed=True)

    def wobble_bezier_points(
        self, points: tuple[Point, ...]
    ) -> tuple[Point, ...]:
        """Apply lighter wobble (~1px, amplitude * 0.5) to bezier control points.

        Used for connector paths — we want subtle wobble on the path itself,
        not dramatic vertex displacement. If not enabled, returns points unchanged.
        """
        if not self._config.enabled:
            return points
        lighter_amp = self._config.amplitude * 0.5
        return tuple(self.wobble_point(p, amplitude=lighter_amp) for p in points)
