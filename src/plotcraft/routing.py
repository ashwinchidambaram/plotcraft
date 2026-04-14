"""Orthogonal edge router for PlotCraft.

Routes connectors using right-angle (orthogonal) paths that avoid obstacles,
with rounded corners at bends — draw.io-style.

This module is PURE GEOMETRY: it only imports from plotcraft.types.
"""
from __future__ import annotations

from plotcraft.types import BBox, Point

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_EPS = 1e-6  # tolerance for "same coordinate" comparisons


def _segment_intersects_bbox(p1: Point, p2: Point, bbox: BBox) -> bool:
    """Check if an axis-aligned segment intersects a bbox (with a tiny epsilon gap).

    Only correct for horizontal or vertical segments.
    """
    # Horizontal segment
    if abs(p1.y - p2.y) < _EPS:
        y = p1.y
        if y <= bbox.y or y >= bbox.y + bbox.height:
            return False
        seg_x_min = min(p1.x, p2.x)
        seg_x_max = max(p1.x, p2.x)
        if seg_x_max <= bbox.x or seg_x_min >= bbox.x + bbox.width:
            return False
        return True

    # Vertical segment
    if abs(p1.x - p2.x) < _EPS:
        x = p1.x
        if x <= bbox.x or x >= bbox.x + bbox.width:
            return False
        seg_y_min = min(p1.y, p2.y)
        seg_y_max = max(p1.y, p2.y)
        if seg_y_max <= bbox.y or seg_y_min >= bbox.y + bbox.height:
            return False
        return True

    # Diagonal – shouldn't happen in orthogonal routing, treat as non-intersecting
    return False


def _path_clear(waypoints: list[Point], obstacles: list[BBox]) -> bool:
    """Return True if no segment in the waypoint list intersects any obstacle."""
    for i in range(len(waypoints) - 1):
        for obs in obstacles:
            if _segment_intersects_bbox(waypoints[i], waypoints[i + 1], obs):
                return False
    return True


def _expanded(bbox: BBox, margin: float) -> BBox:
    """Return a BBox expanded by *margin* on all sides."""
    return BBox(
        x=bbox.x - margin,
        y=bbox.y - margin,
        width=bbox.width + 2 * margin,
        height=bbox.height + 2 * margin,
    )


# ---------------------------------------------------------------------------
# Public API — routing
# ---------------------------------------------------------------------------

def route_orthogonal(
    start: Point,
    end: Point,
    obstacles: list[BBox],
    corner_radius: float = 8.0,
    margin: float = 10.0,
) -> list[Point]:
    """Return waypoints for an orthogonal path from *start* to *end*.

    Obstacles are padded by *margin* before intersection tests so the path
    stays at least *margin* pixels away from any bbox edge.

    Strategy (in order):
    1. Straight line (collinear + unobstructed)
    2. L-route (one bend)
    3. Z-route (two bends) with mid-point offset search
    4. U-route fallback (route wide around blocking obstacle)
    """
    expanded = [_expanded(b, margin) for b in obstacles]

    # ------------------------------------------------------------------
    # 1. Straight line
    # ------------------------------------------------------------------
    if abs(start.x - end.x) < _EPS or abs(start.y - end.y) < _EPS:
        path = [start, end]
        if _path_clear(path, expanded):
            return path

    # ------------------------------------------------------------------
    # 2. L-route (one bend, two candidates)
    # ------------------------------------------------------------------
    bend_h = Point(end.x, start.y)   # horizontal-first bend
    bend_v = Point(start.x, end.y)   # vertical-first bend

    l_horiz = [start, bend_h, end]
    l_vert  = [start, bend_v, end]

    h_ok = _path_clear(l_horiz, expanded)
    v_ok = _path_clear(l_vert,  expanded)

    if h_ok and v_ok:
        # Both work: pick shorter total path length
        def _len(pts: list[Point]) -> float:
            return sum(
                abs(pts[i + 1].x - pts[i].x) + abs(pts[i + 1].y - pts[i].y)
                for i in range(len(pts) - 1)
            )
        return l_horiz if _len(l_horiz) <= _len(l_vert) else l_vert

    if h_ok:
        return l_horiz
    if v_ok:
        return l_vert

    # ------------------------------------------------------------------
    # 3. Z-route (two bends)
    # ------------------------------------------------------------------
    # We search for a mid_x (horizontal-first Z) or mid_y (vertical-first Z)
    # that avoids all obstacles.

    def _try_z_horizontal(mid_x: float) -> list[Point] | None:
        """start → (mid_x, start.y) → (mid_x, end.y) → end"""
        path = [
            start,
            Point(mid_x, start.y),
            Point(mid_x, end.y),
            end,
        ]
        return path if _path_clear(path, expanded) else None

    def _try_z_vertical(mid_y: float) -> list[Point] | None:
        """start → (start.x, mid_y) → (end.x, mid_y) → end"""
        path = [
            start,
            Point(start.x, mid_y),
            Point(end.x, mid_y),
            end,
        ]
        return path if _path_clear(path, expanded) else None

    # Candidate mid-x values: midpoint first, then bbox edges ± margin
    mid_x_base = (start.x + end.x) / 2
    mid_x_candidates = [mid_x_base]
    for obs in expanded:
        mid_x_candidates.append(obs.x - margin)           # left of obstacle
        mid_x_candidates.append(obs.x + obs.width + margin)  # right of obstacle

    for mid_x in mid_x_candidates:
        result = _try_z_horizontal(mid_x)
        if result is not None:
            return result

    mid_y_base = (start.y + end.y) / 2
    mid_y_candidates = [mid_y_base]
    for obs in expanded:
        mid_y_candidates.append(obs.y - margin)
        mid_y_candidates.append(obs.y + obs.height + margin)

    for mid_y in mid_y_candidates:
        result = _try_z_vertical(mid_y)
        if result is not None:
            return result

    # ------------------------------------------------------------------
    # 4. U-route fallback — go wide around the first blocking obstacle
    # ------------------------------------------------------------------
    # Find the obstacle that most blocks the direct route.
    blocking: BBox | None = None
    for obs in expanded:
        if _segment_intersects_bbox(start, Point(end.x, start.y), obs) or \
           _segment_intersects_bbox(Point(end.x, start.y), end, obs) or \
           _segment_intersects_bbox(start, Point(start.x, end.y), obs) or \
           _segment_intersects_bbox(Point(start.x, end.y), end, obs):
            blocking = obs
            break

    if blocking is None:
        # Shouldn't happen, but just return L-route as-is
        return l_horiz

    # Try going around the 4 edges of the blocking obstacle
    routes: list[list[Point]] = []

    # Around left edge
    x_left = blocking.x - margin
    routes.append([start, Point(x_left, start.y), Point(x_left, end.y), end])

    # Around right edge
    x_right = blocking.x + blocking.width + margin
    routes.append([start, Point(x_right, start.y), Point(x_right, end.y), end])

    # Around top edge
    y_top = blocking.y - margin
    routes.append([start, Point(start.x, y_top), Point(end.x, y_top), end])

    # Around bottom edge
    y_bottom = blocking.y + blocking.height + margin
    routes.append([start, Point(start.x, y_bottom), Point(end.x, y_bottom), end])

    # Pick first clear route; if none, pick the geometrically shortest
    for r in routes:
        if _path_clear(r, expanded):
            return r

    # Absolute fallback: return the shortest route even if it clips something
    def _manhattan(pts: list[Point]) -> float:
        return sum(
            abs(pts[i + 1].x - pts[i].x) + abs(pts[i + 1].y - pts[i].y)
            for i in range(len(pts) - 1)
        )

    return min(routes, key=_manhattan)


