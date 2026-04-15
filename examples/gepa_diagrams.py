"""Recreate the GEPA mutation diagrams with richer D2 features."""

import subprocess
import tempfile
import os

def render_d2(source: str, output_path: str, dark: bool = False):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".d2", delete=False) as f:
        f.write(source)
        d2_path = f.name
    try:
        cmd = ["d2", "--sketch", "--pad", "80"]
        cmd.extend(["--theme", "200" if dark else "0"])
        cmd.extend([d2_path, output_path])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.strip().split(chr(10))[0]}")
        else:
            print(f"  -> {output_path}")
    finally:
        os.unlink(d2_path)


# --------------------------------------------------------------------------
# 1. Synaptic Pruning — 5-stage horizontal pipeline with internal detail
# --------------------------------------------------------------------------

print("1. Synaptic Pruning")
render_d2(r'''
direction: right

title: "Synaptic Pruning\nOne-shot compression: generate overspecified, measure each piece, cut dead weight, strengthen" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

generate: "1. Generate (x3)" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 12

  p1: |md
    **Prompt 1**
    Score: 0.65
  | {style.fill: "#DBEAFE"; style.stroke: "#93C5FD"}
  p2: |md
    **Prompt 2**
    Score: 0.58
  | {style.fill: "#DBEAFE"; style.stroke: "#93C5FD"}
  p3: |md
    **Prompt 3**
    Score: 0.62
  | {style.fill: "#DBEAFE"; style.stroke: "#93C5FD"}

  best: "best = Prompt 1" {
    style.font-size: 12
    style.font-color: "#16A34A"
    shape: text
  }
}

ablate: "2. Ablate Each" {
  style.fill: "#FFF7ED"
  style.stroke: "#F59E0B"
  style.border-radius: 12

  sa: "Section A: -0.08 (critical)" {style.fill: "#FEE2E2"; style.stroke: "#EF4444"}
  sb: "Section B: -0.12 (critical)" {style.fill: "#FEE2E2"; style.stroke: "#EF4444"}
  sc: "Section C: -0.002 (prunable)" {style.fill: "#F3F4F6"; style.stroke: "#9CA3AF"; style.opacity: 0.6}
  sd: "Section D: -0.03 (neutral)" {style.fill: "#F9FAFB"; style.stroke: "#D1D5DB"}
  se: "Section E: +0.01 (harmful)" {style.fill: "#F3F4F6"; style.stroke: "#9CA3AF"; style.opacity: 0.6}

  note: "Remove each section,\nmeasure score impact" {
    shape: text
    style.font-size: 11
    style.font-color: "#6B7280"
  }
}

prune: "3. Prune" {
  style.fill: "#F0FDF4"
  style.stroke: "#22C55E"
  style.border-radius: 12

  keep_a: "Section A" {style.fill: "#DCFCE7"; style.stroke: "#22C55E"}
  keep_b: "Section B" {style.fill: "#DCFCE7"; style.stroke: "#22C55E"}
  keep_d: "Section D" {style.fill: "#F9FAFB"; style.stroke: "#D1D5DB"}

  cut: "C, E removed\n(dead weight or harmful)" {
    shape: text
    style.font-size: 11
    style.font-color: "#6B7280"
  }
}

strengthen: "4. Strengthen" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 12

  sa2: "Section A (strengthened)" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  sb2: "Section B (strengthened)" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  sd2: "Section D" {style.fill: "#F9FAFB"; style.stroke: "#D1D5DB"}

  note2: "LLM rewrites critical\nsections for clarity" {
    shape: text
    style.font-size: 11
    style.font-color: "#6B7280"
  }
}

final: "5. Final Prompt" {
  style.fill: "#F0FDF4"
  style.stroke: "#16A34A"
  style.border-radius: 12
  style.font-size: 16
  style.bold: true

  result: |md
    **Minimal, Effective Prompt**
    ~800 chars (from ~2000)
  | {style.fill: "#DCFCE7"; style.stroke: "#16A34A"}

  metric: "25-460 rollouts\n15-100x fewer than GEPA" {
    shape: text
    style.font-size: 12
    style.font-color: "#16A34A"
    style.bold: true
  }
}

generate -> ablate
ablate -> prune: "cut" {style.stroke: "#EF4444"}
prune -> strengthen: "reinforce" {style.stroke: "#3B82F6"}
strengthen -> final {style.stroke-width: 3; style.stroke: "#16A34A"}

footer: "pipeline (no iteration)" {
  shape: text
  style.font-size: 13
  style.font-color: "#9CA3AF"
  near: bottom-center
}
''', "examples/renders/gepa_synaptic_pruning.png")


# --------------------------------------------------------------------------
# 2. Tournament — bracket with generation strategies
# --------------------------------------------------------------------------

