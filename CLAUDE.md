# PlotCraft

AI-friendly diagram engine — text-driven, grid-snapped SVG generation for LLM agents.

## Tech Stack

- Python 3.12+
- uv (package manager)
- Pure Python SVG generation (no external rendering dependencies)

## Directory Structure

```
plotcraft/
├── src/plotcraft/       # Main package
├── tests/               # Test suite
├── docs/                # Documentation
└── pyproject.toml       # Project config (uv-managed)
```

## Architecture

### Core Concepts

1. **Grid** — coordinate system that all elements snap to; prevents bounding box overlaps
2. **Containers** — shapes (rect, square, circle, oval) that wrap text content and auto-scale
3. **Text elements** — semantic types: title, subtitle, caption, text — each with sizing rules
4. **Anchor points** — corners + midpoints on every shape, used as connector attachment points
5. **Connectors** — curved arrows that route between anchors, avoiding shapes but able to cross bounding box margins
6. **Bounding boxes** — invisible margin around each shape; exclusive grid occupancy (no overlaps)

### LLM Workflow

1. Determine elements to present (text content)
2. Classify each element (title, subtitle, caption, text)
3. Define connections between elements
4. Choose shape for each element
5. PlotCraft handles layout, sizing, and SVG rendering

### Design Rules

- No sharp edges — all corners and connectors are rounded/curved
- Shapes scale to fit text, maintaining proportions
- Grid-based placement ensures clean, non-overlapping layouts
- Connectors route intelligently around shapes

## Conventions

- Tests go in `tests/` with `test_` prefix
- Run tests: `uv run pytest`
