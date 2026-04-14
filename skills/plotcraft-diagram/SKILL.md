# PlotCraft Diagram Skill

Create polished, argument-driven diagrams using PlotCraft's Python API with draw.io rendering.

**Use when:** The user asks you to create a diagram, flowchart, architecture diagram, visualization, or any visual explanation of a concept.

## Prerequisites

PlotCraft must be installed:
```bash
cd /Users/ashwinchidambaram/dev/projects/plotcraft && uv sync
```

Draw.io desktop app must be installed for high-quality rendering:
- macOS: `brew install --cask drawio` or download from https://www.drawio.com/
- Verify: `/Applications/draw.io.app/Contents/MacOS/draw.io --version`

## Core Philosophy

**Diagrams ARGUE, they don't DISPLAY.** A diagram is a visual argument that shows relationships, causality, and flow that words alone cannot express. Every shape, color, and connection must carry meaning.

**The Isomorphism Test:** If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The One-Week Test:** Could someone recall the core argument a week later? If not, sharpen the promise.

---

## The Process

Follow these steps IN ORDER (Steps 0–9). Do not skip steps.

### Step 0: Identify the Promise

Before touching any code, answer:
1. What is this diagram about?
2. Who will look at it?
3. **What ONE thing should they understand?** ← This becomes the title.

The title states the INSIGHT, not the topic:
- Bad: "Deployment Architecture"
- Good: "How a commit becomes a production release"
- Bad: "ReAct Loop"  
- Good: "How AI agents reason and act iteratively"

### Step 1: Assess Depth

- **Conceptual**: Mental models, overviews → abstract shapes, minimal labels
- **Technical**: Real systems, architectures → concrete examples, real terminology

### Step 2: Understand the Concept

For each element: What does it DO? What relationships exist? What's the core transformation? **Where's the surprise?** (The non-obvious element that makes the diagram worth creating.)

### Step 3: Choose the Visual Pattern

Match the concept to a pattern. Read `references/patterns.md` for the full catalog with code examples.

| If the concept... | Use pattern | Layout |
|---|---|---|
| Has sequential steps | **pipeline** | Horizontal L→R |
| Spawns multiple outputs | **fan_out** | Radial from center |
| Combines inputs into one | **convergence** | Funnel inward |
| Loops or iterates | **cycle** | Circular/triangular |
| Branches on conditions | **decision_tree** | Top-down |
| Has temporal phases | **timeline** | Horizontal dots |
| Has parent-child structure | **hierarchy** | Top-down tree |
| Compares alternatives | **comparison** | Side-by-side |

### Step 4: Select Shapes and Colors

Every choice must encode meaning:

| Concept | Shape | Color | Why |
|---|---|---|---|
| Origin, trigger, input | `ShapeKind.OVAL` | `ColorTheme.START` | Soft, origin-like |
| Process, action, step | `ShapeKind.RECT` | `ColorTheme.NEUTRAL` | Contained action |
| Decision, condition | `ShapeKind.DIAMOND` | `ColorTheme.DECISION` | Classic branch symbol |
| Terminal, output, result | `ShapeKind.OVAL` | `ColorTheme.END` | Completion |
| Error, failure path | `ShapeKind.RECT` | `ColorTheme.ERROR` | Danger signal |
| Label, annotation | `ShapeKind.NONE` | — | Free-floating text |
| Important, highlighted | any | `ColorTheme.HIGHLIGHT` | Draws attention |
| Informational | `ShapeKind.RECT` | `ColorTheme.INFO` | Calm, factual |

**Container discipline:** Default to `ShapeKind.NONE` for labels and descriptions. Only use container shapes when arrows connect to it or the shape carries meaning.

**Section discipline:** Only group shapes that occupy contiguous grid positions into a section. If shapes are spread across non-adjacent rows/columns, the section bounding box will be oversized and visually confusing. Split into multiple sections instead.

### Step 5: Plan the Eye Flow

Trace the intended reading path: Where does the eye land first → follow → end?
- Start at top-left (Western reading order)
- Bold/colored elements attract first
- Arrows pull the eye along the narrative
- The endpoint completes the arc started by the title

### Step 6: Write the Code in Passes

**Build the diagram in 3 passes to prevent drift.** Writing the entire diagram in one block causes the LLM to lose track of positions and relationships, resulting in overlaps and wrong connections. Break it up:

#### Pass A: Layout Table (plan before coding)

First, write out a position table as a comment. This is your source of truth:

