from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


class TextRole(Enum):
    TITLE = "title"
    SUBTITLE = "subtitle"
    CAPTION = "caption"
    BODY = "body"


class ShapeKind(Enum):
    RECT = "rect"
    SQUARE = "square"
    CIRCLE = "circle"
    OVAL = "oval"
    DIAMOND = "diamond"
    NONE = "none"


class TextAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class ArrowDirection(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    BOTH = "both"
    NONE = "none"


class AnchorName(Enum):
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    RIGHT_CENTER = "right_center"
    BOTTOM_RIGHT = "bottom_right"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_LEFT = "bottom_left"
    LEFT_CENTER = "left_center"
    CENTER = "center"


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Size:
    width: float
    height: float


@dataclass(frozen=True)
class BBox:
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def anchor(self, name: AnchorName) -> Point:
        """Return the Point for a given anchor name on this bounding box."""
        match name:
            case AnchorName.TOP_LEFT:
                return Point(self.x, self.y)
            case AnchorName.TOP_CENTER:
                return Point(self.x + self.width / 2, self.y)
            case AnchorName.TOP_RIGHT:
                return Point(self.x + self.width, self.y)
            case AnchorName.LEFT_CENTER:
                return Point(self.x, self.y + self.height / 2)
            case AnchorName.CENTER:
                return self.center
            case AnchorName.RIGHT_CENTER:
                return Point(self.x + self.width, self.y + self.height / 2)
            case AnchorName.BOTTOM_LEFT:
                return Point(self.x, self.y + self.height)
            case AnchorName.BOTTOM_CENTER:
                return Point(self.x + self.width / 2, self.y + self.height)
            case AnchorName.BOTTOM_RIGHT:
                return Point(self.x + self.width, self.y + self.height)


@dataclass(frozen=True)
class TextStyle:
    font_family: str
    font_size: float
    font_weight: str  # "normal" or "bold"
    line_height: float  # multiplier e.g. 1.3


TEXT_STYLE_DEFAULTS: dict[TextRole, TextStyle] = {
    TextRole.TITLE: TextStyle("Arial", 24.0, "bold", 1.3),
    TextRole.SUBTITLE: TextStyle("Arial", 18.0, "bold", 1.3),
    TextRole.CAPTION: TextStyle("Arial", 12.0, "normal", 1.3),
    TextRole.BODY: TextStyle("Arial", 14.0, "normal", 1.4),
}


@dataclass(frozen=True)
class RoleScale:
    min_width: float
    min_height: float
    padding_multiplier: float


ROLE_SCALE_DEFAULTS: dict[TextRole, RoleScale] = {
    TextRole.TITLE: RoleScale(min_width=280, min_height=80, padding_multiplier=1.8),
    TextRole.SUBTITLE: RoleScale(min_width=220, min_height=60, padding_multiplier=1.4),
    TextRole.BODY: RoleScale(min_width=0, min_height=0, padding_multiplier=1.0),
    TextRole.CAPTION: RoleScale(min_width=0, min_height=0, padding_multiplier=0.8),
}


class ColorTheme(Enum):
    NEUTRAL = "neutral"
    START = "start"
    END = "end"
    DECISION = "decision"
    ERROR = "error"
    HIGHLIGHT = "highlight"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True)
class ColorPalette:
    fill: str
    stroke: str


COLOR_DEFAULTS: dict[ColorTheme, ColorPalette] = {
    ColorTheme.NEUTRAL: ColorPalette(fill="#f8f9fa", stroke="#333333"),
    ColorTheme.START: ColorPalette(fill="#d4edda", stroke="#28a745"),
    ColorTheme.END: ColorPalette(fill="#f8d7da", stroke="#dc3545"),
    ColorTheme.DECISION: ColorPalette(fill="#fff3cd", stroke="#ffc107"),
    ColorTheme.ERROR: ColorPalette(fill="#f8d7da", stroke="#dc3545"),
    ColorTheme.HIGHLIGHT: ColorPalette(fill="#cce5ff", stroke="#007bff"),
    ColorTheme.INFO: ColorPalette(fill="#d1ecf1", stroke="#17a2b8"),
    ColorTheme.SUCCESS: ColorPalette(fill="#d4edda", stroke="#28a745"),
    ColorTheme.WARNING: ColorPalette(fill="#fff3cd", stroke="#e0a800"),
}


class ConnectorStyle(Enum):
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"


class LineWeight(Enum):
    THIN = "thin"
    NORMAL = "normal"
    BOLD = "bold"


LINE_WEIGHT_WIDTHS: dict["LineWeight", float] = {
    LineWeight.THIN: 1.0,
    LineWeight.NORMAL: 1.5,
    LineWeight.BOLD: 3.0,
}


@dataclass(frozen=True)
class SectionStyle:
    fill: str = "#f0f4ff"
    stroke: str = "#b0c4de"
    stroke_width: float = 1.0
    corner_radius: float = 12.0
    label_font_size: float = 16.0
    label_color: str = "#555555"
    padding: float = 30.0


class TimelineOrientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass(frozen=True)
class TimelineEntry:
    label: str
    description: str = ""


@dataclass(frozen=True)
class TreeNode:
    label: str
    children: tuple[TreeNode, ...] = ()


class PlacementError(Exception):
    pass


class ConnectionError(Exception):
    pass
