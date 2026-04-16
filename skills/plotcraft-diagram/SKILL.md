# PlotCraft Diagram Skill

Create polished, argument-driven diagrams using PlotCraft's Scene API with D2 rendering.

**Use when:** The user asks you to create a diagram, flowchart, architecture diagram, visualization, visual essay, or any visual explanation of a concept.

## IMPORTANT: Read Design Rules First

Before creating ANY diagram, read `docs/DESIGN_RULES.md` in the PlotCraft repo. It contains spacing rules, arrow rules, text placement rules, and a pre-flight checklist that prevent the most common layout mistakes.

## Prerequisites

PlotCraft must be installed:
```bash
cd /Users/ashwinchidambaram/dev/projects/plotcraft && uv sync
```

D2 must be installed (provides layout + sketch-mode rendering):
```bash
brew install d2  # or see https://d2lang.com/
d2 version       # verify: should show 0.7.x+
```

## Core Philosophy

**Diagrams ARGUE, they don't DISPLAY.** A diagram is a visual argument that shows relationships, causality, and flow that words alone cannot express. Every shape, color, and connection must carry meaning.

**The Isomorphism Test:** If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test:** Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches.

**The One-Week Test:** Could someone recall the core argument a week later? If not, sharpen the promise.

---

## Output Format

PlotCraft uses **D2** as the primary rendering engine. D2 provides:
- Hand-drawn sketch aesthetic (built-in `--sketch` mode)
- Intelligent auto-layout via dagre (text centering, arrow routing, spacing)
- SVG and PNG output
- Semantic colors from PlotCraft's Terracotta/Sage/Gold palette

Excalidraw JSON (`.excalidraw`) remains available as an alternative format.

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

### Step 4: Select Roles and Emphasis

With the Scene API, you describe elements semantically — roles and emphasis control the visual output:

| Concept | Role | Emphasis | Visual result |
|---|---|---|---|
| Origin, trigger, input | `"start"` | normal | Oval, warm terracotta |
| Process, action, step | `"process"` | normal | Rectangle, neutral |
| Key step (highlighted) | `"process"` | `"high"` | Rectangle, bold terracotta, shadow |
| Decision, condition | `"decision"` | normal | Diamond, gold |
| Terminal, output | `"end"` | normal | Oval, sage green |
| Background/faded | `"process"` | `"low"` | Rectangle, faded opacity |

**Size** controls visual hierarchy: `"small"`, `"medium"` (default), `"large"`, `"hero"`.

**Theme:** `Scene(dark=True)` for dark canvas with light text. Good for technical/dramatic topics.

### Step 5: Plan the Eye Flow

Trace the intended reading path: Where does the eye land first -> follow -> end?
- Start at top-left (Western reading order)
- Bold/emphasized elements attract first
- Arrows pull the eye along the narrative
- The endpoint completes the arc started by the title

### Step 6: Write the Code

The Scene API is simple — describe elements, connect them, pick a layout, save:

```python
from plotcraft import Scene

s = Scene()  # or Scene(dark=True) for dark theme

# Title and caption frame the narrative
s.add("How AI agents reason and act", role="title")

# Flow elements — roles control shape/color, emphasis controls visual weight
s.add("User Query", role="start")
s.add("Observe", role="process", size="large", emphasis="high")
s.add("Think", role="decision")
s.add("Act", role="process", size="large")
s.add("Answer", role="end")

# Connections — D2 handles all routing automatically
s.connect("User Query", "Observe")
s.connect("Observe", "Think")
s.connect("Think", "Act", label="execute")
s.connect("Act", "Observe", label="feedback", style="dashed")
s.connect("Think", "Answer", label="done")

# Annotations float near their targets
s.annotate("Gather context", near="Observe")
s.annotate("Choose next action", near="Think")

s.add("Repeat until goal is reached", role="caption")

# Layout pattern — D2's dagre engine handles positioning
s.layout("cycle")

# Save — D2 renders with sketch mode (hand-drawn aesthetic)
s.save("output.svg")
```

