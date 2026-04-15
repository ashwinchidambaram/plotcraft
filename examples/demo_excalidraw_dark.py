"""Dark theme: The machine learning pipeline — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig,
    ThemeMode, DecorativeKind,
)

# LAYOUT TABLE — simple vertical flow, one column:
# row=0: title (col=1)
# row=1: data (col=1)
# row=3: preprocess (col=1)
# row=5: train (col=1)
# row=7: evaluate (col=1)
# row=9: deploy (col=1)
# Numbered decoratives at col=0 on each step row

d = Diagram(
    grid_config=GridConfig(cell_width=280, cell_height=160, margin=30),
    theme=ThemeMode.DARK,
)

# Title
d.add("title", "The ML Pipeline",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# Step 1: Data
d.decorate("n1", DecorativeKind.NUMBERED_CIRCLE, text="1", row=1, col=0, color=ColorTheme.INFO)
d.add("data", "Raw Data", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=1)

# Step 2: Preprocess
d.decorate("n2", DecorativeKind.NUMBERED_CIRCLE, text="2", row=3, col=0, color=ColorTheme.WARNING)
d.add("prep", "Preprocess", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=3, col=1)

d.connect("data", "prep",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Step 3: Train
d.decorate("n3", DecorativeKind.NUMBERED_CIRCLE, text="3", row=5, col=0, color=ColorTheme.HIGHLIGHT)
d.add("train", "Train Model", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=5, col=1)

d.connect("prep", "train",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Step 4: Evaluate
d.decorate("n4", DecorativeKind.NUMBERED_CIRCLE, text="4", row=7, col=0, color=ColorTheme.DECISION)
d.add("eval", "Evaluate", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=7, col=1)

d.connect("train", "eval",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Step 5: Deploy
d.decorate("n5", DecorativeKind.NUMBERED_CIRCLE, text="5", row=9, col=0, color=ColorTheme.END)
d.add("deploy", "Deploy", shape=ShapeKind.OVAL, color=ColorTheme.END, row=9, col=1)

d.connect("eval", "deploy",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Caption
d.add("caption", "Iterate fast, evaluate rigorously, deploy confidently",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=11, col=1)

d.save("examples/dark_ml_pipeline.excalidraw")
print("Saved examples/dark_ml_pipeline.excalidraw")
