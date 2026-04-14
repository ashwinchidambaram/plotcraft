# Plan A: Improved SVG Renderer + Design Advisor + Optional Draw.io Skill

**Status:** Proposed
**Priority:** Core improvements to make PlotCraft self-contained and pip-installable

## Summary

Upgrade PlotCraft's pure Python SVG renderer with draw.io-inspired routing, anchoring, and text layout — making it a fully self-contained `pip install plotcraft` with zero external dependencies. Separately ship a Claude skill for optional draw.io integration.

## Two Tiers

### Tier 1: PlotCraft Core (pip-installable)
- **Orthogonal edge router** — A* or L/Z routing that goes around shapes
- **Anchor system overhaul** — connectors hit visible shape edges, not bounding boxes
- **SVG renderer upgrades** — filled triangle arrowheads, rounded corner bends, better text centering
- **Design advisor** — pattern catalog + diagram validation based on Excalidraw methodology
- **Wobble stays native** — hand-drawn aesthetic applied directly in SVG generation

### Tier 2: Draw.io Skill (optional)
- Lives in `skills/drawio/` in the repo
- Converts PlotCraft model → `.drawio` XML → draw.io CLI → PNG/SVG
- Only works when draw.io app is installed
- Clean dependency: skill imports PlotCraft, not vice versa

## Key Technical Work

1. **Orthogonal router** (`routing.py`) — L/Z-shaped paths that avoid obstacles, rounded corners at bends
2. **Shape-aware anchors** (`shapes.py`) — diamond vertices, circle circumference projection, gap parameter
3. **SVG upgrades** (`svg.py`) — orthogonal path rendering, filled arrowheads, proper diamond text centering
4. **Advisor** (`advisor.py`) — pattern suggestion, diagram validation rules
5. **Draw.io skill** (`skills/drawio/`) — XML generation, CLI wrapper, fallback handling

## Pros
- Fully self-contained — `pip install plotcraft` just works
- No external dependencies beyond cairosvg (optional, for PNG)
- Preserves hand-drawn wobble aesthetic natively
- Draw.io available as bonus when installed

## Cons
- Orthogonal routing is complex to implement well (the hard part)
- Won't match draw.io's routing quality initially
- More code to maintain (own router vs delegating to draw.io)

## Estimated Effort
- 4 parallel waves of subagent work
- Wave 1 (router + anchors + advisor) is the bulk
- ~7 implementation tasks + tests
