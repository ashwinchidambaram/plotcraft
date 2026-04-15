"""Decision tree: How to pick your database — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig,
    CalloutPosition,
)

# LAYOUT TABLE:
# row=0: title (col=1)
# row=1: start (col=1)
# row=3: decision (col=1)
# row=5: relational (col=0), document (col=2)
# row=6: callout_pg (col=0), callout_mongo (col=2)
# row=7: caption (col=1)

d = Diagram(grid_config=GridConfig(cell_width=280, cell_height=160, margin=30))

# Title
d.add("title", "How to pick your database",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# Entry
d.add("start", "New Project", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=1)

# Decision — short text for diamond
d.add("q1", "Structured?", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=3, col=1)

d.connect("start", "q1",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Two branches
d.add("sql", "PostgreSQL", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=5, col=0)
d.add("nosql", "MongoDB", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=5, col=2)

d.connect("q1", "sql",
          source_anchor=AnchorName.LEFT_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          label="Yes", line_weight=LineWeight.BOLD)
d.connect("q1", "nosql",
          source_anchor=AnchorName.RIGHT_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          label="No", line_weight=LineWeight.BOLD)

# Callouts for each choice
d.callout("c_sql", "ACID, joins,\ncomplex queries",
          "sql", position=CalloutPosition.BELOW)
d.callout("c_nosql", "Flexible schema,\nrapid iteration",
          "nosql", position=CalloutPosition.BELOW)

# Caption
d.add("caption", "Start simple, migrate when you outgrow it",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=8, col=1)

d.save("examples/decision.excalidraw")
print("Saved examples/decision.excalidraw")