print("2. Tournament")
render_d2(r'''
direction: right

title: "Tournament: Single-Elimination Bracket\nMaximum initial diversity, head-to-head elimination, no mutation" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

strategies: "4 Generation Strategies" {
  style.fill: "#FFF7ED"
  style.stroke: "#F59E0B"
  style.border-radius: 12

  grid-columns: 1
  s1: "Reasoning (x16)" {style.fill: "#FEF3C7"; style.stroke: "#F59E0B"}
  s2: "Format (x16)" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  s3: "Detail Level (x16)" {style.fill: "#E0E7FF"; style.stroke: "#6366F1"}
  s4: "Error Prevention (x16)" {style.fill: "#FEE2E2"; style.stroke: "#EF4444"}
  seed: "+ seed prompt" {shape: text; style.font-size: 12; style.font-color: "#6B7280"}
}

pool: |md
  **64 candidates**
  Pool frozen
| {
  style.fill: "#F3F4F6"
  style.stroke: "#6B7280"
}

bracket: "Single-Elimination Bracket" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 12

  r1: "R1: 32 matches\n5 examples each" {style.fill: "#DBEAFE"}
  r2: "R2: 16 matches\n7 examples each" {style.fill: "#DBEAFE"}
  semi: "Semi: 8 matches\n10 examples each" {style.fill: "#DBEAFE"}
  qf: "QF: 4 matches\n15 examples each" {style.fill: "#93C5FD"; style.stroke: "#3B82F6"}
  final: "Final: 20 examples" {style.fill: "#3B82F6"; style.stroke: "#1D4ED8"; style.font-color: "#FFFFFF"}

  r1 -> r2 -> semi -> qf -> final
}

champion: |md
  **Champion**
  Full validation set
| {
  style.fill: "#DCFCE7"
  style.stroke: "#16A34A"
  style.font-size: 16
  style.bold: true
}

strategies -> pool
pool -> bracket.r1 {style.stroke-width: 3}
bracket.final -> champion {style.stroke-width: 3; style.stroke: "#16A34A"}

warning: |md
  **No mutation between rounds**
  If the best prompt wasn't
  generated in step 1,
  it can never be found.
| {
  shape: text
  style.font-size: 12
  style.font-color: "#EF4444"
}

footer: "Evaluation rigor increases: 5 -> 7 -> 10 -> 15 -> 20 -> full valset (~1,000-1,500 rollouts)" {
  shape: text
  style.font-size: 13
  style.font-color: "#9CA3AF"
  near: bottom-center
}
''', "examples/renders/gepa_tournament.png")


# --------------------------------------------------------------------------
# 3. Slime Mold — progressive narrowing with mutation between rounds
# --------------------------------------------------------------------------

print("3. Slime Mold")
render_d2(r'''
direction: right

title: "Slime Mold: Progressive Pruning\nExplore widely, eliminate weakest, mutate survivors, repeat until one champion remains" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

gen: "Generate 20" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 12

  grid-columns: 4
  c1: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c2: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c3: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c4: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c5: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c6: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c7: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c8: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c9: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c10: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c11: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c12: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  seed: "." {shape: circle; style.fill: "#16A34A"; width: 24; height: 24}
  c14: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c15: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c16: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c17: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c18: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c19: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
  c20: "." {shape: circle; style.fill: "#93C5FD"; width: 24; height: 24}
}

r1: "Round 1\n10 examples" {
  style.fill: "#FFF7ED"
  style.stroke: "#F59E0B"
  style.border-radius: 12

  keep: "keep 10" {shape: text; style.font-size: 12; style.font-color: "#F59E0B"}
}

mutate1: "mutate via\nfailure info" {
  shape: diamond
  style.fill: "#E0E7FF"
  style.stroke: "#6366F1"
  style.font-size: 12
}

r2: "Round 2\n15 examples" {
  style.fill: "#FFF7ED"
  style.stroke: "#F59E0B"
  style.border-radius: 12

  keep2: "keep 5" {shape: text; style.font-size: 12; style.font-color: "#F59E0B"}
}

mutate2: "mutate via\nfailure info" {
  shape: diamond
  style.fill: "#E0E7FF"
  style.stroke: "#6366F1"
  style.font-size: 12
}

r3: "Round 3\n20 examples" {
  style.fill: "#FFF7ED"
  style.stroke: "#F59E0B"
  style.border-radius: 12

  keep3: "keep 3" {shape: text; style.font-size: 12; style.font-color: "#F59E0B"}
}

r4: "Round 4\n30 examples" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 12

  keep4: "keep 1" {shape: text; style.font-size: 12; style.font-color: "#3B82F6"; style.bold: true}
}

champion: |md
  **Champion**
| {
  shape: oval
  style.fill: "#DCFCE7"
  style.stroke: "#16A34A"
  style.font-size: 18
  style.bold: true
}

gen -> r1 {style.stroke-width: 2}
r1 -> mutate1
mutate1 -> r2
r2 -> mutate2
mutate2 -> r3
r3 -> r4 {style.stroke-width: 2}
r4 -> champion {style.stroke-width: 3; style.stroke: "#16A34A"}

key: |md
  **Key:** Survivors are REWRITTEN
  between rounds (not just filtered)
| {
  shape: text
  style.font-size: 12
  style.font-color: "#6366F1"
}

footer: "20 -> 10 -> 5 -> 3 -> 1  (~540-930 rollouts)" {
  shape: text
  style.font-size: 13
  style.font-color: "#9CA3AF"
  near: bottom-center
}
''', "examples/renders/gepa_slime_mold.png")


