# Diagram Planning Advisor Spec

Synthesized from:
1. **Patrick Winston's MIT communication principles** — how to structure arguments that stick
2. **Excalidraw diagram skill methodology** — argue don't display, isomorphism test, pattern matching
3. **PlotCraft's advisor module** — pattern catalog, shape semantics, validation

---

## A. Communication Principles for Diagrams

### A.1 The Promise (Winston #1)

Every diagram must make a **promise** within the first second. The title states what the viewer will learn — not just what the diagram "is about."

- Bad: "Deployment Architecture"
- Good: "How a commit becomes a production release"

Every diagram MUST have a `TextRole.TITLE` element that states the insight. The title drives every subsequent design decision.

### A.2 Eliminate Visual Crimes (Winston #2)

| Winston Slide Crime | Diagram Equivalent |
|---|---|
| Too much text | Labels crammed into shapes |
| Font too small | Unreadable at export size |
| Reading the slide aloud | Shape labels that restate the title |
| No white space | Shapes packed edge-to-edge |
| Weak final slide | No clear terminus — eye wanders off |

### A.3 Make It Unforgettable (Winston #3 — 5S Framework)

- **Symbol**: The diagram's silhouette IS the symbol. A cycle looks circular. A pipeline looks linear.
- **Slogan**: The title captures the core idea in under 8 words.
- **Surprise**: At least one element challenges expectations (feedback loop where people assume linearity, bottleneck where people assume parallelism).
- **Salient idea**: ONE core message. If you can't state it in one sentence, the diagram does too much.
- **Story**: The eye path tells a narrative — beginning, middle, end.

### A.4 Structure That Persuades (Winston #4)

- **Vision** (first 5 sec): Layout + title communicate the argument
- **Proof** (the body): Connections and details demonstrate it's sound
- **Contributions** (takeaway): The endpoint — what the viewer now understands

Opening and closing should mirror each other: "User Request" → ... → "User Satisfaction"

### A.5 Tangibility (Winston #5)

- Show concrete examples, not abstract labels
- Create tension → demonstration → resolution
- Guide attention with visual weight (size, color, density)

---

## B. Planning Process

### Step 0: Identify the Promise
1. What is this diagram about?
2. Who will look at it?
3. What ONE thing should they understand? (becomes the title)

### Step 1: Assess Depth
- **Conceptual**: Abstract shapes, minimal labels
- **Technical**: Concrete examples, real terminology

### Step 2: Understand Deeply
For each concept: What does it DO? What relationships exist? What's the core transformation? Where's the surprise?

### Step 3: Map to Visual Patterns

| Concept behavior | Pattern | Layout |
|---|---|---|
| Spawns multiple outputs | fan_out | Radial |
| Combines inputs | convergence | Radial inward |
| Hierarchy/nesting | hierarchy | Top-down tree |
| Sequence of steps | pipeline | Horizontal L→R |
| Loops/iterates | cycle | Circular |
| Temporal phases | timeline | Horizontal with dots |
| Compares alternatives | comparison | Side-by-side |
| Branches on conditions | decision_tree | Top-down diamonds |

Use `suggest_pattern()` to validate.

### Step 4: Select Shapes and Colors

| Concept | Shape | Color |
|---|---|---|
| Origin, trigger | OVAL/CIRCLE | START |
| Process, action | RECT | NEUTRAL |
| Decision | DIAMOND | DECISION |
| Terminal, output | OVAL/CIRCLE | END |
| Error path | RECT | ERROR |
| Annotation, label | NONE | — |
| Highlighted | any | HIGHLIGHT |

**Container discipline**: Default to NONE. Add containers only when arrows connect to it or shape carries meaning. Target <70% container usage.

### Step 5: Plan Eye Flow
Trace the path: Where does the eye land first → follow → end? This tells the story.

### Step 6: Isomorphism Test
Remove all text. Does the structure alone communicate the concept? If not, redesign.

### Step 7: Build and Validate
Run `validate_diagram()`. Address every warning.

---

## C. Pattern Catalog

(8 patterns with PlotCraft code examples — see full spec for details)

1. **Pipeline** — Sequential L→R flow
2. **Fan-out** — One source, many targets
3. **Convergence** — Many inputs, one output
4. **Cycle** — Feedback loop with return connector
5. **Decision tree** — Diamond branching
6. **Timeline** — Temporal milestones
7. **Hierarchy** — Tree structure
8. **Comparison** — Side-by-side parallel

---

## D. Anti-Patterns

1. **Label Grid** — Equal boxes in a grid. Fails isomorphism test.
2. **Everything in a Box** — All text containerized. Containers lose meaning.
3. **Monochrome** — All NEUTRAL. Wastes the color channel.
4. **Disconnected Islands** — Shapes with no connectors.
5. **One-Exit Diamond** — Decision with one outcome = not a decision.
6. **Missing Promise** — No title, or title that names topic not insight.
7. **No Narrative Flow** — Eye bounces randomly. No reading order.
8. **Surprise Deficit** — Only confirms expectations. Teaches nothing new.

---

## E. Quality Criteria

### Communication (Winston)
1. Has a promise (TITLE states what viewer learns)
2. Tells a story (clear start→middle→end)
3. Contains a surprise (non-obvious element)
4. Opening mirrors closing (complete arc)
5. One salient idea (statable in one sentence)
6. No visual crimes (readable, breathing room)

### Structural (Excalidraw)
7. Passes isomorphism test
8. Argues, does not display
9. Pattern variety across sections
10. Shape carries meaning
11. Color encodes information
12. Container discipline (<70%)

### Technical (PlotCraft)
13. `validate_diagram()` passes
14. All non-label shapes connected
15. Diamonds have 2+ exits
16. Visual hierarchy exists (TITLE/SUBTITLE)
17. Semantic color used
18. Renders without error

### The Final Gut Check
**One-week test**: Could someone recall the core argument a week later?
