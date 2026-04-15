# PlotCraft Diagram Skill

Create polished, argument-driven diagrams using PlotCraft's Python API with Excalidraw rendering.

**Use when:** The user asks you to create a diagram, flowchart, architecture diagram, visualization, visual essay, or any visual explanation of a concept.

## Prerequisites

PlotCraft must be installed:
```bash
cd /Users/ashwinchidambaram/dev/projects/plotcraft && uv sync
```

For visual verification (render to PNG), install the render pipeline:
```bash
cd /Users/ashwinchidambaram/dev/projects/plotcraft/skills/plotcraft-diagram/references
uv sync && uv run playwright install chromium
```

## Core Philosophy

**Diagrams ARGUE, they don't DISPLAY.** A diagram is a visual argument that shows relationships, causality, and flow that words alone cannot express. Every shape, color, and connection must carry meaning.

**The Isomorphism Test:** If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test:** Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches.

**The One-Week Test:** Could someone recall the core argument a week later? If not, sharpen the promise.

---

## Output Format

PlotCraft generates **Excalidraw JSON** (`.excalidraw`) as the primary output. This gives you:
- Hand-drawn aesthetic via roughness=1 (built-in, no extra config)
- Beautiful Terracotta/Sage/Gold color palette on a warm Sand canvas
- Native arrow routing via Excalidraw's binding system
- PNG verification via Playwright

Draw.io (`.drawio`) and SVG (`.svg`) remain available as fallback formats.

---

## The Process

Follow these steps IN ORDER (Steps 0-9). Do not skip steps.

### Step 0: Identify the Promise

Before touching any code, answer:
1. What is this diagram about?
2. Who will look at it?
3. **What ONE thing should they understand?** <- This becomes the title.

The title states the INSIGHT, not the topic:
- Bad: "Deployment Architecture"
- Good: "How a commit becomes a production release"
- Bad: "ReAct Loop"
- Good: "How AI agents reason and act iteratively"

### Step 1: Assess Depth and Scope

**Depth:**
- **Conceptual**: Mental models, overviews -> abstract shapes, minimal labels
- **Technical**: Real systems, architectures -> concrete examples, real terminology

**Scope:**
- **Single diagram** (<=15 shapes): one pattern, standard workflow
- **Visual essay** (multiple sections): plan each section separately, use callouts and decoratives

### Step 2: Understand the Concept

For each element: What does it DO? What relationships exist? What's the core transformation? **Where's the surprise?** (The non-obvious element that makes the diagram worth creating.)

### Step 3: Choose the Visual Pattern

Match the concept to a pattern. Read `references/patterns.md` for the full catalog with code examples.

| If the concept... | Use pattern | Layout |
|---|---|---|
| Has sequential steps | **pipeline** | Horizontal L->R |
| Spawns multiple outputs | **fan_out** | Radial from center |
| Combines inputs into one | **convergence** | Funnel inward |
| Loops or iterates | **cycle** | Circular/triangular |
| Branches on conditions | **decision_tree** | Top-down |
| Has temporal phases | **timeline** | Horizontal dots |
| Has parent-child structure | **hierarchy** | Top-down tree |
| Compares alternatives | **comparison** | Side-by-side |
| Explains with annotations | **annotated_flow** | Flow + callouts |
| Multi-section essay | **visual_essay** | Sections with mixed patterns |

### Step 4: Select Shapes, Colors, and Theme

Every choice must encode meaning:

| Concept | Shape | Color | Why |
|---|---|---|---|
| Origin, trigger, input | `ShapeKind.OVAL` | `ColorTheme.START` | Soft, origin-like |
| Process, action, step | `ShapeKind.RECT` | `ColorTheme.NEUTRAL` | Contained action |
| Decision, condition | `ShapeKind.DIAMOND` | `ColorTheme.DECISION` | Classic branch symbol |
| Terminal, output, result | `ShapeKind.OVAL` | `ColorTheme.END` | Completion |
| Error, failure path | `ShapeKind.RECT` | `ColorTheme.ERROR` | Danger signal |
| Label, annotation | `ShapeKind.NONE` | -- | Free-floating text |
| Important, highlighted | any | `ColorTheme.HIGHLIGHT` | Draws attention |
| Informational | `ShapeKind.RECT` | `ColorTheme.INFO` | Calm, factual |