```python
# LAYOUT TABLE:
# row=0: title (col=1)
# row=1: query (col=0), observe (col=2)
# row=3: act (col=0), think (col=2), answer (col=4)
```

Keep this table SHORT — 1 line per element. If you have >12 elements, split into sections and plan each section's grid region separately.

#### Pass B: Shapes Only (no connectors)

Add all shapes. Verify the layout table matches. Do NOT add connectors yet.

```python
from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName, ArrowDirection,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig, SectionStyle,
)

d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Title
d.add("title", "How AI agents reason and act",
      role=TextRole.TITLE, shape=ShapeKind.NONE, row=0, col=1)

# Row 1: entry and observe
d.add("query", "User Query", shape=ShapeKind.OVAL, color=ColorTheme.START, row=1, col=0)
d.add("observe", "Observe", shape=ShapeKind.RECT, color=ColorTheme.INFO, row=1, col=2)

# Row 3: act, think, answer
d.add("act", "Act", shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=3, col=0)
d.add("think", "Think", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=3, col=2)
d.add("answer", "Answer", shape=ShapeKind.OVAL, color=ColorTheme.END, row=3, col=4)
```

#### Pass C: Connectors (referencing the layout table)

Now add connectors. For each one, check the layout table to confirm direction before choosing anchors. The draw.io renderer auto-corrects bad anchors, but getting them right produces cleaner paths.

```python
# query(row=1,col=0) → observe(row=1,col=2): target is RIGHT
d.connect("query", "observe")

# observe(row=1,col=2) → think(row=3,col=2): target is BELOW
d.connect("observe", "think",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# think(row=3,col=2) → act(row=3,col=0): target is LEFT
d.connect("think", "act",
          source_anchor=AnchorName.LEFT_CENTER,
          target_anchor=AnchorName.RIGHT_CENTER,
          line_weight=LineWeight.BOLD)

# act(row=3,col=0) → observe(row=1,col=2): target is ABOVE-RIGHT
d.connect("act", "observe",
          source_anchor=AnchorName.TOP_CENTER,
          target_anchor=AnchorName.BOTTOM_CENTER,
          label="loop", line_weight=LineWeight.BOLD)

# think(row=3,col=2) → answer(row=3,col=4): target is RIGHT
d.connect("think", "answer", label="done", style=ConnectorStyle.DASHED)
```

#### Pass D: Sections and Save

```python
d.section("Iterative Loop", ["observe", "think", "act"],
          style=SectionStyle(fill="#ede9e0", stroke="#b0a898", ...))

d.save("output.drawio")
```

**Why passes matter:** Each pass is small enough to hold in context. The layout table prevents drift. Connectors reference the table to get directions right. This consistently produces better diagrams than one giant code block.

### LLM Pitfall Prevention

These are the ways diagram generation goes wrong. Read before coding.

**1. Complexity budget:** Count your elements. For draw.io output:
- **Simple** (≤6 shapes): one pattern, no sections needed
- **Medium** (7-10 shapes): one or two patterns, 1-2 sections
- **Complex** (11-15 shapes): multiple patterns, sections required
- **Too many** (>15 shapes): split into multiple diagrams. A single diagram with >15 shapes almost always has overlaps and routing problems.

**2. Diamond/oval span awareness:** Diamonds and ovals are WIDER than rectangles. At `cell_width=260`:
- `ShapeKind.RECT` with short text = 1 column
- `ShapeKind.DIAMOND` = often 1 column but taller (2 rows)
- `ShapeKind.OVAL` with long text = may span 2 columns
- **Leave at least 1 empty column** between a diamond/oval and its neighbor

**3. Row skipping for vertical space:** When shapes in different rows need connectors between them, skip a row. Shapes at row=1 and row=2 are too close — use row=1 and row=3. The empty row=2 gives the router space.

**4. Don't copy pattern examples literally.** The row/col values in `references/patterns.md` are examples. Calculate YOUR layout based on YOUR shapes and their sizes. Always write the layout table first.

**5. Keep connector count reasonable.** Each connector adds routing complexity. If you have N shapes, aim for N-1 to N+2 connectors. More than 2x shapes = too many connectors, the diagram will be a mess.

### Step 7: Render via Draw.io

