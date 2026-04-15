"""PlotCraft — AI-friendly diagram engine with freeform Scene API and D2 rendering."""

__version__ = "0.2.0"

from plotcraft.scene import Scene
from plotcraft.types import (
    TextRole, ShapeKind, TextAlign, AnchorName, ArrowDirection,
    ConnectorStyle, LineWeight, RoutingStyle, SectionStyle, ColorTheme,
    TimelineOrientation, TimelineEntry, TreeNode,
    ThemeMode, DecorativeKind, CalloutPosition,
)
from plotcraft.diagram import Diagram
from plotcraft.grid import GridConfig
from plotcraft.wobble import WobbleConfig
from plotcraft.advisor import VisualPattern, PATTERNS, SHAPE_SEMANTICS, suggest_pattern, validate_diagram

__all__ = [
    # Primary API
    "Scene",
    # Legacy grid-based API
    "Diagram",
    "TextRole",
    "ShapeKind",
    "TextAlign",
    "AnchorName",
    "ArrowDirection",
    "ConnectorStyle",
    "LineWeight",
    "RoutingStyle",
    "GridConfig",
    "SectionStyle",
    "ColorTheme",
    "TimelineOrientation",
    "TimelineEntry",
    "TreeNode",
    "WobbleConfig",
    "ThemeMode",
    "DecorativeKind",
    "CalloutPosition",
    # advisor
    "VisualPattern",
    "PATTERNS",
    "SHAPE_SEMANTICS",
    "suggest_pattern",
    "validate_diagram",
]
