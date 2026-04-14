# Plan B: Draw.io as Primary Rendering Backend

**Status:** Proposed (original plan, revised after self-contained constraint)

## Summary

Use draw.io as PlotCraft's primary rendering engine. PlotCraft generates `.drawio` XML, shells out to draw.io CLI for export, and optionally applies wobble post-processing to the resulting SVG.

## Architecture

```
Diagram Python API → .drawio XML → draw.io CLI → SVG → wobble post-process → final output
```

## Key Technical Work

1. **DrawioRenderer** (`drawio_renderer.py`) — converts PlotCraft model to mxGraphModel XML
2. **CLI wrapper** (`drawio_cli.py`) — detects and invokes draw.io CLI
3. **SVG post-processor** (`svg_postprocess.py`) — applies wobble to draw.io-exported SVG
4. **Anchor mapping** — PlotCraft AnchorName → draw.io exitX/exitY/entryX/entryY
5. **Advisor** (`advisor.py`) — same as Plan A

## Pros
- Draw.io handles ALL hard rendering problems (routing, text, anchoring)
- Highest quality output — 10+ years of draw.io engineering
- Less code to write and maintain
- `.drawio` files can be opened and edited in draw.io app

## Cons
- **Requires draw.io app** (200MB Electron app, not pip-installable)
- Not self-contained — breaks `pip install plotcraft` as a standalone tool
- System dependency that varies by OS
- Wobble post-processing adds complexity (parsing draw.io's SVG output)

## Revised Role

After the self-contained constraint, this plan becomes the **optional skill** (Tier 2) in Plan A rather than the primary approach. The draw.io integration ships as a Claude skill in `skills/drawio/` that enhances PlotCraft when draw.io is installed, but PlotCraft works fully without it.

## When This Makes Sense as Primary

- If the user always has draw.io installed
- If output quality matters more than portability
- If PlotCraft is used as a local tool, not distributed via pip