Export to PNG using the draw.io CLI:

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --scale 2 --border 20 --output output.png output.drawio
```

Or for SVG:
```bash
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format svg --border 20 --output output.svg output.drawio
```

### Step 8: View and Validate

Use the Read tool to view the exported PNG. Run TWO review passes:

#### Pass 1: Absolute Nos (BLOCKING — must fix before anything else)

These are hard failures. If ANY are true, stop and fix immediately before evaluating anything else.

- [ ] **No arrows through shapes** — every connector must route AROUND shapes, never through them
- [ ] **No overlapping shapes** — every shape must have clear space around it, no visual collision
- [ ] **No text overflow** — all text must fit inside its shape container
- [ ] **No U-turn arrows** — arrows must not exit a shape, loop around, and re-enter from the same direction (the renderer auto-corrects most of these, but check visually)
- [ ] **No clipped elements** — nothing cut off at the edges of the export
- [ ] **No unreadable text** — all labels must be legible at the exported resolution
- [ ] **No orphaned arrows** — every connector must visually connect to both its source and target shape

If any Absolute No is violated: fix the layout (adjust row/col positions, increase cell_width/cell_height, or reduce element count) and re-export before proceeding to Pass 2.

#### Pass 2: Quality Checks (improve, don't block)

**Communication:**
- [ ] Title states the insight, not just the topic
- [ ] Clear start → middle → end narrative
- [ ] At least one surprise element
- [ ] Opening mirrors closing (complete arc)

**Structural:**
- [ ] Passes isomorphism test (structure communicates without text)
- [ ] Shape types encode meaning (diamonds=decisions, ovals=terminals)
- [ ] Colors encode meaning (green=start, red=end, yellow=decision)
- [ ] Not everything is in a box

**Technical:**
- [ ] Arrows route cleanly with natural paths
- [ ] No disconnected shapes
- [ ] Labels have breathing room from shapes
- [ ] Spacing feels balanced (not too cramped, not too sparse)

### Step 9: Fix and Re-render

If any check fails, edit the Python code and re-export. Common fixes:
- Adjust `GridConfig(cell_width=..., cell_height=...)` for spacing
- Move elements by changing `row`/`col` values
- Change anchor points to fix arrow routing
- Add `SectionStyle` for visual grouping

**Common pitfalls:**
- **PlacementError**: Shapes with long text (especially ovals/diamonds) may span 2+ grid columns. Fix: increase `cell_width` to 260+ or use shorter text.
- **Overlapping sections**: If a section's shapes span non-contiguous grid areas, the section box covers too much. Fix: only group adjacent shapes.
- **Visual gaps**: Skipping column numbers (e.g., col 4 to col 6) creates empty space. This is useful to separate phases but avoid unintentional gaps.

### Combining Multiple Patterns

Real diagrams often combine patterns (e.g., pipeline + decision + cycle). Strategy:
1. Lay out the **primary pattern** first (usually pipeline or fan-out) on the main row.
2. Add **decision branches** by placing the diamond in-line, then branching to rows above/below.
3. Add **feedback loops** by connecting failure paths back to earlier nodes, using `ConnectorStyle.DOTTED` for visual distinction.
4. Use **sections** to group phases (e.g., "CI Checks", "Deploy", "Client", "Backend").
5. Place **annotations** (`ShapeKind.NONE`) near the element they describe, on a row below.

---

## Anti-Patterns to AVOID

| Anti-Pattern | What It Looks Like | Fix |
|---|---|---|
| **Label Grid** | Equal boxes in a grid | Vary shapes, add hierarchy |
| **Everything in a Box** | All text containerized | Use `ShapeKind.NONE` for labels |
| **Monochrome** | All `ColorTheme.NEUTRAL` | Use semantic colors |
| **Disconnected Islands** | Shapes with no connectors | Connect or remove |
| **One-Exit Diamond** | Decision with 1 outcome | Add branch or use RECT |
| **Missing Promise** | No title or generic title | Title states the insight |
| **No Narrative** | Eye bounces randomly | Establish L→R or T→B flow |

---

## Winston's 5S Checklist (Final Quality Gate)

Before delivering, verify your diagram has:

1. **Symbol** — The silhouette communicates the concept (cycle looks circular, pipeline looks linear)
2. **Slogan** — Title captures the core idea in ≤8 words
3. **Surprise** — One element reveals something non-obvious
4. **Salient idea** — Entire diagram serves ONE message
5. **Story** — Eye follows a clear narrative arc

---

## Quick Reference: PlotCraft API

```python
# Imports
from plotcraft import (
    Diagram, TextRole, ShapeKind, TextAlign, AnchorName,
    ArrowDirection, ConnectorStyle, LineWeight, ColorTheme,
    GridConfig, SectionStyle, TimelineEntry, TimelineOrientation, TreeNode,
)

