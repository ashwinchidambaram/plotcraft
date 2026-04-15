"""Decision tree: How to choose a database — rendered to Excalidraw."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig,
    CalloutPosition,
)

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Title
d.add("title", "How to Choose a Database",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=2)

# Entry point
d.add("start", "New Project\nNeeds a DB", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=2)

# Central decision diamond
d.add("q1", "Structured\ndata?", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=3, col=2)

# Connect start -> decision (skip row 2 for vertical connector)
d.connect("start", "q1",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# Left branch: structured -> relational vs analytical
d.add("relational", "Relational DB\n(PostgreSQL)", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=3, col=0)
d.connect("q1", "relational",
          source_anchor=AnchorName.LEFT_CENTER,
          target_anchor=AnchorName.RIGHT_CENTER,
          label="Yes")

# Right branch: unstructured -> document vs graph
d.add("nosql_q", "Relationships\nmatter?", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=3, col=4)
d.connect("q1", "nosql_q",
          source_anchor=AnchorName.RIGHT_CENTER,
          target_anchor=AnchorName.LEFT_CENTER,
          label="No")

# NoSQL branches
d.add("document", "Document Store\n(MongoDB)", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=5, col=3)
d.add("graph", "Graph DB\n(Neo4j)", shape=ShapeKind.RECT, color=ColorTheme.SUCCESS, row=5, col=5)

d.connect("nosql_q", "document",
          source_anchor=AnchorName.BOTTOM_LEFT,
          target_anchor=AnchorName.TOP_CENTER,
          label="No")
d.connect("nosql_q", "graph",
          source_anchor=AnchorName.BOTTOM_RIGHT,
          target_anchor=AnchorName.TOP_CENTER,
          label="Yes")

# Callouts explaining when to use each
d.callout("c_pg", "ACID compliance,\ncomplex queries,\njoins galore",
          "relational", position=CalloutPosition.BELOW, color=ColorTheme.INFO)

d.callout("c_mongo", "Flexible schema,\nrapid iteration,\nJSON-native",
          "document", position=CalloutPosition.BELOW, color=ColorTheme.HIGHLIGHT)

d.callout("c_neo", "Social networks,\nfraud detection,\npath queries",
          "graph", position=CalloutPosition.BELOW, color=ColorTheme.SUCCESS)

# Caption
d.add("caption", "Start with the simplest option that fits your access patterns",
      role=TextRole.CAPTION, shape=ShapeKind.NONE, row=7, col=2)

d.save("examples/decision.excalidraw")
print("Saved examples/decision.excalidraw")
