# PlotCraft

AI-friendly diagram engine — freeform Scene API with D2 rendering for LLM agents.

## Tech Stack

- Python 3.12+
- uv (package manager)
- D2 (`d2lang.com`) — layout engine + sketch-mode rendering (installed at /opt/homebrew/bin/d2)
- Excalidraw JSON — alternative hand-drawn output format
- Pure Python SVG generation (legacy, self-contained)

## Directory Structure

```
plotcraft/
├── src/plotcraft/       # Main package
│   ├── scene.py         # PRIMARY: Freeform Scene API with D2/Excalidraw backends
│   ├── diagram.py       # Legacy grid-based Diagram API
│   └── ...              # Grid, shapes, routing, renderers
├── tests/               # Test suite (pytest)
├── examples/            # Example diagram scripts
│   ├── demo_scene_d2_all.py  # All 5 Scene+D2 examples
│   └── renders/              # Generated SVG/PNG outputs
├── skills/              # Claude Code skills
│   └── plotcraft-diagram/    # Diagram creation skill with design methodology
├── docs/                # Documentation and specs
└── pyproject.toml       # Project config (uv-managed)
```

## Architecture

### Primary: Scene API + D2

The recommended workflow for creating diagrams:

1. **Scene API** (`scene.py`) — freeform declarative API where the LLM describes WHAT (elements, connections, roles) and the engine decides WHERE
2. **D2 Backend** — generates D2 markup, renders via D2 CLI with `--sketch` for hand-drawn aesthetic. D2's dagre layout handles text centering, arrow routing, and element positioning.
3. **Excalidraw Backend** — alternative output generating `.excalidraw` JSON directly with computed pixel positions

```python
from plotcraft import Scene

s = Scene()
s.add("Start", role="start")
s.add("Process", role="process", emphasis="high")
s.add("End", role="end")
s.connect("Start", "Process")
s.connect("Process", "End")
s.layout("pipeline")
s.save("diagram.svg")  # D2 rendering (default)
```

### Legacy: Grid-based Diagram API

The original grid-based API remains for backward compatibility:

1. **Diagram API** (`diagram.py`) — fluent builder: `.add()`, `.connect()`, `.section()`, `.render()`
2. **Grid** (`grid.py`) — cell-based placement, auto-place, cell spanning
3. **Shapes/Routing/Connectors** — auto-sizing, anchor resolution, orthogonal routing
4. **Renderers** — Excalidraw JSON, SVG (wobble), draw.io XML
5. **Advisor** (`advisor.py`) — 10 visual pattern suggestions, diagram validation

### Design System

- **D2 output**: Sketch mode (hand-drawn), semantic colors (Terracotta/Sage/Gold), dagre layout
- **Excalidraw output**: roughness=1, fontFamily=3, Terracotta/Sage/Gold palette on Sand canvas (#F9F7F4)
- **SVG output** (legacy): Caveat/Patrick Hand/Indie Flower fonts, wobble paths, cream canvas


## Conventions

- Tests go in `tests/` with `test_` prefix
- Run tests: `uv run pytest`
- Examples go in `examples/`, renders in `examples/renders/`
- Generated outputs (*.png, *.svg, *.drawio, *.excalidraw) are gitignored (except renders/)
- The plotcraft-diagram skill at `skills/plotcraft-diagram/` embeds design methodology
- Scene API is the primary API; Diagram API is legacy
