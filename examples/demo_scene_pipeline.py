"""Scene API demo: pipeline diagram."""

from plotcraft.scene import Scene

s = Scene(width=1200, height=500)

s.add("How a commit becomes a release", role="title")
s.add("Push Code", role="start")
s.add("Run Tests", role="process", size="large", emphasis="high")
s.add("Code Review", role="process")
s.add("Deploy", role="end")

s.connect("Push Code", "Run Tests")
s.connect("Run Tests", "Code Review")
s.connect("Code Review", "Deploy")

s.annotate("Automated CI", near="Run Tests", position="above")
s.annotate("Manual gate", near="Code Review", position="below")

s.add("Every step is automated, every gate must pass", role="caption")

s.layout("pipeline")
s.save("examples/scene_pipeline.excalidraw")
print("Saved examples/scene_pipeline.excalidraw")
