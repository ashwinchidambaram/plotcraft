# PlotCraft

AI-friendly diagram engine — text-driven, grid-snapped diagram generation for LLM agents. Outputs SVG (self-contained) or draw.io XML (high-quality rendering).

## What is this?

PlotCraft is a Python library that lets AI agents create clean, well-laid-out diagrams without thinking in pixels or coordinates. The AI describes **content and relationships**, and PlotCraft handles geometry, layout, and rendering.

## Features

- **Text-driven containers** — shapes auto-scale to fit text content
- **Grid-snapped layout** — bounding boxes snap to a grid, preventing overlaps
- **Orthogonal routing** — connectors route around shapes with right-angle paths and rounded corners
- **Shape-aware anchors** — connectors attach to actual shape edges (diamond vertices, circle circumference)
- **Hand-drawn aesthetic** — wobbly paths, handwriting fonts, translucent fills (SVG output)
- **Draw.io export** — `.drawio` files for high-quality rendering via draw.io app
- **Design advisor** — pattern suggestions and diagram validation based on visual design methodology
- **9 color themes** — semantic colors (start, end, decision, error, highlight, info, success, warning)
- **6 shape types** — rect, square, circle, oval, diamond, free-text

## Setup

```bash
uv sync
```

## Quick Start

```python
from plotcraft import *

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

d.add("title", "How code reaches production",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)
d.add("commit", "Push", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
d.add("ci", "Run CI", shape=ShapeKind.RECT, row=1, col=1)
d.add("deploy", "Deploy", shape=ShapeKind.OVAL, color=ColorTheme.END, row=1, col=2)

d.connect("commit", "ci")
d.connect("ci", "deploy")

d.save("pipeline.drawio")  # Open in draw.io for best quality
d.save("pipeline.svg")     # Self-contained SVG
```

## Output Formats

| Format | Command | Quality | Dependencies |
|--------|---------|---------|-------------|
| `.drawio` | `d.save("out.drawio")` | Best (via draw.io app) | draw.io desktop app |
| `.svg` | `d.save("out.svg")` | Good (hand-drawn style) | None |
| `.png` | `d.save("out.png")` | Good | cairosvg |

## Claude Skill

The `skills/plotcraft-diagram/` directory contains a Claude Code skill that guides LLMs through creating effective diagrams. It embeds design methodology from Patrick Winston's MIT communication framework and Excalidraw's visual design system.

Install: `ln -s /path/to/plotcraft/skills/plotcraft-diagram ~/.claude/skills/plotcraft-diagram`

## Project Structure

```
plotcraft/
├── src/plotcraft/        # Main package
│   ├── diagram.py        # Public API (Diagram class)
│   ├── types.py          # Enums, dataclasses, defaults
│   ├── shapes.py         # Shape creation + anchor resolution
│   ├── grid.py           # Grid-based layout
│   ├── connectors.py     # Connector routing (orthogonal + bezier)
│   ├── routing.py         # Orthogonal path router
│   ├── svg.py            # SVG renderer (hand-drawn wobble)
│   ├── wobble.py         # Hand-drawn path noise
│   ├── drawio_renderer.py # Draw.io XML generation
│   ├── advisor.py        # Design pattern advisor
│   ├── structures.py     # Timelines and trees
│   └── text.py           # Font metrics and text measurement
├── tests/                # Test suite
├── examples/             # Example diagram scripts
├── skills/               # Claude Code skills
│   └── plotcraft-diagram/ # Diagram creation skill
├── docs/                 # Documentation and specs
└── ref/                  # Design references
```

## Running Tests

```bash
uv run pytest
```
