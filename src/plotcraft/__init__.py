"""PlotCraft — AI-friendly diagram engine with D2 rendering and spatial compositions."""

__version__ = "1.7.0"

from plotcraft.scene import Scene, Palette, PALETTES
from plotcraft.spatial import Canvas
from plotcraft.templates import (
    Pipeline,
    DecisionTree,
    Comparison,
    Cycle,
    FanOut,
    Architecture,
    Timeline,
)

__all__ = [
    "Scene",
    "Canvas",
    # Color customization
    "Palette",
    "PALETTES",
    # Templates (recommended for small models)
    "Pipeline",
    "DecisionTree",
    "Comparison",
    "Cycle",
    "FanOut",
    "Architecture",
    "Timeline",
]
