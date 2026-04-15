"""System architecture: How requests flow through a web app — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig, SectionStyle,
)

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Title
d.add("title", "Request Flow Through a Web App",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=2)

# --- Client tier (row 1) ---
d.add("browser", "Browser", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
d.add("cdn", "CDN\n(Cloudflare)", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=1, col=1)
d.add("lb", "Load Balancer", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=1, col=2)

d.connect("browser", "cdn", line_weight=LineWeight.BOLD)
d.connect("cdn", "lb", line_weight=LineWeight.BOLD)

# --- Backend tier (row 3, skip row 2) ---
d.add("api", "API Server\n(FastAPI)", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=3, col=1)
d.add("auth", "Auth Service\n(JWT)", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=3, col=2)
d.add("worker", "Background\nWorker", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=3, col=3)

d.connect("lb", "api",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("api", "auth")
d.connect("api", "worker")

# --- Data tier (row 5, skip row 4) ---
d.add("postgres", "PostgreSQL", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=5, col=1)
d.add("redis", "Redis Cache", shape=ShapeKind.RECT, color=ColorTheme.ERROR, row=5, col=2)
d.add("queue", "Message Queue\n(RabbitMQ)", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=5, col=3)

d.connect("api", "postgres",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER)
d.connect("api", "redis",
          source_anchor=AnchorName.BOTTOM_RIGHT,
          target_anchor=AnchorName.TOP_LEFT)
d.connect("worker", "queue",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER)

# Result
d.add("response", "HTTP Response", shape=ShapeKind.OVAL, color=ColorTheme.END, row=5, col=0)
d.connect("postgres", "response",
          source_anchor=AnchorName.LEFT_CENTER,
          target_anchor=AnchorName.RIGHT_CENTER,
          label="result",
          style=ConnectorStyle.DASHED)

# Sections
d.section("Client Tier", ["browser", "cdn", "lb"],
          style=SectionStyle(fill="#eef6ff", stroke="#6ba3d6"))
d.section("Backend Services", ["api", "auth", "worker"],
          style=SectionStyle(fill="#fff8ee", stroke="#d6a86b"))
d.section("Data Layer", ["postgres", "redis", "queue"],
          style=SectionStyle(fill="#eefff0", stroke="#6bd680"))

# Caption
d.add("caption", "Each tier scales independently — CDN and cache absorb most reads",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=7, col=2)

d.save("examples/architecture.excalidraw")
print("Saved examples/architecture.excalidraw")