**Container discipline:** Default to `ShapeKind.NONE` for labels and descriptions. Only use container shapes when arrows connect to it or the shape carries meaning.

**Theme:** Use `ThemeMode.LIGHT` (default, warm Sand canvas) or `ThemeMode.DARK` (dark canvas with light text). Dark works well for technical/dramatic topics.

### Step 5: Plan the Eye Flow

Trace the intended reading path: Where does the eye land first -> follow -> end?
- Start at top-left (Western reading order)
- Bold/colored elements attract first
- Arrows pull the eye along the narrative
- The endpoint completes the arc started by the title

### Step 6: Write the Code in Passes

**Build the diagram in 3 passes to prevent drift.** Writing the entire diagram in one block causes the LLM to lose track of positions and relationships, resulting in overlaps and wrong connections.

#### Pass A: Layout Table (plan before coding)

First, write out a position table as a comment. This is your source of truth:

```python
# LAYOUT TABLE:
# row=0: title (col=1)
# row=1: query (col=0), observe (col=2)
# row=3: act (col=0), think (col=2), answer (col=4)
```

Keep this table SHORT -- 1 line per element. If you have >12 elements, split into sections and plan each section's grid region separately.

#### Pass B: Shapes Only (no connectors)

Add all shapes. Verify the layout table matches. Do NOT add connectors yet.

```python
from plotcraft import (
    Diagram, TextRole, ShapeKind, AnchorName, ArrowDirection,
    ConnectorStyle, LineWeight, ColorTheme, GridConfig, SectionStyle,
    ThemeMode, DecorativeKind, CalloutPosition,
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

#### Pass C: Connectors, Callouts, Sections, and Save

Now add connectors, annotations, and save. For each connector, check the layout table to confirm direction before choosing anchors.

```python
# query(row=1,col=0) -> observe(row=1,col=2): target is RIGHT
d.connect("query", "observe")

# observe(row=1,col=2) -> think(row=3,col=2): target is BELOW
d.connect("observe", "think",
          source_anchor=AnchorName.BOTTOM_CENTER,
          target_anchor=AnchorName.TOP_CENTER,
          line_weight=LineWeight.BOLD)

# think(row=3,col=2) -> act(row=3,col=0): target is LEFT
d.connect("think", "act",
          source_anchor=AnchorName.LEFT_CENTER,
          target_anchor=AnchorName.RIGHT_CENTER,
          line_weight=LineWeight.BOLD)

# act(row=3,col=0) -> observe(row=1,col=2): feedback loop
d.connect("act", "observe",
          source_anchor=AnchorName.TOP_CENTER,
          target_anchor=AnchorName.BOTTOM_CENTER,
          label="loop", line_weight=LineWeight.BOLD)

# think(row=3,col=2) -> answer(row=3,col=4): exit
d.connect("think", "answer", label="done", style=ConnectorStyle.DASHED)

# Add a callout annotation
d.callout("note1", "Repeats until done", target_id="act", position=CalloutPosition.BELOW)

# Section groups the loop
d.section("Iterative Loop", ["observe", "think", "act"],
          style=SectionStyle(fill="#ede9e0", stroke="#b0a898", stroke_width=1.5,
                             corner_radius=16, label_font_size=18, label_color="#7a7060", padding=40))