**Key points:**
- No row/col coordinates — D2 computes the layout
- No anchor selection — D2 routes arrows intelligently
- `emphasis="high"` makes elements visually dominant
- `s.annotate()` places context near elements
- `s.layout()` picks the flow direction (pipeline=right, cycle/top_down/fan_out/decision_tree=down)

### LLM Pitfall Prevention

**1. Complexity budget:** Keep it focused.
- **Simple** (<=6 shapes): one pattern
- **Medium** (7-10 shapes): one or two patterns
- **Too many** (>12 shapes): split into multiple diagrams

**2. Keep connector count reasonable.** N shapes should have N-1 to N+2 connectors. More = visual clutter.

**3. Short text in shapes.** D2 auto-sizes shapes to fit text, but long text makes shapes awkwardly large. Keep shape labels to 1-3 words. Use annotations for details.

### Step 7: Render and View

D2 renders directly to SVG when you call `s.save("output.svg")`. Open the SVG to verify:

```python
s.save("examples/renders/my_diagram.svg")  # D2 renders with sketch mode
```

### Step 8: Validate

View the SVG and check:

- [ ] Title states the insight, not just the topic
- [ ] Clear narrative flow (start -> middle -> end)
- [ ] Shapes encode meaning (ovals=terminals, diamonds=decisions)
- [ ] Emphasis draws the eye to the key element
- [ ] Annotations add context without cluttering
- [ ] Arrows route cleanly (D2 handles this automatically)

### Step 9: Fix and Re-render

If issues remain, adjust the Scene code:
- Change `emphasis="high"` to highlight key elements
- Add `s.annotate()` for context
- Switch `size="large"` for visual hierarchy
- Change `layout()` pattern if flow direction is wrong

---

## Anti-Patterns to AVOID

| Anti-Pattern | What It Looks Like | Fix |
|---|---|---|
| **Label Grid** | Equal boxes in rows | Use emphasis + size to create hierarchy |
| **Monochrome** | All default process roles | Use semantic roles (start, end, decision) |
| **Disconnected Islands** | Shapes with no connections | Connect or remove |
| **Missing Promise** | No title or generic title | Title states the insight |
| **No Narrative** | Eye bounces randomly | Pick the right layout pattern |
| **Too Busy** | >12 shapes crammed together | Split into multiple diagrams |
| **Long text in shapes** | Shapes balloon to fit text | Keep labels short, use annotations |

---

## Winston's 5S Checklist (Final Quality Gate)

1. **Symbol** -- The silhouette communicates the concept
2. **Slogan** -- Title captures the core idea in <=8 words
3. **Surprise** -- One element reveals something non-obvious
4. **Salient idea** -- Entire diagram serves ONE message
5. **Story** -- Eye follows a clear narrative arc

---

## Quick Reference: Scene API

```python
from plotcraft import Scene

# Create scene
s = Scene()                  # light theme
s = Scene(dark=True)         # dark theme

# Add elements (all return self for chaining)
s.add(text, role="process", size="medium", emphasis="normal")
# Roles: title, subtitle, start, end, process, decision, caption
# Sizes: small, medium, large, hero
# Emphasis: low, normal, high

# Connect elements (by text or ID)
s.connect(source, target, label=None, style="solid", weight="normal")
# Styles: solid, dashed, dotted
# Weights: thin, normal, bold

# Annotate (floats near target)
s.annotate(text, near=target_text_or_id)

# Layout
s.layout("pipeline")       # horizontal L->R
s.layout("top_down")       # vertical T->B
s.layout("fan_out")        # one source, many targets
s.layout("convergence")    # many sources, one target
s.layout("cycle")          # circular loop
s.layout("decision_tree")  # branching from root

# Save (D2 is default for SVG/PNG)
s.save("diagram.svg")           # D2 sketch-mode SVG
s.save("diagram.svg", engine="d2")  # explicit D2
s.save("diagram.excalidraw")    # Excalidraw JSON (alternative)
s.save("diagram.d2")            # D2 source markup
```
