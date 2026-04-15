"""Visual essay: Why microservices beat monoliths at scale — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig, SectionStyle,
    DecorativeKind, CalloutPosition,
)

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Title
d.add("title", "Why Microservices Beat Monoliths at Scale",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=2)

# --- Section 1: The monolith problem (convergence) ---
d.decorate("num1", DecorativeKind.NUMBERED_CIRCLE, text="1", row=1, col=0,
           color=ColorTheme.ERROR)

d.add("s1_label", "The Monolith Problem",
      role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=1, col=1)

# Everything funnels into one big box
d.add("ui", "UI Layer", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=0)
d.add("biz", "Business Logic", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=2)
d.add("data", "Data Access", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=4)

d.add("monolith", "MONOLITH\n(one deploy)", shape=ShapeKind.RECT, color=ColorTheme.ERROR, row=4, col=2)

# Convergence: everything points into the monolith
d.connect("ui", "monolith",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_LEFT,
          line_weight=LineWeight.BOLD)
d.connect("biz", "monolith",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("data", "monolith",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_RIGHT,
          line_weight=LineWeight.BOLD)

d.callout("c_mono", "One bad deploy\ntakes down\neverything",
          "monolith", position=CalloutPosition.RIGHT, color=ColorTheme.ERROR)

d.section("Problem: Tight Coupling", ["ui", "biz", "data", "monolith"],
          style=SectionStyle(fill="#fff0f0", stroke="#d66b6b"))

# --- Section 2: The microservice solution (fan-out) ---
d.decorate("num2", DecorativeKind.NUMBERED_CIRCLE, text="2", row=6, col=0,
           color=ColorTheme.SUCCESS)

d.add("s2_label", "The Microservice Solution",
      role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=6, col=1)

d.add("gateway", "API Gateway", shape=ShapeKind.OVAL, color=ColorTheme.START, row=7, col=2)

# Fan-out: gateway to independent services
d.add("svc_user", "User Service", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=9, col=0)
d.add("svc_order", "Order Service", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=9, col=2)
d.add("svc_notif", "Notification\nService", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=9, col=4)

d.connect("gateway", "svc_user",
          source_anchor=AnchorName.BOTTOM_LEFT,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("gateway", "svc_order",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("gateway", "svc_notif",
          source_anchor=AnchorName.BOTTOM_RIGHT,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

d.callout("c_micro", "Each service deploys\nindependently —\nfailure is isolated",
          "svc_order", position=CalloutPosition.BELOW, color=ColorTheme.SUCCESS)

d.section("Solution: Independent Services", ["gateway", "svc_user", "svc_order", "svc_notif"],
          style=SectionStyle(fill="#f0fff0", stroke="#6bd66b"))

# Closing insight
d.add("insight", "Scale what needs scaling. Deploy what changed. Fail only where it broke.",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=11, col=2)

d.save("examples/essay.excalidraw")
print("Saved examples/essay.excalidraw")
