# PlotCraft

**Better diagrams from your AI.** PlotCraft is a Python library that gives LLMs the ability to create clean, well-designed diagrams. You describe what you want, PlotCraft handles the layout and rendering.

## Why?

AI-generated diagrams usually look terrible — misaligned text, arrows through shapes, everything the same size. PlotCraft fixes this by using [D2](https://d2lang.com) for intelligent layout and hand-drawn sketch rendering. The AI writes simple Python, D2 does the visual design.

## Two Modes

PlotCraft supports two fundamentally different diagram types:

### Flowcharts (Scene API → D2)

For **process flows, decisions, and sequences** — you describe elements and connections, D2 handles layout and routing automatically.

<p align="center">
  <img src="examples/renders/https.png" alt="HTTPS diagram" width="90%" />
</p>

<p align="center">
  <img src="examples/renders/startup.png" alt="Startup funding journey" width="90%" />
</p>

### Spatial Compositions (Excalidraw)

For **visual storytelling through density, quantity, and position** — where the spatial arrangement IS the information. Clusters of shapes, progressive narrowing, scattered elements that tell a story.

<p align="center">
  <img src="examples/renders/spatial_gradient_descent.png" alt="Gradient descent convergence" width="90%" />
</p>

### Themes

The same diagram in different color schemes:

<p align="center">
  <img src="examples/renders/theme_default.png" alt="Default theme" width="30%" />
  <img src="examples/renders/theme_earth.png" alt="Earth theme" width="30%" />
  <img src="examples/renders/theme_grape.png" alt="Grape theme" width="30%" />
</p>
<p align="center">
  <img src="examples/renders/theme_ocean.png" alt="Ocean theme" width="30%" />
  <img src="examples/renders/theme_cool.png" alt="Cool theme" width="30%" />
  <img src="examples/renders/theme_mixed.png" alt="Mixed theme" width="30%" />
</p>

## Install

```bash
pip install plotcraft
```

You'll also need D2 for rendering:

```bash
# macOS
brew install d2

# Linux
curl -fsSL https://d2lang.com/install.sh | sh
```

## Quick Start

```python
from plotcraft import Scene

s = Scene()
s.add("How HTTPS keeps your data safe", role="title")
s.add("You type a URL", role="start")
s.add("TLS Handshake", role="process", emphasis="high")
s.add("Certificate Check", role="decision")
s.add("Encrypted Tunnel", role="process", size="large", emphasis="high")
s.add("Page Loads", role="end")

s.connect("You type a URL", "TLS Handshake")
s.connect("TLS Handshake", "Certificate Check")
s.connect("Certificate Check", "Encrypted Tunnel", label="valid")
s.connect("Encrypted Tunnel", "Page Loads")

s.annotate("AES-256 encryption", near="Encrypted Tunnel")
s.add("Every request, invisible, in milliseconds", role="caption")

s.layout("pipeline")
s.save("https.png")
```

## How It Works

1. **You describe elements** — give each a role (`start`, `process`, `decision`, `end`) and optionally `emphasis` and `size`
2. **You connect them** — PlotCraft figures out the arrow routing
3. **You pick a layout** — `pipeline`, `top_down`, `fan_out`, `cycle`, `decision_tree`, `convergence`
4. **D2 renders it** — sketch mode for a hand-drawn aesthetic, dagre for intelligent positioning

No coordinates. No anchor points. No grid cells. Just content and relationships.

## Themes

PlotCraft ships with 9 color themes:

```python
Scene(theme="default")   # clean blues
Scene(theme="earth")     # warm browns
Scene(theme="grape")     # rich purples
Scene(theme="ocean")     # cool teals
Scene(theme="vanilla")   # soft yellows
Scene(theme="cool")      # muted pastels
Scene(theme="mixed")     # colorful variety
Scene(dark=True)         # dark mode
```

## API Reference

```python
from plotcraft import Scene

# Create a scene
s = Scene(
    dark=False,          # dark mode
    theme="default",     # color scheme
)

# Add elements
s.add(text,
    role="process",      # title, subtitle, start, end, process, decision, caption
    size="medium",       # small, medium, large, hero
    emphasis="normal",   # low, normal, high
)

# Connect elements (by their text)
s.connect(source, target,
    label=None,          # text on the arrow
    style="solid",       # solid, dashed, dotted
    weight="normal",     # thin, normal, bold
)

# Add floating annotations
s.annotate(text, near=element_text)

# Choose layout and render
s.layout("pipeline")     # pipeline, top_down, fan_out, convergence, cycle, decision_tree
s.save("diagram.png")    # .png, .svg, .d2, .excalidraw
```

## Element Roles

| Role | Shape | Best for |
|------|-------|----------|
| `"title"` | floating text | Diagram title — states the insight |
| `"subtitle"` | floating text | Section headers |
| `"start"` | oval | Entry points, triggers |
| `"end"` | oval | Results, outcomes |
| `"process"` | rectangle | Steps, actions, states |
| `"decision"` | diamond | Branch points, conditions |
| `"caption"` | floating text | Closing insight |

## Claude Code Skill

PlotCraft includes a Claude Code skill at `skills/plotcraft-diagram/` that teaches AI assistants the design methodology — when to use which layout, how to pick roles, and how to write effective diagram titles.

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
