# PlotCraft Diagram Skill

A Claude Code skill for creating polished, argument-driven diagrams.

## Setup

### 1. Install PlotCraft

```bash
cd /path/to/plotcraft
uv sync
```

### 2. Install draw.io (for high-quality rendering)

**macOS:**
```bash
brew install --cask drawio
```

**Or download:** https://www.drawio.com/

### 3. Add the skill to Claude Code

Add to your `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run python *)",
      "Bash(/Applications/draw.io.app/Contents/MacOS/draw.io --export *)"
    ]
  }
}
```

## Usage

Just ask Claude to create a diagram:

- "Draw a diagram of the ReAct agent loop"
- "Create a flowchart showing how authentication works"
- "Visualize our deployment pipeline"
- "Compare monolith vs microservices architecture"

The skill will:
1. Plan the diagram using visual design methodology
2. Choose the right pattern (pipeline, cycle, decision tree, etc.)
3. Generate PlotCraft Python code
4. Export via draw.io for polished rendering
5. Show you the result and iterate

## What Makes This Different

This skill embeds design methodology from Patrick Winston's MIT communication framework and the Excalidraw visual design system:

- **Diagrams argue, they don't display** — every element carries meaning
- **The Promise** — every diagram has a title that states the insight, not just the topic
- **The 5S Framework** — Symbol, Slogan, Surprise, Salient idea, Story
- **Isomorphism Test** — structure communicates even without text
- **Pattern Matching** — 8 visual patterns matched to concept behavior