# Save as Excalidraw (primary)
d.save("output.excalidraw")
```

**Why passes matter:** Each pass is small enough to hold in context. The layout table prevents drift. Connectors reference the table to get directions right.

### LLM Pitfall Prevention

These are the ways diagram generation goes wrong. Read before coding.

**1. Complexity budget:** Count your elements.
- **Simple** (<=6 shapes): one pattern, no sections needed
- **Medium** (7-10 shapes): one or two patterns, 1-2 sections
- **Complex** (11-15 shapes): multiple patterns, sections required
- **Too many** (>15 shapes): split into multiple diagrams or use visual essay approach

**2. Diamond/oval span awareness:** Diamonds and ovals are WIDER than rectangles. At `cell_width=260`:
- `ShapeKind.RECT` with short text = 1 column
- `ShapeKind.DIAMOND` = often 1 column but taller (2 rows)
- `ShapeKind.OVAL` with long text = may span 2 columns
- **Leave at least 1 empty column** between a diamond/oval and its neighbor

**3. Row skipping for vertical space:** When shapes in different rows need connectors between them, skip a row. Shapes at row=1 and row=2 are too close -- use row=1 and row=3.

**4. Don't copy pattern examples literally.** The row/col values in `references/patterns.md` are examples. Calculate YOUR layout based on YOUR shapes and their sizes.

**5. Keep connector count reasonable.** If you have N shapes, aim for N-1 to N+2 connectors. More than 2x shapes = too many.

### Step 7: Render to PNG

Render the Excalidraw output to PNG for visual verification:

```bash
cd /Users/ashwinchidambaram/dev/projects/plotcraft/skills/plotcraft-diagram/references && uv run python render_excalidraw.py /path/to/output.excalidraw
```

This outputs a PNG next to the `.excalidraw` file.

### Step 8: View and Validate

Use the Read tool to view the exported PNG. Run TWO review passes:

#### Pass 1: Absolute Nos (BLOCKING -- must fix before anything else)

These are hard failures. If ANY are true, stop and fix immediately.

- [ ] **No overlapping shapes** -- every shape must have clear space around it
- [ ] **No text overflow** -- all text must fit inside its shape container
- [ ] **No clipped elements** -- nothing cut off at the edges
- [ ] **No unreadable text** -- all labels must be legible
- [ ] **No orphaned arrows** -- every connector must visually connect to both endpoints
- [ ] **No arrows through shapes** -- connectors must route around shapes

If any Absolute No is violated: fix the layout and re-render.

#### Pass 2: Quality Checks (improve, don't block)

**Communication:**
- [ ] Title states the insight, not just the topic
- [ ] Clear start -> middle -> end narrative
- [ ] At least one surprise element
- [ ] Opening mirrors closing (complete arc)

**Structural:**
- [ ] Passes isomorphism test (structure communicates without text)
- [ ] Shape types encode meaning (diamonds=decisions, ovals=terminals)
- [ ] Colors encode meaning (semantic color use)
- [ ] Not everything is in a box (container discipline)

**Technical:**
- [ ] Arrows route cleanly
- [ ] No disconnected shapes
- [ ] Spacing feels balanced

### Step 9: Fix and Re-render

If any check fails, edit the Python code and re-render. Common fixes:
- Adjust `GridConfig(cell_width=..., cell_height=...)` for spacing
- Move elements by changing `row`/`col` values
- Add callouts for context that doesn't fit in the main flow
- Use sections for visual grouping

---

## Visual Essay Workflow

For multi-section compositions that go beyond single flowcharts:

1. **Plan sections first:** Each section gets its own grid region and pattern
2. **Use callouts** (`d.callout()`) for annotations that support the argument
3. **Use notes** (`d.note()`) for free-floating commentary
4. **Use decoratives** (`d.decorate()`) for numbered circles and badges
5. **Consider dark theme** (`ThemeMode.DARK`) for dramatic effect
6. **Budget:** Max 5-6 sections, max 40 total shapes across all sections

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
| **No Narrative** | Eye bounces randomly | Establish L->R or T->B flow |
| **Too Busy** | >15 shapes crammed together | Split into sections or multiple diagrams |

---

## Winston's 5S Checklist (Final Quality Gate)

Before delivering, verify your diagram has:

1. **Symbol** -- The silhouette communicates the concept (cycle looks circular, pipeline looks linear)
2. **Slogan** -- Title captures the core idea in <=8 words
3. **Surprise** -- One element reveals something non-obvious
4. **Salient idea** -- Entire diagram serves ONE message
5. **Story** -- Eye follows a clear narrative arc

---

## Quick Reference: PlotCraft API

```python
# Imports
from plotcraft import (
    Diagram, TextRole, ShapeKind, TextAlign, AnchorName,
    ArrowDirection, ConnectorStyle, LineWeight, ColorTheme,
    GridConfig, SectionStyle, TimelineEntry, TimelineOrientation, TreeNode,
    ThemeMode, DecorativeKind, CalloutPosition,
)

# Create diagram (Excalidraw output)
d = Diagram(grid_config=GridConfig(cell_width=260, cell_height=160, margin=30))

# Dark theme
d = Diagram(theme=ThemeMode.DARK)

