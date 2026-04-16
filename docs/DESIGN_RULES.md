# PlotCraft Design Rules

Hard-won rules from iterating on real diagrams. Follow these BEFORE generating any diagram to avoid the common mistakes that cost iterations.

## Choose Your Mode First

| What you're making | Mode | Why |
|---|---|---|
| Flowchart, decision tree, pipeline | **Scene API → D2** | D2 handles layout, text centering, arrow routing |
| Evolution tree, bracket, timeline axis | **Excalidraw (spatial)** | Needs pixel-level control of node positions |
| Dot clusters, progressive narrowing | **Excalidraw (spatial)** | COUNT of elements IS the visual story |
| Biological metaphor, organic shapes | **Excalidraw (spatial)** | Wobble paths, blobs, petri dishes |
| Side-by-side comparison panels | **Excalidraw (spatial)** | Consistent anchors across panels |

## Spacing Rules

```
Title (36-38px)
  ↕ 12-15px
Subtitle (12-13px)
  ↕ 30px+ ← separate visual zones, don't merge
Section headers (13-15px)
  ↕ 20px
Content (illustrations, blocks, dots)
  ↕ radius * 0.4 minimum
Captions / annotations
  ↕ 20px
Flow line / pipeline label
  ↕ 20px
Legend
  ↕ 20px
Footer
```

Each zone gets its own y-band. Never share a y-band between two pieces of text.

## Arrow Rules

1. **All horizontal arrows at the same y-level.** Don't drop one lower — it looks broken.

2. **40px+ clear runway.** Measure: element edge → arrow start → arrow end → next element. Nothing else in that corridor.

3. **Text beside blocks = arrow collisions.** Labels to the right of shapes sit exactly where horizontal arrows go. Put text INSIDE blocks or BELOW, never to the right in a horizontal flow.

4. **No clear runway? Don't force arrows.** Use a flow underline instead — one continuous arrow below all content with tick marks at transition points.

5. **Flow underline tick labels need 10px+ gap below the arrow.** Labels touching the line are unreadable.

## Text Placement

- **Metadata inside blocks.** Delta scores, kind labels, status → inside the block, not beside it. Right-align numbers.
- **Two-line blocks need 38px+ height.** Name on line 1, kind/status on line 2.
- **Checkmarks replace verbose labels.** "Section A ✓" inside a block beats "Section A" + "strengthened" outside.
- **Colors are labels.** If the legend explains what red/gray/green mean, don't also write "(critical)" beside every element.
- **Reader vocabulary, not code vocabulary.** "R5" not "SF". "Champion" not "best_candidate".

## Grid and Dot Layouts

- **Uniform element sizes.** Don't encode information in SIZE when COUNT already communicates it. Progressive sizing causes collisions between adjacent groups.
- **Trace pixel math during review.** Compute: `element_x + element_width < next_element_x`. Don't eyeball — calculate.
- **Dot spacing = 16px** for 6px-radius dots works well. Adjust proportionally.

## Multi-Panel Layouts

- **Consistent anchor positions across panels.** Food sources, nodes, reference points stay in the same relative position so viewers can track evolution.
- **Panel spacing = illustration_radius × 4.** Enough room for transition arrows + labels.
- **Text NEVER inside illustration framing** (petri dishes, borders). All labels outside.
- **Cap illustrations at ~250px diameter.** Larger ones cover text.
- **Reserve 40%+ of total height for text zones.**

## Visual Differentiation

Each diagram in a set needs a unique visual identity. If two diagrams look interchangeable, redesign one.

Differentiate through:
- **Structure**: bracket vs dot clusters vs pipeline blocks vs tree vs panels
- **Color progression**: uniform (frozen) vs darkening (iterative refinement)
- **Unique elements**: memory boxes, mutation diamonds, strikethrough blocks, bracket lines

The visual metaphor should match the algorithm:
- Tournament = converging bracket (1v1 pairs merge)
- Progressive pruning = dot clusters with mutation diamonds (leaderboard cutoff)
- Ablation pipeline = colored blocks being cut/strengthened (linear transformation)
- Evolutionary optimization = branching tree with timeline axis (generations)
- Contrastive learning = standard tree + prominent memory/evidence box

## Diagram Type Quick Reference

| Visual pattern | Best for | Key elements |
|---|---|---|
| **Converging bracket** | Head-to-head elimination | Pair lines merging into winners |
| **Dot clusters** | Leaderboard cutoffs (top-K) | Uniform dots, shrinking groups, flow underline |
| **Pipeline blocks** | Linear stages | Colored rectangles, arrows between stages |
| **Evolution tree** | Branching across generations | Circles at positions, arrows showing lineage |
| **Petri dish panels** | Biological metaphors | Circular framing, organic veins, food sources |
| **Timeline + nodes** | Temporal progression | Horizontal axis with tick marks, nodes above |

## D2-Specific Rules

- **Never use D2 containers** when arrows need to cross container borders — they collide with container labels. Use flat layouts instead.
- **`near: object`** only works with TALA (paid). Use `near: top-center` / `near: bottom-center` (constants) with dagre/elk.
- **`direction: right`** for pipelines, **`direction: down`** for everything else.
- **Title + subtitle** as a single text block with `\n` separator if using `near: top-center` (two separate `near: top-center` elements overlap).

## Pre-Flight Checklist

Before rendering, verify:

- [ ] 40px+ clear space for every arrow
- [ ] Text inside blocks, not beside them (in horizontal flows)
- [ ] All horizontal arrows at the same y-level
- [ ] 20px+ between every text zone
- [ ] For grids: pixel math confirms no overlap between groups
- [ ] For dense layouts: using flow underline instead of individual arrows
- [ ] This diagram is visually distinct from other diagrams in the set
- [ ] Reader-friendly labels (not code variable names)
- [ ] Legend explains all colors and symbols used
