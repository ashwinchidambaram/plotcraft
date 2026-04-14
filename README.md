# PlotCraft

AI-friendly diagram engine — text-driven, grid-snapped SVG generation designed for LLM agents.

## What is this?

PlotCraft is a Python library that lets AI agents create clean, well-laid-out diagrams without thinking in pixels or coordinates. The AI describes **content and relationships**, and PlotCraft handles geometry, layout, and rendering.

## Core Concepts

- **Text-driven containers** — shapes auto-scale to fit their text content
- **Grid-snapped layout** — bounding boxes snap to a grid, preventing overlaps
- **Anchor points** — corners and midpoints on every shape for connector routing
- **Smart connectors** — arrows route between anchors, avoiding shapes but crossing bounding box margins
- **Rounded edges** — all shapes and connectors use curved edges
- **Semantic elements** — title, subtitle, caption, body text with distinct hierarchy

## Setup

```bash
uv sync
```

## Usage

```python
import plotcraft
# API coming soon
```
