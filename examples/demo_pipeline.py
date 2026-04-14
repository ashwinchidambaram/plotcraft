"""Demo: Software Deployment Pipeline using all 8 new PlotCraft features."""
from plotcraft import (
    Diagram, TextRole, ShapeKind, TextAlign, AnchorName, GridConfig,
    ColorTheme, ConnectorStyle, LineWeight, ArrowDirection, SectionStyle,
    TimelineOrientation, TimelineEntry, TreeNode,
)

d = (
    Diagram(GridConfig(cell_width=280, cell_height=170, margin=25))

    # === Title (free-floating, visual hierarchy) ===
    .add("title", "Deployment Pipeline", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

    # === Development section ===
    .add("push", "Code Push", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
    .add("build", "Build & Test", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=1, col=1)

    # === Gate section ===
    .add("gate", "Tests\nPass?", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=1, col=2)
    .add("fix", "Fix Issues", shape=ShapeKind.RECT, color=ColorTheme.ERROR, row=2, col=2)

    # === Production section ===
    .add("staging", "Deploy to\nStaging", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=1, col=3)
    .add("prod", "Deploy to\nProduction", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=1, col=4)
    .add("monitor", "Monitoring\n& Alerts", shape=ShapeKind.OVAL, color=ColorTheme.INFO, row=2, col=4)

    # === Annotations (free-floating) ===
    .add("note1", "automated", role=TextRole.CAPTION, shape=ShapeKind.NONE, row=0, col=0)
    .add("note2", "manual approval", role=TextRole.CAPTION, shape=ShapeKind.NONE, row=0, col=3)

    # === Connections ===
    .connect("push", "build", label="trigger")
    .connect("build", "gate", label="results")
    .connect("gate", "staging", label="pass",
             source_anchor=AnchorName.RIGHT_CENTER, target_anchor=AnchorName.LEFT_CENTER)
    .connect("gate", "fix", label="fail",
             source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
             style=ConnectorStyle.DASHED, line_weight=LineWeight.THIN)
    .connect("fix", "build",
             source_anchor=AnchorName.LEFT_CENTER, target_anchor=AnchorName.BOTTOM_CENTER,
             style=ConnectorStyle.DOTTED, label="retry")
    .connect("staging", "prod", label="promote", line_weight=LineWeight.BOLD)
    .connect("prod", "monitor", label="health checks",
             source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
             direction=ArrowDirection.BOTH)

    # === Sections ===
    .section("Development", ["push", "build"],
             SectionStyle(fill="#e8f5e9", stroke="#4caf50"))
    .section("Quality Gate", ["gate", "fix"],
             SectionStyle(fill="#fff8e1", stroke="#ff9800"))
    .section("Production", ["staging", "prod", "monitor"],
             SectionStyle(fill="#e3f2fd", stroke="#2196f3"))
)

d.save("demo_pipeline.svg")
d.save("demo_pipeline.png", scale=2.0)
print("Saved demo_pipeline.svg and demo_pipeline.png")