# Add shapes (all return self for chaining)
d.add(id, text, role=TextRole.BODY, shape=ShapeKind.RECT,
      align=TextAlign.CENTER, row=N, col=N, color=ColorTheme.NEUTRAL)

# Connect shapes
d.connect(source_id, target_id,
          source_anchor=AnchorName.RIGHT_CENTER,
          target_anchor=AnchorName.LEFT_CENTER,
          label=None, direction=ArrowDirection.FORWARD,
          style=ConnectorStyle.SOLID, line_weight=LineWeight.NORMAL)

# Callout (annotation near a target shape)
d.callout(id, text, target_id, position=CalloutPosition.RIGHT,
          color=ColorTheme.WARNING)

# Note (free-floating text)
d.note(id, text, row=N, col=N, color=ColorTheme.INFO)

# Decorative elements
d.decorate(id, DecorativeKind.NUMBERED_CIRCLE, text="1", row=N, col=N)
d.decorate(id, DecorativeKind.BADGE, text="NEW", row=N, col=N)

# Group into sections
d.section(label, [shape_ids], style=SectionStyle(...))

# Timelines
d.timeline([TimelineEntry("Q1", "Design"), TimelineEntry("Q2", "Build")],
           orientation=TimelineOrientation.HORIZONTAL, start_row=0, start_col=0)

# Trees
d.tree(TreeNode("Root", children=(TreeNode("Child1"), TreeNode("Child2"))),
       start_row=0, start_col=0)

# Save (format detected from extension)
d.save("diagram.excalidraw")  # Excalidraw JSON (primary)
d.save("diagram.drawio")      # draw.io XML
d.save("diagram.svg")         # SVG (PlotCraft renderer)
d.save("diagram.png")         # PNG (needs cairosvg)
```

### Anchor Points
```
TOP_LEFT      TOP_CENTER     TOP_RIGHT
LEFT_CENTER   CENTER         RIGHT_CENTER
BOTTOM_LEFT   BOTTOM_CENTER  BOTTOM_RIGHT
```

### CRITICAL: Anchor Selection by Direction

**Anchors must match the RELATIVE POSITION of source and target.** The arrow exits the source toward the target and enters the target from the source's direction.

| Target is... | Source anchor | Target anchor |
|---|---|---|
| **Right** of source | `RIGHT_CENTER` | `LEFT_CENTER` |
| **Left** of source | `LEFT_CENTER` | `RIGHT_CENTER` |
| **Below** source | `BOTTOM_CENTER` | `TOP_CENTER` |
| **Above** source | `TOP_CENTER` | `BOTTOM_CENTER` |

**The rule:** The arrow EXITS the source on the side FACING the target, and ENTERS the target on the side FACING the source.

### Connector Styles
- `ConnectorStyle.SOLID` -- primary flow
- `ConnectorStyle.DASHED` -- secondary/optional path
- `ConnectorStyle.DOTTED` -- weak/rare connection (also used by callouts)

### Line Weights
- `LineWeight.THIN` (1px) -- subtle connections
- `LineWeight.NORMAL` (2px) -- standard
- `LineWeight.BOLD` (3px) -- primary flow emphasis

### Color Themes (Excalidraw Palette)

**Light theme (default, canvas: #F9F7F4):**
| Theme | Fill | Stroke | Use |
|---|---|---|---|
| `START` | Terracotta 50 | Terracotta 600 | Origins |
| `END` | Sage 100 | Sage 700 | Terminals |
| `DECISION` | Gold 50 | Gold 800 | Branch points |
| `ERROR` | Error Light | Error Dark | Failure paths |
| `HIGHLIGHT` | Terracotta 400 | Terracotta 700 | Emphasis |
| `INFO` | Info Light | Info Dark | Informational |
| `SUCCESS` | Sage 100 | Sage 700 | Positive outcomes |
| `WARNING` | Gold 100 | Gold 700 | Caution |
| `NEUTRAL` | Sand 200 | Gray 600 | Default |

### Render Pipeline

```bash
# Render .excalidraw to PNG
cd /path/to/skills/plotcraft-diagram/references
uv run python render_excalidraw.py /path/to/diagram.excalidraw

# Output: /path/to/diagram.png (next to the .excalidraw file)
```
