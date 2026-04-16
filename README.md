# PlotCraft

**Better diagrams from your AI.** Describe what you want in Python, get a polished hand-drawn diagram back.

<p align="center">
  <img src="examples/renders/compiler_pipeline.png" alt="How a compiler works" width="90%" />
</p>

<p align="center">
  <img src="examples/renders/neural_network_learning.png" alt="How a neural network learns" width="90%" />
</p>

<p align="center">
  <img src="examples/renders/startup_death.png" alt="How startups die" width="90%" />
</p>

## Why?

AI-generated diagrams usually look terrible — misaligned text, arrows through shapes, everything the same size. PlotCraft fixes this by using [D2](https://d2lang.com) for intelligent layout and hand-drawn sketch rendering.

No coordinates. No anchor points. No grid cells. Just content and relationships.

## Install

```bash
pip install plotcraft
brew install d2        # rendering engine
```

## Quick Start

```python
from plotcraft import Scene

s = Scene()
s.add("How a neural network learns", role="title")
s.add("Training Data", role="start")
s.add("Forward Pass", role="process", emphasis="high")
s.add("Compute Loss", role="decision")
s.add("Backpropagation", role="process", size="large", emphasis="high")
s.add("Update Weights", role="process")
s.add("Trained Model", role="end", size="large")

s.connect("Training Data", "Forward Pass")
s.connect("Forward Pass", "Compute Loss", label="predictions")
s.connect("Compute Loss", "Backpropagation", label="error signal")
s.connect("Backpropagation", "Update Weights", label="gradients")
s.connect("Update Weights", "Forward Pass", label="next batch", style="dashed")

s.annotate("Chain rule through every layer", near="Backpropagation")
s.add("Repeat until the loss stops decreasing", role="caption")

s.layout("top_down")
s.save("neural_net.png")
```

## Themes

<p align="center">
  <img src="examples/renders/theme_default.png" alt="Default" width="30%" />
  <img src="examples/renders/theme_earth.png" alt="Earth" width="30%" />
  <img src="examples/renders/theme_grape.png" alt="Grape" width="30%" />
</p>
<p align="center">
  <img src="examples/renders/theme_ocean.png" alt="Ocean" width="30%" />
  <img src="examples/renders/theme_cool.png" alt="Cool" width="30%" />
  <img src="examples/renders/theme_mixed.png" alt="Mixed" width="30%" />
</p>

```python
Scene(theme="default")   Scene(theme="earth")    Scene(theme="grape")
Scene(theme="ocean")     Scene(theme="vanilla")  Scene(theme="cool")
Scene(theme="mixed")     Scene(dark=True)
```

## API

```python
from plotcraft import Scene

s = Scene(theme="default", dark=False)

# Elements
s.add(text, role="process", size="medium", emphasis="normal")
# Roles: title, subtitle, start, end, process, decision, caption
# Sizes: small, medium, large, hero
# Emphasis: low, normal, high

# Connections
s.connect(source, target, label=None, style="solid", weight="normal")

# Annotations
s.annotate(text, near=element_text)

# Layout + render
s.layout("pipeline")      # pipeline, top_down, fan_out, convergence, cycle, decision_tree
s.save("diagram.png")     # .png, .svg, .d2, .excalidraw
```

## Design Rules

PlotCraft ships with [`docs/DESIGN_RULES.md`](docs/DESIGN_RULES.md) — a comprehensive guide for creating diagrams that look right on the first try. Spacing rules, arrow rules, text placement, and a pre-flight checklist, all learned from real iteration.

## Development

```bash
git clone https://github.com/ashwinchidambaram/plotcraft
cd plotcraft
uv sync
uv run pytest
```

---

<p align="center">
  <a href="https://github.com/ashwinchidambaram"><img src="assets/ac-blackhole-static.svg" alt="Built by Ashwin Chidambaram" width="260" /></a>
</p>
