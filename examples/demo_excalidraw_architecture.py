"""Architecture: How a request flows through a web app — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig, SectionStyle,
)

# LAYOUT TABLE:
# row=0: title (col=1)
# row=1: browser (col=0), cdn (col=1), balancer (col=2)
# row=3: api (col=1)
# row=5: db (col=0), cache (col=2)
# row=7: caption (col=1)

d = Diagram(grid_config=GridConfig(cell_width=280, cell_height=160, margin=30))

# Title
d.add("title", "How a request reaches your data",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# --- Client tier (row 1) ---
d.add("browser", "Browser", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
d.add("cdn", "CDN", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=1, col=1)
d.add("lb", "Load Balancer", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=1, col=2)

d.connect("browser", "cdn", line_weight=LineWeight.BOLD)
d.connect("cdn", "lb", line_weight=LineWeight.BOLD)

# --- Backend (row 3) ---
d.add("api", "API Server", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=3, col=1)

d.connect("lb", "api",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# --- Data tier (row 5) ---
d.add("db", "PostgreSQL", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=5, col=1)
d.add("cache", "Redis", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=5, col=2)

d.connect("api", "db",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("api", "cache",
          source_anchor=AnchorName.RIGHT_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          style=ConnectorStyle.DASHED)

# Sections
d.section("Frontend", ["browser", "cdn", "lb"],
          style=SectionStyle(fill="#eef6ff", stroke="#6ba3d6"))
d.section("Backend", ["api"],
          style=SectionStyle(fill="#fff8ee", stroke="#d6a86b"))
d.section("Data", ["db", "cache"],
          style=SectionStyle(fill="#eefff0", stroke="#6bd680"))

# Caption
d.add("caption", "Each tier scales independently",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=7, col=1)

d.save("examples/architecture.excalidraw")
print("Saved examples/architecture.excalidraw")
