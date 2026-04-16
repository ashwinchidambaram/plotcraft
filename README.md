# PlotCraft

> Your AI is great at writing. It's great at coding. It is **catastrophically bad at diagrams**.
> Crooked boxes. Arrows through letters. Tiny grey labels.
> PlotCraft fixes that.

<div align="center">
  <img src="examples/renders/neural_network_learning.png" alt="How a neural network learns" width="60%" />
</div>

That diagram came from a single sentence: *"draw me how a neural network learns."* No design tools. No fiddling with arrows. No swearing at PowerPoint.

---

## What is this, exactly?

PlotCraft is a tool that lets you **just ask for a diagram in plain English** and get a polished, hand-drawn one back. You don't open Figma. You don't drag boxes around. You type what you want, and the diagram appears.

Think of it like having a designer who only does whiteboard sketches, sitting next to your AI assistant, ready to draw anything you describe.

---

## How it works

PlotCraft is built for **[Claude Code](https://claude.com/claude-code)** — Anthropic's coding assistant that runs in your terminal. You install Claude Code once, drop PlotCraft's "skill" folder into the right place, and from then on Claude knows how to draw beautiful diagrams from anything you describe in plain English. Examples below.

> **Heads up:** Today PlotCraft is tuned specifically for Claude Code. Support for ChatGPT, Cursor, Gemini, and local models (Ollama) is on the [roadmap](#roadmap--whats-coming-next).

---

## Get started in 60 seconds

You'll need:

1. **A Mac or Linux computer** (Windows support coming soon)
2. **[Claude Code](https://claude.com/claude-code) installed** — Anthropic has a one-line installer
3. **Python 3.12 or newer** — most computers already have it; if not, download from [python.org](https://www.python.org)

Then, in your terminal:

```bash
# 1. Install PlotCraft
pip install plotcraft

# 2. Install the diagram skill into Claude Code
git clone https://github.com/ashwinchidambaram/plotcraft
cp -r plotcraft/skills/plotcraft-diagram ~/.claude/skills/
```

That's it. Now open Claude Code and ask it to draw something.

> The first time you make a diagram, PlotCraft will quietly download the two helpers it needs (a layout engine called D2, and a tiny browser called Chromium for the fancy spatial diagrams). After that, everything is local and instant.

---

## Things you can ask Claude to draw

Copy any prompt below into Claude Code with the skill installed. Each one produces a polished diagram in seconds.

### Step-by-step processes

> *"Show me how the immune system fights an infection."*

<div align="center">
  <img src="examples/renders/readme_pipeline.png" alt="Immune system pipeline" width="55%" />
</div>

### Decisions

> *"Are you out of Claude Code usage? Show the options."*

<div align="center">
  <img src="examples/renders/readme_claude_meme.png" alt="Out of Claude Code usage" width="55%" />
</div>

### Comparisons

> *"Compare iPhone vs Android side by side, three points each."*

<div align="center">
  <img src="examples/renders/readme_comparison.png" alt="iPhone vs Android" width="40%" />
</div>

### Feedback loops

> *"Visualize the writer's revision loop — draft, get feedback, revise, repeat."*

<div align="center">
  <img src="examples/renders/readme_cycle.png" alt="Writer revision loop" width="40%" />
</div>

### One-to-many flows

> *"What happens when I press send on an email? Show every place it goes."*

<div align="center">
  <img src="examples/renders/readme_fanout.png" alt="Email fan-out" width="55%" />
</div>

### Multi-tier systems

> *"Show me how a restaurant works: front of house, kitchen, suppliers."*

<div align="center">
  <img src="examples/renders/readme_architecture.png" alt="Restaurant architecture" width="35%" />
</div>

### Timelines

> *"Make a timeline of a product launch year — Q1 research, Q2 build, Q3 beta, Q4 launch."*

<div align="center">
  <img src="examples/renders/readme_timeline.png" alt="Product launch timeline" width="55%" />
</div>

Don't like the result? Just say *"use blue colors"* or *"emphasize the second step"* or *"make it darker"* and Claude will regenerate.

---

## When templates aren't enough

For richer concepts — branching paths, multiple endpoints, feedback loops, scientific systems — Claude reaches for the **Scene API**. Same conversation, more elaborate output. Try prompts like:

> *"Diagram the life cycle of a star, including what happens to high-mass and low-mass stars."*

<div align="center">
  <img src="examples/renders/readme_star_lifecycle.png" alt="Life cycle of a star" width="65%" />
</div>

> *"Explain how TikTok's recommendation algorithm decides what to show me."*

<div align="center">
  <img src="examples/renders/readme_tiktok.png" alt="TikTok algorithm" width="75%" />
</div>

And for genuinely custom infographics — slime molds, tournament brackets, evolutionary trees — there's a **Canvas API** that gives Claude pixel-precise spatial control. See the [GEPA project](https://github.com/ashwinchidambaram/gepa-mutations) for examples in the wild.

---

## Pick a vibe — eight color palettes built in

Every diagram ships in your choice of palette. You don't need to know color theory, just say *"use the ocean theme"*:

<div align="center">
  <img src="examples/renders/template_theme_default.png" alt="terracotta" width="24%" />
  <img src="examples/renders/template_theme_ocean.png" alt="ocean" width="24%" />
  <img src="examples/renders/template_theme_forest.png" alt="forest" width="24%" />
  <img src="examples/renders/template_theme_sunset.png" alt="sunset" width="24%" />
</div>
<div align="center">
  <img src="examples/renders/template_theme_grape.png" alt="grape" width="24%" />
  <img src="examples/renders/template_theme_monochrome.png" alt="monochrome" width="24%" />
  <img src="examples/renders/template_theme_pastel.png" alt="pastel" width="24%" />
  <img src="examples/renders/template_theme_vanilla.png" alt="vanilla" width="24%" />
</div>

Built-in palettes: **default** (terracotta), **ocean**, **forest**, **sunset**, **grape**, **monochrome**, **pastel**, **vanilla**. Plus a dark mode for any of them.

### Want your own brand colors?

Just tell Claude:

> *"Use these colors: #FF6B35 for highlights, #0066AA for endings, white background."*

And it'll build you a custom palette and use it. Save the palette once, reuse it on every diagram you make.

---

## For developers — yes, you can use it directly

If you want to skip Claude Code and call PlotCraft from your own Python script, you can. The same templates work as a fluent builder:

```python
from plotcraft import Pipeline

Pipeline("How HTTPS works") \
    .step("You type a URL") \
    .step("DNS Lookup") \
    .step("TLS Handshake", emphasize=True) \
    .step("Page Loads") \
    .caption("Every request, in milliseconds") \
    .save("https.png")
```

Three layers of API depending on how much control you want:

- **Templates** — seven prebuilt diagram types, fluent builders, ~5 lines of code
- **Scene API** — describe elements + connections, layout is automatic
- **Canvas API** — pixel-precise spatial composition for custom infographics

Full API reference is in [`skills/plotcraft-diagram/LLM-SKILL.md`](skills/plotcraft-diagram/LLM-SKILL.md). Design rules and best practices in [`docs/DESIGN_RULES.md`](docs/DESIGN_RULES.md).

---

## Roadmap — what's coming next

PlotCraft today is great if you use Claude Code. Here's what's next.

### v2: Support for other AI assistants
Today, the skill format is Claude-specific. Coming soon:
- **ChatGPT** — custom GPT + plugin
- **Cursor** — `.cursorrules` integration
- **Continue.dev / Cody** — extension support
- **Gemini Code** — once their skill format stabilizes

### v3: A local SLM that drives PlotCraft
A small (~3B parameter) language model, fine-tuned specifically to translate plain English into PlotCraft template calls. Bundled with the package, runs locally via [llama.cpp](https://github.com/ggerganov/llama.cpp) or [Ollama](https://ollama.com).

```bash
plotcraft sketch "show me how OAuth works"
# → reasoning happens locally, on your machine
# → PlotCraft renders the result
# → you get a polished diagram, no API key, no network, no cloud
```

**Why bother?**
- **Privacy** — your diagrams never leave your machine
- **Offline** — works on a plane or in a basement
- **Free** — no per-render API cost
- **Fast** — local inference is sub-second on an M-series Mac

The whole `SLM-SKILL.md` document is already structured around this — every template is a recipe a 3B model can reliably follow. The fine-tune is the missing piece.

### Other things on the list
- Windows support
- More diagram types (sankey, swimlane, sequence diagrams)
- A web playground (paste a prompt, see the diagram)
- Animated diagrams (GIF / MP4 export)
- An MCP server so any AI agent framework can use it

If any of these sound fun to work on, [open an issue](https://github.com/ashwinchidambaram/plotcraft/issues) — I'd love collaborators.

---

## Built on the shoulders of giants

PlotCraft is the assembly — these are the brilliant pieces that make it possible:

| Tool | What it does for us |
| --- | --- |
| **[Claude Code](https://claude.com/claude-code)** by Anthropic | The AI assistant that actually drives PlotCraft. The whole skill system is what makes "just ask for a diagram" possible. |
| **[D2](https://d2lang.com)** by Terrastruct | The layout engine and sketch-mode renderer behind every flowchart. Honestly the secret sauce. |
| **[dagre](https://github.com/dagrejs/dagre)** | The graph-layout algorithm D2 uses to figure out where boxes go and how arrows route. |
| **[Excalidraw](https://excalidraw.com)** | The hand-drawn JSON format powering the spatial diagrams, plus the renderer used by the Playwright pipeline. |
| **[Playwright](https://playwright.dev)** by Microsoft | Headless Chromium for rendering Excalidraw diagrams to PNG and SVG. |
| **[Hatchling](https://hatch.pypa.io/)** by the Hatch team | The Python build backend that bundles everything into one clean install. |
| **[uv](https://docs.astral.sh/uv/)** by Astral | Package manager that makes Python development not painful. |

Aesthetic inspiration from Figma's hand-drawn whiteboard mode, Edward Tufte's information design, and Dan Roam's *The Back of the Napkin*. The core belief is Tufte's: **diagrams should argue, not just display.**

---

## Development

If you want to hack on PlotCraft itself:

```bash
git clone https://github.com/ashwinchidambaram/plotcraft
cd plotcraft
uv sync
uv run pytest         # 49 tests, all passing
uv run python examples/test_all_templates.py  # render every template + theme
```

PRs welcome — especially for new templates, new color palettes, Windows support, or anyone who wants to take a swing at the local-SLM future.

---

<div align="center">
  <a href="https://github.com/ashwinchidambaram"><img src="assets/ac-blackhole-static.svg" alt="Built by Ashwin Chidambaram" width="260" /></a>
</div>

<div align="center">
  <sub>MIT licensed. Built because I hate shitty diagrams.</sub>
</div>
