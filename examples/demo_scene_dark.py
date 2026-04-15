"""Scene API demo: dark theme top-down flow."""

from plotcraft.scene import Scene

s = Scene(width=800, height=750, dark=True)

s.add("The ML Pipeline", role="title")
s.add("Raw Data", role="start", size="large")
s.add("Preprocess", role="process", emphasis="high")
s.add("Train", role="process", size="large")
s.add("Evaluate", role="process")
s.add("Deploy", role="end", size="large")

s.connect("Raw Data", "Preprocess")
s.connect("Preprocess", "Train")
s.connect("Train", "Evaluate")
s.connect("Evaluate", "Deploy")

s.annotate("Clean, normalize,\nfeature engineer", near="Preprocess", position="right")
s.annotate("GPU-accelerated", near="Train", position="right")

s.add("Iterate fast, deploy confidently", role="caption")

s.layout("top_down")
s.save("examples/scene_dark.excalidraw")
print("Saved examples/scene_dark.excalidraw")
