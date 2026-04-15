"""Dark theme: The machine learning pipeline — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig,
    ThemeMode, CalloutPosition, DecorativeKind,
)

d = Diagram(
    grid_config=GridConfig(cell_width=260, cell_height=160, margin=30),
    theme=ThemeMode.DARK,
)

# Title
d.add("title", "The Machine Learning Pipeline",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=2)

# Step 1: Raw data (row 1)
d.decorate("n1", DecorativeKind.NUMBERED_CIRCLE, text="1", row=1, col=0,
           color=ColorTheme.INFO)
d.add("raw", "Raw Data\n(CSV, JSON, APIs)", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=1, col=1)

# Step 2: Preprocessing (row 3)
d.decorate("n2", DecorativeKind.NUMBERED_CIRCLE, text="2", row=3, col=0,
           color=ColorTheme.INFO)
d.add("clean", "Data Cleaning\n& Validation", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=3, col=1)
d.add("feature", "Feature\nEngineering", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=3, col=3)

d.connect("raw", "clean",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("clean", "feature")

# Callout for cleaning — col 2 is free between clean(1) and feature(3)
d.callout("c_clean", "Handle nulls,\noutliers,\nduplicates",
          "clean", position=CalloutPosition.RIGHT, color=ColorTheme.WARNING)

# Step 3: Training (row 5)
d.decorate("n3", DecorativeKind.NUMBERED_CIRCLE, text="3", row=5, col=0,
           color=ColorTheme.HIGHLIGHT)
d.add("train", "Model Training\n(GPU)", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=5, col=1)

d.connect("feature", "train",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Step 4: Evaluation (row 7)
d.decorate("n4", DecorativeKind.NUMBERED_CIRCLE, text="4", row=7, col=0,
           color=ColorTheme.SUCCESS)
d.add("eval", "Evaluation\n(metrics)", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=7, col=1)
d.add("good", "Accuracy\n>= 95%?", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=7, col=3)

d.connect("train", "eval",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("eval", "good")

# Callout for eval — col 2 is free
d.callout("c_eval", "Precision, recall,\nF1 score,\nconfusion matrix",
          "eval", position=CalloutPosition.RIGHT, color=ColorTheme.SUCCESS)

# Retrain loop
d.connect("good", "train",
          source_anchor=AnchorName.TOP_CENTER,
          target_anchor=AnchorName.RIGHT_CENTER,
          label="No — retrain",
          style=ConnectorStyle.DASHED)

# Step 5: Deploy (row 9)
d.decorate("n5", DecorativeKind.NUMBERED_CIRCLE, text="5", row=9, col=0,
           color=ColorTheme.END)
d.add("deploy", "Deploy to\nProduction", shape=ShapeKind.OVAL, color=ColorTheme.END, row=9, col=3)

d.connect("good", "deploy",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          label="Yes",
          line_weight=LineWeight.BOLD)

d.callout("c_deploy", "Model registry,\nA/B testing,\nmonitoring",
          "deploy", position=CalloutPosition.RIGHT, color=ColorTheme.END)

# Caption
d.add("caption", "Iterate fast, evaluate rigorously, deploy confidently",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=11, col=2)

d.save("examples/dark_ml_pipeline.excalidraw")
print("Saved examples/dark_ml_pipeline.excalidraw")