# ---------------------------------------------------------------------------
# Public API — SVG serialisation
# ---------------------------------------------------------------------------

def orthogonal_path_to_svg(waypoints: list[Point], corner_radius: float = 8.0) -> str:
    """Convert orthogonal waypoints to an SVG path *d* string.

    Sharp bend corners are replaced with quadratic bezier curves whose
    radius equals *corner_radius*.  The curve is drawn through the original
    bend point as the control point.

    Example output::

        "M 100 200 L 250 200 Q 260 200 260 210 L 260 350"
    """
    if len(waypoints) < 2:
        return ""

    def _fmt(v: float) -> str:
        # Emit integer when possible, otherwise 2 dp
        return f"{v:.2f}".rstrip("0").rstrip(".")

    def _p(pt: Point) -> str:
        return f"{_fmt(pt.x)} {_fmt(pt.y)}"

    # Start at the first point
    parts: list[str] = [f"M {_p(waypoints[0])}"]

    n = len(waypoints)

    # We iterate over each segment, shortening it near bend points so the
    # quadratic bezier can be inserted.
    i = 0
    while i < n - 1:
        p_cur = waypoints[i]
        p_next = waypoints[i + 1]

        # Is p_next a bend (i.e., not the last point)?
        is_bend = (i + 2 < n)

        if not is_bend:
            # Last segment — draw straight to end
            parts.append(f"L {_p(p_next)}")
        else:
            p_after = waypoints[i + 2]

            # Direction from p_cur to p_next
            dx1 = p_next.x - p_cur.x
            dy1 = p_next.y - p_cur.y
            len1 = max(abs(dx1), abs(dy1))  # Manhattan length of segment

            # Direction from p_next to p_after
            dx2 = p_after.x - p_next.x
            dy2 = p_after.y - p_next.y

            # Clamp corner radius to half of the shorter adjoining segment length
            len2 = max(abs(dx2), abs(dy2))
            r = min(corner_radius, len1 / 2.0, len2 / 2.0)

            if r < _EPS or len1 < _EPS:
                # Segment too short for a rounded corner — just draw straight
                parts.append(f"L {_p(p_next)}")
            else:
                # Point on incoming segment, r before the bend
                t1_x = p_next.x - r * (dx1 / len1)
                t1_y = p_next.y - r * (dy1 / len1)

                # Point on outgoing segment, r after the bend
                t2_x = p_next.x + r * (dx2 / max(len2, _EPS))
                t2_y = p_next.y + r * (dy2 / max(len2, _EPS))

                parts.append(f"L {_fmt(t1_x)} {_fmt(t1_y)}")
                # Q control-point end-point
                parts.append(
                    f"Q {_fmt(p_next.x)} {_fmt(p_next.y)} "
                    f"{_fmt(t2_x)} {_fmt(t2_y)}"
                )
                # The next iteration starts from t2, not p_next, so we move
                # the cursor by inserting a synthetic "current" position.
                # We handle this by storing t2 as the effective start of the
                # next segment (replace waypoints[i+1] conceptually).
                #
                # Because waypoints is a plain list we splice a synthetic
                # intermediate point: skip past the bend by advancing i but
                # prepend t2 to waypoints for the next segment start.
                waypoints = (
                    waypoints[: i + 1]
                    + [Point(t2_x, t2_y)]
                    + waypoints[i + 2 :]
                )
                # n stays the same (we replaced p_next with t2, p_after is unchanged)
                i += 1
                continue

        i += 1

    return " ".join(parts)
