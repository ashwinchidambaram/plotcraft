# PlotCraft

AI-friendly diagram engine — text-driven, grid-snapped SVG/draw.io generation for LLM agents.

## Tech Stack

- Python 3.12+
- uv (package manager)
- Pure Python SVG generation (self-contained, no external dependencies)
- Optional: draw.io desktop app for high-quality rendering

## Directory Structure

```
plotcraft/
├── src/plotcraft/       # Main package
├── tests/               # Test suite (pytest)
├── examples/            # Example diagram scripts
├── skills/              # Claude Code skills
│   └── plotcraft-diagram/ # Diagram creation skill with design methodology
├── docs/                # Documentation and specs
├── ref/                 # Design references (Figma, Google AI Studio)
└── pyproject.toml       # Project config (uv-managed)
```

## Architecture

### Core Pipeline

1. **Diagram API** (`diagram.py`) — fluent builder: `.add()`, `.connect()`, `.section()`, `.callout()`, `.note()`, `.decorate()`, `.render()`
2. **Grid** (`grid.py`) — cell-based placement, auto-place, cell spanning
3. **Shapes** (`shapes.py`) — auto-sizing, anchor resolution (shape-aware: diamond vertices, circle circumference)
4. **Routing** (`routing.py`) — orthogonal L/Z/U routing around obstacles with rounded corners
5. **Connectors** (`connectors.py`) — routing integration, bezier fallback
6. **Excalidraw Renderer** (`excalidraw_renderer.py`) — **primary output**, generates `.excalidraw` JSON with hand-drawn aesthetic (roughness=1), Terracotta/Sage/Gold palette, dark theme support
7. **SVG Renderer** (`svg.py`) — hand-drawn wobble aesthetic, Google Fonts, translucent fills
8. **Draw.io Renderer** (`drawio_renderer.py`) — generates `.drawio` XML for high-quality export
9. **Advisor** (`advisor.py`) — 10 visual pattern suggestions, diagram validation

### Design System

- Fonts: Caveat (titles), Patrick Hand (body), Indie Flower (captions)
- Colors: 9 semantic themes with translucent fills (0.5-0.6 opacity)
- Canvas: #fdf6e3 (warm cream)
- Wobble: seeded random noise for hand-drawn paths
- Grid: 160x120 cells (SVG), 260x160 recommended for draw.io and Excalidraw

### Triple Output

- **Excalidraw** (primary): Hand-drawn aesthetic via roughness=1, Terracotta/Sage/Gold palette, Playwright PNG verification
- **SVG**: Self-contained, pip-installable, hand-drawn wobble aesthetic
- **Draw.io**: Higher quality routing/text, requires draw.io app

## Conventions

- Tests go in `tests/` with `test_` prefix
- Run tests: `uv run pytest`
- Examples go in `examples/`
- Generated outputs (*.png, *.drawio) are gitignored
- The plotcraft-diagram skill at `skills/plotcraft-diagram/` embeds design methodology
