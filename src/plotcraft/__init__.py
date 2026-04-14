"""PlotCraft — AI-friendly diagram engine for generating grid-snapped SVG diagrams."""

__version__ = "0.1.0"

from plotcraft.types import (
    TextRole, ShapeKind, TextAlign, AnchorName, ArrowDirection,
    ConnectorStyle, LineWeight, RoutingStyle, SectionStyle, ColorTheme,
    TimelineOrientation, TimelineEntry, TreeNode,
)
from plotcraft.diagram import Diagram
from plotcraft.grid import GridConfig
from plotcraft.wobble import WobbleConfig
from plotcraft.advisor import VisualPattern, PATTERNS, SHAPE_SEMANTICS, suggest_pattern, validate_diagram

__all__ = [
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
    # advisor
    "VisualPattern",
    "PATTERNS",
    "SHAPE_SEMANTICS",
    "suggest_pattern",
    "validate_diagram",
]
