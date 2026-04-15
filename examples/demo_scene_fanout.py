"""Scene API demo: fan-out pattern."""

from plotcraft.scene import Scene

s = Scene(width=1100, height=600)

s.add("How events propagate", role="title")
s.add("Event Bus", role="start", size="large")
s.add("Logger", role="process")
s.add("Notifier", role="process", emphasis="high")
s.add("Archiver", role="process")
s.add("Analytics", role="process", emphasis="low")

s.connect("Event Bus", "Logger")
s.connect("Event Bus", "Notifier")
s.connect("Event Bus", "Archiver")
s.connect("Event Bus", "Analytics")

s.annotate("Real-time alerts", near="Notifier", position="below")

s.add("Every event reaches every consumer", role="caption")

s.layout("fan_out")
s.save("examples/scene_fanout.excalidraw")
print("Saved examples/scene_fanout.excalidraw")
