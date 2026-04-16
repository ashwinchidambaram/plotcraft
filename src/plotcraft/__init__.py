"""PlotCraft — AI-friendly diagram engine with D2 rendering and spatial compositions."""

__version__ = "1.6.0"

from plotcraft.scene import Scene
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
    # Templates (recommended for small models)
    "Pipeline",
    "DecisionTree",
    "Comparison",
    "Cycle",
    "FanOut",
    "Architecture",
    "Timeline",
]
