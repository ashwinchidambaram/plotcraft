"""Example 1: Simple pipeline diagram rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig,
)

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Title
d.add("title", "How a commit becomes a release",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# Pipeline flow (row 1, left to right)
d.add("commit", "Push Commit", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
d.add("ci", "Run CI Tests", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=1, col=1)
d.add("review", "Code Review", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=1, col=2)
d.add("deploy", "Deploy to Prod", shape=ShapeKind.OVAL, color=ColorTheme.END, row=1, col=3)

# Connectors
d.connect("commit", "ci", line_weight=LineWeight.BOLD)
d.connect("ci", "review", line_weight=LineWeight.BOLD)
d.connect("review", "deploy", line_weight=LineWeight.BOLD)

# Caption
d.add("caption", "Every step is automated, every gate must pass",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=2, col=1)

d.save("examples/pipeline.excalidraw")
print("Saved examples/pipeline.excalidraw")
