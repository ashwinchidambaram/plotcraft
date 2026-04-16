# PlotCraft for Small Language Models

This guide is optimized for small models (3B-13B). It uses **templates** that hide the complexity. You only need to pick a template and fill in the data.

## The Rule

**Always use a template.** Don't write Scene or Canvas code from scratch.

## Pick the right template

| If the diagram shows... | Use |
|---|---|
| Sequential steps in order | `Pipeline` |
| A choice with branches | `DecisionTree` |
| Two or more options side-by-side | `Comparison` |
| A loop that repeats | `Cycle` |
| One source spreading to many targets | `FanOut` |
| Multiple tiers of a system | `Architecture` |
| Events on a timeline | `Timeline` |

## Templates with examples

### Pipeline — sequential steps

```python
from plotcraft import Pipeline

Pipeline("How HTTPS works") \
    .step("You type a URL") \
    .step("DNS Lookup") \
    .step("TLS Handshake", emphasize=True) \
    .step("Certificate Check") \
    .step("Page Loads") \
    .caption("Every request, in milliseconds") \
    .save("https.png")
```

Use `emphasize=True` for the most important step.
Add `annotation="extra info"` to put a note next to a step.

### DecisionTree — branching choice

```python
from plotcraft import DecisionTree

DecisionTree("Picking your database") \
    .question("Structured data?") \
    .branch("Yes", "PostgreSQL", note="ACID, joins, complex queries") \
    .branch("No", "MongoDB", note="Flexible schema, JSON-native") \
    .caption("Start simple, migrate when you outgrow it") \
    .save("db.png")
```

Always call `.question()` first, then `.branch()` for each option.

### Comparison — side-by-side options

```python
from plotcraft import Comparison

Comparison("Monolith vs Microservices") \
    .option("Monolith", points=[
        "Single deployment",
        "Tightly coupled",
        "Vertical scaling only",
    ]) \
    .option("Microservices", points=[
        "Independent deploys",
        "Loosely coupled",
        "Horizontal scaling",
    ]) \
    .save("compare.png")
```

### Cycle — feedback loop

```python
from plotcraft import Cycle

Cycle("How AI agents reason") \
    .step("Observe") \
    .step("Think", emphasize=True) \
    .step("Act") \
    .feedback("until done") \
    .caption("Repeat until goal is reached") \
    .save("cycle.png")
```

### FanOut — one source to many targets

```python
from plotcraft import FanOut

FanOut("How events propagate") \
    .source("Event Bus") \
    .target("Logger") \
    .target("Notifier", emphasize=True) \
    .target("Archiver") \
    .target("Analytics") \
    .caption("Every event reaches every consumer") \
    .save("events.png")
```

Always call `.source()` first, then `.target()` for each downstream consumer.

### Architecture — multi-tier system

```python
from plotcraft import Architecture

Architecture("How a request flows") \
    .tier("Frontend", ["Browser", "CDN", "Load Balancer"]) \
    .tier("Backend", ["API Server", "Auth Service"]) \
    .tier("Data", ["PostgreSQL", "Redis"]) \
    .caption("Each tier scales independently") \
    .save("arch.png")
```

### Timeline — events in order

```python
from plotcraft import Timeline

Timeline("Product roadmap") \
    .event("Q1", "Research") \
    .event("Q2", "Build", emphasize=True) \
    .event("Q3", "Beta") \
    .event("Q4", "Launch") \
    .save("roadmap.png")
```

## Themes

Add `theme="..."` to any template:

```python
Pipeline("Title", theme="ocean").step("X").save("out.png")

# Available themes:
# default, earth, grape, ocean, vanilla, cool, mixed
```

Add `dark=True` for dark mode:

```python
Pipeline("Title", dark=True).step("X").save("out.png")
```

## Output formats

The `.save()` method picks format from the file extension:

```python
.save("out.png")          # PNG image
.save("out.svg")          # SVG image
.save("out.excalidraw")   # Excalidraw JSON (no rendering needed)
```

## DO

- Pick the template that matches what you're showing
- Use `emphasize=True` to highlight 1-2 key elements
- Write a clear `title()` that states the insight ("How HTTPS works", not "HTTPS Diagram")
- Add a `caption()` with one sentence of takeaway
- Keep step names short (1-3 words)

## DON'T

- Don't write `Scene()` or `Canvas()` code directly — use a template
- Don't try to combine templates in one diagram — pick one
- Don't add more than 8 steps to a Pipeline (split into two diagrams instead)
- Don't emphasize everything (1-2 elements max)

## If no template fits

If you genuinely need something none of the templates cover (e.g., a custom spatial composition like a slime mold network or a tournament bracket), see `LLM-SKILL.md` for the full Scene/Canvas APIs. But 90% of diagrams fit a template.
