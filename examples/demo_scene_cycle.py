"""Scene API demo: cycle / feedback loop."""

from plotcraft.scene import Scene

s = Scene(width=1000, height=700)

s.add("How AI agents think", role="title")
s.add("Observe", role="process", size="large", emphasis="high")
s.add("Think", role="decision", size="medium")
s.add("Act", role="process", size="large")

s.connect("Observe", "Think")
s.connect("Think", "Act", label="execute")
s.connect("Act", "Observe", label="feedback", style="dashed")

s.annotate("Gather context\nfrom environment", near="Observe", position="right")
s.annotate("Choose next\naction", near="Think", position="right")

s.add("Repeat until goal is reached", role="caption")

s.layout("cycle")
s.save("examples/scene_cycle.excalidraw")
print("Saved examples/scene_cycle.excalidraw")
