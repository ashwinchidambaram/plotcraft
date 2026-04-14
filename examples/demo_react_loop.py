"""ReAct Loop diagram — shows how an AI agent reasons and acts iteratively."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ArrowDirection, ConnectorStyle, LineWeight, ColorTheme,
    GridConfig, SectionStyle,
)

# Wide cells for readable labels
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=140, margin=28))

# ── Title ──
d.add("title", "ReAct Agent Loop", role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=0, col=3)

# ── Horizontal flow: Query → Observe → Think → Answer ──
d.add("query", "User Query", role=TextRole.SUBTITLE, shape=ShapeKind.RECT,
      color=ColorTheme.START, row=1, col=0)

d.add("observe", "Observe", role=TextRole.SUBTITLE, shape=ShapeKind.RECT,
      color=ColorTheme.INFO, row=1, col=2)

d.add("think", "Think", role=TextRole.SUBTITLE, shape=ShapeKind.DIAMOND,
      color=ColorTheme.DECISION, row=1, col=4)

d.add("answer", "Answer", role=TextRole.SUBTITLE, shape=ShapeKind.RECT,
      color=ColorTheme.END, row=1, col=6)

# ── Feedback loop: Act sits below, centered under Observe ──
d.add("act", "Act", role=TextRole.SUBTITLE, shape=ShapeKind.RECT,
      color=ColorTheme.HIGHLIGHT, row=3, col=3)

# ═══ Connectors ═══

# Forward flow (left to right)
d.connect("query", "observe",
          style=ConnectorStyle.SOLID, line_weight=LineWeight.NORMAL)

d.connect("observe", "think",
          style=ConnectorStyle.SOLID, line_weight=LineWeight.BOLD)

# Exit: Think → Answer
d.connect("think", "answer",
          source_anchor=AnchorName.RIGHT_CENTER,
          target_anchor=AnchorName.LEFT_CENTER,
          label="done",
          style=ConnectorStyle.DASHED, line_weight=LineWeight.NORMAL)

# Loop down: Think → Act
d.connect("think", "act",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.RIGHT_CENTER,
          style=ConnectorStyle.SOLID, line_weight=LineWeight.BOLD)

# Loop back up: Act → Observe
d.connect("act", "observe",
          source_anchor=AnchorName.LEFT_CENTER,
          target_anchor=AnchorName.BOTTOM_CENTER,
          label="loop",
          style=ConnectorStyle.SOLID, line_weight=LineWeight.BOLD)

# ── Section: the loop nodes only (not Query or Answer) ──
d.section("Iterative Loop", ["observe", "think", "act"],
          style=SectionStyle(
              fill="#ede9e0", stroke="#b0a898",
              stroke_width=1.5, corner_radius=16.0,
              label_font_size=18.0, label_color="#7a7060",
              padding=35.0,
          ))

# ── Render ──
d.save("demo_react_loop.svg")
d.save("demo_react_loop.png", scale=2.0)
print("Saved demo_react_loop.svg and demo_react_loop.png")
