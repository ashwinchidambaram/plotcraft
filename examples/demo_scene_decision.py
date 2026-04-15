"""Scene API demo: decision tree."""

from plotcraft.scene import Scene

s = Scene(width=1000, height=650)

s.add("Picking your database", role="title")
s.add("Structured?", role="decision", size="large")
s.add("PostgreSQL", role="end", size="large")
s.add("MongoDB", role="end", size="large")

s.connect("Structured?", "PostgreSQL", label="Yes")
s.connect("Structured?", "MongoDB", label="No")

s.annotate("ACID, joins,\ncomplex queries", near="PostgreSQL", position="below")
s.annotate("Flexible schema,\nrapid iteration", near="MongoDB", position="below")

s.add("Start simple, migrate when you outgrow it", role="caption")

s.layout("decision_tree")
s.save("examples/scene_decision.excalidraw")
print("Saved examples/scene_decision.excalidraw")