# --------------------------------------------------------------------------
# 4. Contrastive Reflection — GEPA loop + memory box
# --------------------------------------------------------------------------

print("4. Contrastive Reflection")
render_d2(r'''
direction: right

title: "Contrastive Reflection\nSame GEPA loop, but reflection gets evidence from historical success/failure pairs" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

seed: "Seed\nPrompt" {
  shape: oval
  style.fill: "#DCFCE7"
  style.stroke: "#16A34A"
}

gen1: "Gen 1" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 8

  reflect: "LLM reflects\n+ contrastive evidence" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  candidates: "candidates" {style.fill: "#F3F4F6"}
  reflect -> candidates
}

gen2: "Gen 2" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 8

  reflect2: "inject contrastive\nevidence into reflection" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  candidates2: "candidates" {style.fill: "#F3F4F6"}
  reflect2 -> candidates2
}

genN: "Gen N" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 8

  reflect3: "reflect" {style.fill: "#DBEAFE"}
  candidates3: "candidates" {style.fill: "#F3F4F6"}
  reflect3 -> candidates3
}

best: "Best\nPrompt" {
  shape: oval
  style.fill: "#DCFCE7"
  style.stroke: "#16A34A"
  style.font-size: 16
  style.bold: true
}

memory: "Contrastive Score Memory\nCand 0: ex17=0.3 ex42=0.8 | Cand 1: ex17=0.9 ex42=0.3\n...accumulates per-example scores (CPU-only, zero LLM cost)..." {
  style.fill: "#1E1B4B"
  style.stroke: "#7C3AED"
  style.font-color: "#E0E7FF"
  style.font-size: 13
  style.border-radius: 8
}

seed -> gen1
gen1 -> gen2
gen2 -> genN: "..." {style.stroke-dash: 3}
genN -> best {style.stroke-width: 3; style.stroke: "#16A34A"}

memory -> gen1.reflect: "evidence" {style.stroke: "#7C3AED"; style.stroke-dash: 3}
memory -> gen2.reflect2: "evidence" {style.stroke: "#7C3AED"; style.stroke-dash: 3}
gen1 -> memory: "record scores" {style.stroke: "#7C3AED"; style.stroke-dash: 3}
gen2 -> memory: "record scores" {style.stroke: "#7C3AED"; style.stroke-dash: 3}

benefits: |md
  **Zero extra LLM cost**
  Pure CPU memory lookup
  Same budget as GEPA
| {
  shape: text
  style.font-size: 13
  style.font-color: "#16A34A"
  style.bold: true
}
''', "examples/renders/gepa_contrastive.png")


# --------------------------------------------------------------------------
# 5. GEPA Baseline — evolutionary loop with generations
# --------------------------------------------------------------------------

print("5. GEPA Baseline")
render_d2(r'''
direction: right

title: "GEPA: Evolutionary Prompt Optimization\nICLR 2026 Oral  |  arXiv:2507.19457" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

seed: "Seed\nPrompt" {
  shape: oval
  style.fill: "#DCFCE7"
  style.stroke: "#16A34A"
  style.font-size: 14
}

gen1: "Generation 1" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 8

  reflect1: "LLM reflects\non failures" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  pareto1: "Pareto selects\ndiverse frontier" {style.fill: "#F3F4F6"; style.stroke: "#9CA3AF"}
  pruned1: "pruned" {shape: text; style.font-size: 11; style.font-color: "#9CA3AF"}
  reflect1 -> pareto1
}

gen2: "Generation 2" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 8

  reflect2: "reflect" {style.fill: "#DBEAFE"}
  merge: "merge two\nparents" {style.fill: "#DBEAFE"; style.stroke: "#3B82F6"}
  pareto2: "select" {style.fill: "#F3F4F6"}
  reflect2 -> merge -> pareto2
}

genN: "Generation N" {
  style.fill: "#EFF6FF"
  style.stroke: "#3B82F6"
  style.border-radius: 8

  reflectN: "reflect" {style.fill: "#DBEAFE"}
  paretoN: "select" {style.fill: "#F3F4F6"}
  reflectN -> paretoN
}

best: "Best\nPrompt" {
  shape: oval
  style.fill: "#DCFCE7"
  style.stroke: "#16A34A"
  style.font-size: 16
  style.bold: true
}

seed -> gen1 {style.stroke-width: 2}
gen1 -> gen2 {style.stroke-width: 2}
gen2 -> genN: "..." {style.stroke-dash: 3}
genN -> best {style.stroke-width: 3; style.stroke: "#16A34A"}

legend: |md
  **Legend**
  Arrows = LLM reflection (mutate) or Pareto selection (carry forward)
| {
  shape: text
  style.font-size: 12
  style.font-color: "#6B7280"
  near: bottom-center
}
''', "examples/renders/gepa_baseline.png")


print("\nAll GEPA renders in examples/renders/")
