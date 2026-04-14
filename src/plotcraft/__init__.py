"""PlotCraft — AI-friendly diagram engine for generating grid-snapped SVG diagrams."""

__version__ = "0.1.0"

from plotcraft.types import (
    TextRole, ShapeKind, TextAlign, AnchorName, ArrowDirection,
    ConnectorStyle, LineWeight, SectionStyle, ColorTheme,
    TimelineOrientation, TimelineEntry, TreeNode,
)
from plotcraft.diagram import Diagram
from plotcraft.grid import GridConfig
from plotcraft.wobble import WobbleConfig

__all__ = [
    "Diagram",
    "TextRole",
    "ShapeKind",
    "TextAlign",
    "AnchorName",
    "ArrowDirection",
    "ConnectorStyle",
    "LineWeight",
    "GridConfig",
    "SectionStyle",
    "ColorTheme",
    "TimelineOrientation",
    "TimelineEntry",
    "TreeNode",
    "WobbleConfig",
]
