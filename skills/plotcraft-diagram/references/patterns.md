# Visual Pattern Catalog

Complete code examples for each pattern. Use `GridConfig(cell_width=240, cell_height=160, margin=30)` for draw.io output.

---

## 1. Pipeline (Sequential Flow)

**Use when:** Processes, workflows, sequences, stages.

```python
from plotcraft import *

d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "How code reaches production", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)
d.add("commit", "Push Commit", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
d.add("ci", "Run CI Tests", shape=ShapeKind.RECT, row=1, col=1)
d.add("review", "Code Review", shape=ShapeKind.RECT, row=1, col=2)
d.add("deploy", "Deploy", shape=ShapeKind.OVAL, color=ColorTheme.END, row=1, col=3)

d.connect("commit", "ci")
d.connect("ci", "review")
d.connect("review", "deploy")
d.save("pipeline.drawio")
```

---

## 2. Fan-Out (One-to-Many)

**Use when:** Sources distributing to multiple targets, broadcasting.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "How events propagate through the system", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)
d.add("source", "Event Bus", shape=ShapeKind.CIRCLE, color=ColorTheme.START, row=1, col=0)
d.add("log", "Logger", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=0, col=2)
d.add("notify", "Notifier", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=1, col=2)
d.add("archive", "Archiver", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=2, col=2)

d.connect("source", "log", source_anchor=AnchorName.TOP_CENTER, target_anchor=AnchorName.LEFT_CENTER)
d.connect("source", "notify")
d.connect("source", "archive", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.LEFT_CENTER)
d.save("fan_out.drawio")
```

---

## 3. Convergence (Many-to-One)

**Use when:** Aggregation, funnels, synthesis.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "Three data sources feed one gateway", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)
d.add("api", "REST API", shape=ShapeKind.RECT, row=0, col=0)
d.add("ws", "WebSocket", shape=ShapeKind.RECT, row=1, col=0)
d.add("queue", "Message Queue", shape=ShapeKind.RECT, row=2, col=0)
d.add("gw", "API Gateway", shape=ShapeKind.CIRCLE, color=ColorTheme.END, row=1, col=2)

d.connect("api", "gw", source_anchor=AnchorName.RIGHT_CENTER, target_anchor=AnchorName.TOP_CENTER)
d.connect("ws", "gw")
d.connect("queue", "gw", source_anchor=AnchorName.RIGHT_CENTER, target_anchor=AnchorName.BOTTOM_CENTER)
d.save("convergence.drawio")
```

---

## 4. Cycle (Feedback Loop)

**Use when:** Iterative processes, retry logic, continuous improvement.

**The surprise:** The process circles back — challenges linear assumptions.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "How agents reason and act iteratively", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# Entry
d.add("query", "User Query", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)

# The loop
d.add("observe", "Observe", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=1, col=2)
d.add("think", "Think", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=3, col=2)
d.add("act", "Act", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=3, col=0)

# Exit
d.add("answer", "Answer", shape=ShapeKind.OVAL, color=ColorTheme.END, row=3, col=4)

# Flow
d.connect("query", "observe")
d.connect("observe", "think", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("think", "act", source_anchor=AnchorName.LEFT_CENTER, target_anchor=AnchorName.RIGHT_CENTER,
          line_weight=LineWeight.BOLD)
d.connect("act", "observe", source_anchor=AnchorName.TOP_CENTER, target_anchor=AnchorName.BOTTOM_CENTER,
          label="loop", line_weight=LineWeight.BOLD)
d.connect("think", "answer", label="done", style=ConnectorStyle.DASHED)

# Section groups the loop
d.section("Iterative Loop", ["observe", "think", "act"],
          style=SectionStyle(fill="#ede9e0", stroke="#b0a898", stroke_width=1.5,
                             corner_radius=16, label_font_size=18, label_color="#7a7060", padding=40))
d.save("cycle.drawio")
```

---

## 5. Decision Tree (Branching)

**Use when:** Conditional logic, routing, if/else, switches.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "How authentication routes requests", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)
d.add("check", "Authenticated?", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=1, col=1)
d.add("dash", "Dashboard", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=2, col=0)
d.add("login", "Login Page", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=2, col=2)

d.connect("check", "dash", source_anchor=AnchorName.BOTTOM_LEFT, target_anchor=AnchorName.TOP_CENTER, label="Yes")
d.connect("check", "login", source_anchor=AnchorName.BOTTOM_RIGHT, target_anchor=AnchorName.TOP_CENTER, label="No")
d.save("decision_tree.drawio")
```

---

## 6. Timeline (Temporal Progression)

**Use when:** Milestones, roadmaps, phases, schedules.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "Product roadmap from research to launch", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=0)
d.timeline(
    entries=[
        TimelineEntry("Q1", "Research"),
        TimelineEntry("Q2", "Build"),
        TimelineEntry("Q3", "Beta"),
        TimelineEntry("Q4", "Launch"),
    ],
    orientation=TimelineOrientation.HORIZONTAL,
    start_row=1, start_col=0,
)
d.save("timeline.drawio")
```

---

## 7. Hierarchy (Tree Structure)

**Use when:** Org charts, file systems, taxonomies, inheritance.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "System architecture layers", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=0)
d.tree(
    root=TreeNode("System", children=(
        TreeNode("Frontend", children=(
            TreeNode("React App"),
            TreeNode("Mobile App"),
        )),
        TreeNode("Backend", children=(
            TreeNode("API Server"),
            TreeNode("Workers"),
        )),
        TreeNode("Data", children=(
            TreeNode("PostgreSQL"),
            TreeNode("Redis"),
        )),
    )),
    start_row=1, start_col=0,
)
d.save("hierarchy.drawio")
```

---

## 8. Comparison (Side-by-Side)

**Use when:** Trade-offs, alternatives, before/after, pros/cons.

```python
d = Diagram(grid_config=GridConfig(cell_width=240, cell_height=160, margin=30))
d.add("title", "Why microservices beat monoliths at scale", role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# Left column
d.add("mono_h", "Monolith", role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=1, col=0)
d.add("mono_1", "Single Deploy", shape=ShapeKind.RECT, row=2, col=0)
d.add("mono_2", "Vertical Scaling", shape=ShapeKind.RECT, color=ColorTheme.WARNING, row=3, col=0)

# Right column
d.add("micro_h", "Microservices", role=TextRole.SUBTITLE, shape=ShapeKind.NONE, row=1, col=2)
d.add("micro_1", "Independent Deploy", shape=ShapeKind.RECT, row=2, col=2)
d.add("micro_2", "Horizontal Scaling", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=3, col=2)
d.save("comparison.drawio")
```

---

## Sections (Visual Grouping)

Use sections to group related elements in any pattern:

```python
d.section("Frontend", ["fe1", "fe2", "fe3"],
          style=SectionStyle(
              fill="#e8f0e8",       # light background
              stroke="#6a8a6a",     # border color
              stroke_width=1.5,
              corner_radius=16,
              label_font_size=18,
              label_color="#4a6a4a",
              padding=40,
          ))
```