# Create diagram with wider cells for draw.io (260 prevents multi-column spans)
d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Add shapes (all return self for chaining)
d.add(id, text, role=TextRole.BODY, shape=ShapeKind.RECT,
      align=TextAlign.CENTER, row=N, col=N, color=ColorTheme.NEUTRAL)

# Connect shapes
d.connect(source_id, target_id,
          source_anchor=AnchorName.RIGHT_CENTER,
          target_anchor=AnchorName.LEFT_CENTER,
          label=None, direction=ArrowDirection.FORWARD,
          style=ConnectorStyle.SOLID, line_weight=LineWeight.NORMAL)

# Group into sections
d.section(label, [shape_ids], style=SectionStyle(...))

# Timelines
d.timeline([TimelineEntry("Q1", "Design"), TimelineEntry("Q2", "Build")],
           orientation=TimelineOrientation.HORIZONTAL, start_row=0, start_col=0)

# Trees
d.tree(TreeNode("Root", children=(TreeNode("Child1"), TreeNode("Child2"))),
       start_row=0, start_col=0)

# Save
d.save("diagram.drawio")    # draw.io XML
d.save("diagram.svg")       # SVG (PlotCraft renderer)
d.save("diagram.png")       # PNG (needs cairosvg)

# Open in draw.io app
d.open()
```

### Anchor Points
```
TOP_LEFT      TOP_CENTER     TOP_RIGHT
LEFT_CENTER   CENTER         RIGHT_CENTER
BOTTOM_LEFT   BOTTOM_CENTER  BOTTOM_RIGHT
```

For diamonds: prefer side midpoints (TOP/RIGHT/BOTTOM/LEFT_CENTER) which map to the diamond's actual vertices.

### CRITICAL: Anchor Selection by Direction

**Anchors must match the RELATIVE POSITION of source and target.** The arrow exits the source toward the target and enters the target from the source's direction. Getting this wrong causes arrows to U-turn and take bizarre routes.

| Target is... | Source anchor | Target anchor |
|---|---|---|
| **Right** of source | `RIGHT_CENTER` | `LEFT_CENTER` |
| **Left** of source | `LEFT_CENTER` | `RIGHT_CENTER` |
| **Below** source | `BOTTOM_CENTER` | `TOP_CENTER` |
| **Above** source | `TOP_CENTER` | `BOTTOM_CENTER` |
| **Below-right** | `BOTTOM_CENTER` or `RIGHT_CENTER` | `TOP_CENTER` or `LEFT_CENTER` |
| **Below-left** | `BOTTOM_CENTER` or `LEFT_CENTER` | `TOP_CENTER` or `RIGHT_CENTER` |

**The rule:** The arrow EXITS the source on the side FACING the target, and ENTERS the target on the side FACING the source.

**Common mistake:** Using the default `RIGHT_CENTER → LEFT_CENTER` for a connection that goes LEFT (target is left of source). This makes the arrow exit rightward, U-turn, and loop around — creating the bizarre routing you see.

**Example — connecting right-to-left (Act ← Think):**
```python
# Think is at col=2, Act is at col=0 (Act is LEFT of Think)
d.connect("think", "act",
          source_anchor=AnchorName.LEFT_CENTER,    # exit Think leftward
          target_anchor=AnchorName.RIGHT_CENTER)   # enter Act from right
```

**Example — connecting bottom-to-top (feedback loop):**
```python
# Act is at row=3, Observe is at row=1 (Observe is ABOVE Act)
d.connect("act", "observe",
          source_anchor=AnchorName.TOP_CENTER,     # exit Act upward
          target_anchor=AnchorName.BOTTOM_CENTER)  # enter Observe from below
```

### Connector Styles
- `ConnectorStyle.SOLID` — primary flow
- `ConnectorStyle.DASHED` — secondary/optional path
- `ConnectorStyle.DOTTED` — weak/rare connection

### Line Weights
- `LineWeight.THIN` (1px) — subtle connections
- `LineWeight.NORMAL` (2px) — standard
- `LineWeight.BOLD` (3px) — primary flow emphasis

### Color Themes
- `START` — green (origins)
- `END` — red/pink (terminals)
- `DECISION` — yellow (branch points)
- `ERROR` — salmon (failure paths)
- `HIGHLIGHT` — blue (emphasis)
- `INFO` — teal (informational)
- `SUCCESS` — green (positive outcomes)
- `WARNING` — orange (caution)
- `NEUTRAL` — gray (default)
