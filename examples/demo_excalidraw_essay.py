"""Visual essay: Why microservices beat monoliths — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    LineWeight, ColorTheme, GridConfig, SectionStyle,
    DecorativeKind, CalloutPosition,
)

# LAYOUT TABLE:
# row=0: title (col=1)
# --- Section 1: The Problem ---
# row=1: step1 (col=0), sec1_title (col=1)
# row=2: ui (col=0), logic (col=1), data (col=2)
# row=4: monolith (col=1)
# --- Section 2: The Solution ---
# row=6: step2 (col=0), sec2_title (col=1)
# row=7: gateway (col=1)
# row=9: svc_a (col=0), svc_b (col=1), svc_c (col=2)
# row=11: caption (col=1)

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=140, margin=30))

# Title
d.add("title", "Monoliths vs Microservices",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# --- Section 1: The Problem ---
d.decorate("step1", DecorativeKind.NUMBERED_CIRCLE, text="1", row=1, col=0)
d.add("sec1", "The Problem", role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=1, col=1)

d.add("ui", "UI Layer", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=0)
d.add("logic", "Business Logic", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=1)
d.add("data", "Data Access", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=2)

d.add("monolith", "One Deploy", shape=ShapeKind.RECT, color=ColorTheme.ERROR, row=4, col=1)

d.connect("ui", "monolith",
          source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER)
d.connect("logic", "monolith",
          source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER)
d.connect("data", "monolith",
          source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER)

d.callout("c_mono", "One bad deploy\nbreaks everything",
          "monolith", position=CalloutPosition.RIGHT)

# --- Section 2: The Solution ---
d.decorate("step2", DecorativeKind.NUMBERED_CIRCLE, text="2", row=6, col=0)
d.add("sec2", "The Solution", role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=6, col=1)

d.add("gateway", "API Gateway", shape=ShapeKind.OVAL, color=ColorTheme.START, row=7, col=1)

d.add("svc_a", "Users", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=9, col=0)
d.add("svc_b", "Orders", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=9, col=1)
d.add("svc_c", "Payments", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=9, col=2)

d.connect("gateway", "svc_a",
          source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("gateway", "svc_b",
          source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("gateway", "svc_c",
          source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

d.callout("c_micro", "Each deploys\nindependently",
          "svc_b", position=CalloutPosition.BELOW)

# Sections
d.section("Monolith", ["ui", "logic", "data", "monolith"],
          style=SectionStyle(fill="#fff0f0", stroke="#d68080"))
d.section("Microservices", ["gateway", "svc_a", "svc_b", "svc_c"],
          style=SectionStyle(fill="#f0fff0", stroke="#6bd680"))

# Caption
d.add("caption", "Scale what needs scaling. Deploy what changed. Fail only where it broke.",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=11, col=1)

d.save("examples/essay.excalidraw")
print("Saved examples/essay.excalidraw")
