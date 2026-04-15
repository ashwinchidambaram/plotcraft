# PlotCraft

AI-friendly diagram engine — freeform Scene API with D2 rendering for LLM agents.

## What is this?

PlotCraft is a Python library that lets AI agents create clean, well-designed diagrams without thinking in pixels or coordinates. The AI describes **elements and relationships**, PlotCraft generates D2 markup, and D2 handles layout, text centering, and arrow routing.

## Features

- **Scene API** — declarative: describe what, not where
- **D2 rendering** — sketch mode for hand-drawn aesthetic, dagre layout for intelligent positioning
- **Role-based styling** — elements get shapes and colors from their semantic role (start, end, process, decision)
- **Emphasis system** — `emphasis="high"` makes elements visually dominant
- **Annotations** — floating context near any element
- **Dark theme** — `Scene(dark=True)` for dark canvas with warm colors
- **Multiple backends** — D2 (primary), Excalidraw JSON, SVG, draw.io XML

## Prerequisites

```bash
# Install PlotCraft
uv sync

# Install D2 (required for rendering)
brew install d2
```

## Quick Start

```python
from plotcraft import Scene

s = Scene()
s.add("How a commit becomes a release", role="title")
s.add("Push Code", role="start")
s.add("Run Tests", role="process", emphasis="high")
s.add("Code Review", role="process")
s.add("Deploy", role="end")

s.connect("Push Code", "Run Tests")
s.connect("Run Tests", "Code Review")
s.connect("Code Review", "Deploy")

s.annotate("Automated CI", near="Run Tests")

s.add("Every step is automated", role="caption")

s.layout("pipeline")
s.save("pipeline.svg")  # D2 renders with sketch mode
```

## Output Formats

| Format | Command | Backend | Dependencies |
|--------|---------|---------|-------------|
| `.svg` | `s.save("out.svg")` | D2 (default) | D2 CLI |
| `.png` | `s.save("out.png")` | D2 (default) | D2 CLI |
| `.d2` | `s.save("out.d2")` | D2 source | None |
| `.excalidraw` | `s.save("out.excalidraw")` | Excalidraw JSON | None |

## Layout Patterns

```python
s.layout("pipeline")       # horizontal left-to-right
s.layout("top_down")       # vertical top-to-bottom
s.layout("fan_out")        # one source, many targets
s.layout("convergence")    # many sources, one target
s.layout("cycle")          # circular loop
s.layout("decision_tree")  # branching from root
```

## Element Roles

| Role | Shape | Use for |
|------|-------|---------|
| `"title"` | text | Diagram title |
| `"subtitle"` | text | Section headers |
| `"start"` | oval | Entry points |
| `"end"` | oval | Terminal states |
| `"process"` | rectangle | Steps, actions |
| `"decision"` | diamond | Branch points |
| `"caption"` | text | Closing insight |

## Examples

```bash
# Generate all Scene+D2 examples
uv run python examples/demo_scene_d2_all.py

# Generate GEPA research diagrams
uv run python examples/demo_gepa_final.py
```

## Claude Code Skill

The `skills/plotcraft-diagram/` directory contains a Claude Code skill that guides LLMs through creating effective diagrams with the Scene API.

## Project Structure

```
plotcraft/
├── src/plotcraft/
│   ├── scene.py              # PRIMARY: Scene API + D2/Excalidraw backends
│   ├── diagram.py            # Legacy grid-based API
│   ├── excalidraw_renderer.py # Excalidraw JSON generation
│   ├── advisor.py            # Design pattern advisor
│   └── ...                   # Grid, shapes, routing, SVG, draw.io
├── tests/                    # 143 tests
├── examples/                 # Example scripts
├── skills/plotcraft-diagram/ # Claude Code skill
└── pyproject.toml
```

## Running Tests

```bash
uv run pytest
```

## Legacy API

The original grid-based `Diagram` API is still available for backward compatibility:

```python
from plotcraft import Diagram, ShapeKind, ColorTheme

d = Diagram()
d.add("a", "Start", shape=ShapeKind.OVAL, color=ColorTheme.START, row=0, col=0)
d.add("b", "End", shape=ShapeKind.OVAL, color=ColorTheme.END, row=0, col=1)
d.connect("a", "b")
d.save("diagram.excalidraw")
```
