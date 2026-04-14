from __future__ import annotations
import math
from dataclasses import dataclass
from plotcraft.types import AnchorName, ArrowDirection, Point, BBox, ConnectionError, ConnectorStyle, LineWeight
from plotcraft.grid import Placement


@dataclass(frozen=True)
class Connector:
    id: str
    source_shape_id: str
    source_anchor: AnchorName
    target_shape_id: str
    target_anchor: AnchorName
    path_points: tuple[Point, ...]  # control points for cubic bezier
    label: str | None = None
    style: ConnectorStyle = ConnectorStyle.SOLID
    line_weight: LineWeight = LineWeight.NORMAL
    direction: ArrowDirection = ArrowDirection.FORWARD


def create_connector(
    id: str,
    source_id: str,
    source_anchor: AnchorName,
    target_id: str,
    target_anchor: AnchorName,
    label: str | None = None,
    style: ConnectorStyle = ConnectorStyle.SOLID,
    line_weight: LineWeight = LineWeight.NORMAL,
    direction: ArrowDirection = ArrowDirection.FORWARD,
) -> Connector:
    """Create a connector stub (path_points empty, resolved later)."""
    if source_id == target_id:
        raise ConnectionError(f"Cannot connect shape '{source_id}' to itself")
    return Connector(
        id=id,
        source_shape_id=source_id,
        source_anchor=source_anchor,
        target_shape_id=target_id,
        target_anchor=target_anchor,
        path_points=(),
        label=label,
        style=style,
        line_weight=line_weight,
        direction=direction,
    )


def _get_absolute_anchor(placement: Placement, anchor_name: AnchorName) -> Point:
    """Get the absolute canvas position of an anchor on a placed shape."""
    relative = placement.shape.content_bbox.anchor(anchor_name)
    return Point(placement.position.x + relative.x, placement.position.y + relative.y)


def _departure_direction(anchor: AnchorName) -> Point:
    """Unit-ish vector for the departure direction from an anchor."""
    # Map each anchor to its natural departure direction
    directions = {
        AnchorName.TOP_LEFT: Point(-1, -1),
        AnchorName.TOP_CENTER: Point(0, -1),
        AnchorName.TOP_RIGHT: Point(1, -1),
        AnchorName.RIGHT_CENTER: Point(1, 0),
        AnchorName.BOTTOM_RIGHT: Point(1, 1),
        AnchorName.BOTTOM_CENTER: Point(0, 1),
        AnchorName.BOTTOM_LEFT: Point(-1, 1),
        AnchorName.LEFT_CENTER: Point(-1, 0),
        AnchorName.CENTER: Point(0, 0),
    }
    return directions[anchor]


def _line_intersects_bbox(p1: Point, p2: Point, bbox: BBox) -> bool:
    """Check if line segment p1->p2 intersects with bbox (approximate)."""
    # Simple check: does the line's bounding rect overlap with the bbox?
    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)
    min_y = min(p1.y, p2.y)
    max_y = max(p1.y, p2.y)

    # No overlap if completely separated
    if max_x < bbox.x or min_x > bbox.x + bbox.width:
        return False
    if max_y < bbox.y or min_y > bbox.y + bbox.height:
        return False

    # More precise: check if midpoint of line is inside bbox
    mid_x = (p1.x + p2.x) / 2
    mid_y = (p1.y + p2.y) / 2
    if (bbox.x <= mid_x <= bbox.x + bbox.width and
            bbox.y <= mid_y <= bbox.y + bbox.height):
        return True

    return False


def route_connector(
    connector: Connector,
    placements: dict[str, Placement],
) -> Connector:
    """Resolve path_points with obstacle avoidance using control-point offset approach."""
    source_p = placements[connector.source_shape_id]
    target_p = placements[connector.target_shape_id]

    # Get absolute anchor positions
    start = _get_absolute_anchor(source_p, connector.source_anchor)
    end = _get_absolute_anchor(target_p, connector.target_anchor)

    # Calculate distance for control point offset
    dx = end.x - start.x
    dy = end.y - start.y
    distance = math.sqrt(dx * dx + dy * dy)
    offset = max(40.0, min(80.0, distance * 0.3))

    # Departure and arrival directions
    dep = _departure_direction(connector.source_anchor)
    arr = _departure_direction(connector.target_anchor)

    # Control points offset from start/end in their departure/arrival directions
    cp1 = Point(start.x + dep.x * offset, start.y + dep.y * offset)
    cp2 = Point(end.x + arr.x * offset, end.y + arr.y * offset)

    # Check if the straight line between cp1 and cp2 intersects any obstacle shape
    # (excluding source and target shapes)
    obstacle_shapes = {
        sid: p for sid, p in placements.items()
        if sid != connector.source_shape_id and sid != connector.target_shape_id
    }

    for sid, obs_p in obstacle_shapes.items():
        # Use the shape's actual content_bbox positioned on canvas
        obs_bbox = BBox(
            obs_p.position.x,
            obs_p.position.y,
            obs_p.shape.content_bbox.width,
            obs_p.shape.content_bbox.height,
        )

        if _line_intersects_bbox(cp1, cp2, obs_bbox):
            # Offset the midpoint perpendicular to the line to avoid obstacle
            mid_x = (cp1.x + cp2.x) / 2
            mid_y = (cp1.y + cp2.y) / 2

            # Direction perpendicular to the line cp1->cp2
            line_dx = cp2.x - cp1.x
            line_dy = cp2.y - cp1.y
            line_len = math.sqrt(line_dx * line_dx + line_dy * line_dy) or 1.0

            # Perpendicular (rotate 90 degrees)
            perp_x = -line_dy / line_len
            perp_y = line_dx / line_len

            # Offset by enough to clear the obstacle
            avoidance_dist = max(obs_bbox.width, obs_bbox.height) * 0.75

            # Choose direction that moves away from obstacle center
            obs_center = obs_bbox.center
            if (mid_x + perp_x - obs_center.x) ** 2 + (mid_y + perp_y - obs_center.y) ** 2 > \
               (mid_x - perp_x - obs_center.x) ** 2 + (mid_y - perp_y - obs_center.y) ** 2:
                waypoint = Point(mid_x + perp_x * avoidance_dist, mid_y + perp_y * avoidance_dist)
            else:
                waypoint = Point(mid_x - perp_x * avoidance_dist, mid_y - perp_y * avoidance_dist)

            # Return path with waypoint: start -> cp1 -> waypoint -> cp2 -> end
            return Connector(
                id=connector.id,
                source_shape_id=connector.source_shape_id,
                source_anchor=connector.source_anchor,
                target_shape_id=connector.target_shape_id,
                target_anchor=connector.target_anchor,
                path_points=(start, cp1, waypoint, cp2, end),
                label=connector.label,
                style=connector.style,
                line_weight=connector.line_weight,
                direction=connector.direction,
            )

    # No obstacles: simple cubic bezier: start, cp1, cp2, end
    return Connector(
        id=connector.id,
        source_shape_id=connector.source_shape_id,
        source_anchor=connector.source_anchor,
        target_shape_id=connector.target_shape_id,
        target_anchor=connector.target_anchor,
        path_points=(start, cp1, cp2, end),
        label=connector.label,
        style=connector.style,
        line_weight=connector.line_weight,
        direction=connector.direction,
    )


def route_all(
    connectors: list[Connector],
    placements: dict[str, Placement],
) -> list[Connector]:
    """Route all connectors."""
    return [route_connector(c, placements) for c in connectors]
