# PlotCraft — Planning Prompt

Use this prompt to start a new Claude Code session for planning the PlotCraft build.

---

## The Prompt

You are about to plan and build **PlotCraft** — a pure-Python SVG diagram engine designed specifically for LLMs to use. Not for humans to use directly. For you. You are the user.

### Why this exists

You've tried to make diagrams before. Think about what goes wrong every time:

- You don't have spatial reasoning. You guess at coordinates and things overlap, clip, or float in dead space.
- You can't see what you're producing. You output SVG or Mermaid and hope it looks right. It usually doesn't.
- You have no reliable way to size a shape around text. You hardcode width/height and the text overflows or the box is comically large.
- Connectors are a nightmare. You draw a line from point A to point B and it cuts straight through other elements.
- You have no concept of layout. You place things at arbitrary (x, y) positions and the result looks like a ransom note.

PlotCraft solves all of this by giving you a system where you never think in pixels or coordinates. You think in **content and relationships**, and the engine handles geometry, sizing, and layout.

### What PlotCraft is

A Python library that generates SVG diagrams. It has these core properties:

1. **Text-driven containers.** You declare text content. A shape (rectangle, square, circle, oval) wraps around it and auto-scales to fit. The text has a maximum font size; the shape grows to enclose it proportionally. You never specify dimensions manually.

2. **Semantic element types.** Each piece of text is classified as a title, subtitle, caption, or body text. Each type has its own sizing and styling rules, creating visual hierarchy automatically.

3. **Anchor points.** Every shape exposes its corners and edge midpoints as named connection points. Connectors attach to these anchors — you never calculate intersection coordinates.

4. **Grid-based layout with bounding boxes.** Every shape has an invisible bounding box that snaps to a grid. Where one bounding box exists, another cannot be placed. This guarantees no overlapping elements. You place things by grid position, not pixel coordinates.

5. **Smart connectors.** Arrows route between anchor points on different shapes. They path-find around shapes (avoiding visual overlap with elements) but can pass through the empty margin of bounding boxes. All connectors use curved lines — no sharp corners.

6. **No sharp edges anywhere.** Every rectangle has rounded corners. Every connector has curved routing. This is a hard rule, not a style preference.

### How an LLM uses PlotCraft

The intended workflow when you (an LLM) want to create a diagram:

1. **Declare elements** — list all the text content that needs to appear in the diagram.
2. **Classify elements** — assign each one a semantic type (title, subtitle, caption, text).
3. **Define connections** — state which elements connect to which, and in what direction.
4. **Choose shapes** — pick a shape type for each element (rect, square, circle, oval).
5. **Call PlotCraft** — the engine handles text measurement, shape sizing, grid placement, connector routing, and SVG rendering.

You should not need to specify coordinates, dimensions, font sizes, or path data. The API should make it nearly impossible to produce a broken diagram.

### How to plan the build

**Decompose until you hit atoms, then build upward.**

Do not start by thinking about the full system. Start by asking: what is the smallest, most fundamental piece that everything else depends on? Build that first. Then ask: what's the next smallest piece that depends only on things I've already built? Build that. Repeat.

Concretely:

- Before you can render a diagram, you need to render shapes.
- Before you can render shapes, you need to know how big they are.
- Before you can know how big they are, you need to know how much space the text inside them takes up.
- Before you can measure text, you need a text measurement system that works without a browser or GUI — pure Python, estimating glyph widths for SVG rendering.

That's your starting atom: **text measurement.**

Apply this same recursive decomposition to every part of the system:

- **Grid and bounding boxes** — before you can snap shapes to a grid, you need a grid. Before you need a grid, you need to define what a cell is. Before cells, you need to decide grid units and spacing.
- **Connectors** — before you can route a connector, you need anchor points. Before anchor points, you need shapes with known positions. Before routing around shapes, you need to know where shapes are on the grid. Before curved routing, you need a path representation.
- **SVG rendering** — before you can emit SVG, you need a way to represent visual elements in memory. Before rendering a full diagram, you need to render a single shape. Before a shape, a single rounded rectangle.

Each phase of the plan should produce something **testable and runnable in isolation**. After building text measurement, you should be able to write a test that measures a string and gets back a width and height. After building shapes, you should be able to render a single rounded rectangle to SVG. After the grid, you should be able to place bounding boxes and verify none overlap.

### What to keep in mind as you plan

- **You are building this for yourself.** Think about what API would be easiest for an LLM to use correctly. Minimize the number of decisions the caller has to make. Make invalid states unrepresentable.
- **No external dependencies for rendering.** This is pure Python generating SVG strings. No Pillow, no Cairo, no browser. Text measurement will need to be approximate — and that's fine as long as shapes have generous padding.
- **Test from the bottom up.** Every atomic component gets unit tests before being composed into larger pieces.
- **The grid is the key insight.** It's what prevents the "ransom note" problem. Spend real time designing it well — cell sizing, margin rules, how shapes claim grid cells.

Start planning. Decompose the problem to its atoms. Build the plan from the ground up.
