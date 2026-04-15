# PlotCraft Diagram Skill

A Claude Code skill for creating polished, argument-driven diagrams using PlotCraft's Python API.

## Output

Primary output is **Excalidraw JSON** (`.excalidraw`) with a hand-drawn aesthetic. Draw.io and SVG remain available as alternatives.

## Setup

### 1. Install PlotCraft

```bash
cd /Users/ashwinchidambaram/dev/projects/plotcraft
uv sync
```

### 2. Install Render Pipeline (for PNG verification)

```bash
cd skills/plotcraft-diagram/references
uv sync
uv run playwright install chromium
```

### 3. Verify

```bash
# Test PlotCraft
uv run python -c "from plotcraft import Diagram; print('PlotCraft OK')"

# Test render pipeline
cd skills/plotcraft-diagram/references
uv run python render_excalidraw.py --help
```

## Usage

Just ask Claude to create a diagram:

- "Draw a diagram of the ReAct agent loop"
- "Create a flowchart showing how authentication works"
- "Visualize our deployment pipeline"
- "Create a visual essay comparing monolith vs microservices"

The skill will:
1. Plan the diagram using visual design methodology
2. Choose the right pattern (pipeline, cycle, decision tree, etc.)
3. Generate PlotCraft Python code
4. Export to Excalidraw JSON with hand-drawn aesthetic
5. Render to PNG for verification
6. Iterate until the diagram is polished

## What Makes This Different

- **Design methodology embedded** -- follows Patrick Winston's communication framework (5S: Symbol, Slogan, Surprise, Salient idea, Story)
- **Argues, doesn't display** -- diagrams make visual arguments, not formatted text
- **Build-in-passes workflow** -- layout table -> shapes -> connectors prevents LLM drift
- **Visual essay support** -- callouts, notes, decoratives, sections for multi-part compositions
- **Render-verify loop** -- Playwright-based PNG export for visual quality checks
- **Hand-drawn aesthetic** -- Excalidraw's roughness=1 with Terracotta/Sage/Gold palette
