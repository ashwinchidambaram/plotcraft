"""GEPA diagrams — flat layout, no containers, clean arrow routing."""

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
# 1. How GEPA works — the core loop
# --------------------------------------------------------------------------

print("1. GEPA Core")
render_d2(r'''
direction: down

title: "How GEPA evolves prompts" {
  shape: text
  style.font-size: 28
  style.bold: true
  near: top-center
}

seed: Seed Prompt {
  shape: oval
  style.fill: "#FCF0ED"
  style.stroke: "#A84F3B"
}

sample: Sample Minibatch {
  style.fill: "#F3EFE8"
  style.stroke: "#B0A898"
}

eval: Evaluate on 3 examples {
  style.fill: "#F3EFE8"
  style.stroke: "#B0A898"
}

reflect: |md
  **Reflect on Failures**
  LLM analyzes *why* the prompt failed
| {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}

generate: Generate Candidates {
  style.fill: "#F3EFE8"
  style.stroke: "#B0A898"
}

pareto: Pareto Selection {
  shape: diamond
  style.fill: "#FDF8F0"
  style.stroke: "#5E422A"
}

merge: System-Aware Merge {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}

result: Optimized Prompt {
  shape: oval
  style.fill: "#E3E8DF"
  style.stroke: "#485240"
  style.font-size: 18
}

seed -> sample
sample -> eval
eval -> reflect
reflect -> generate
generate -> pareto
pareto -> sample: iterate {
  style.stroke-dash: 5
  style.stroke: "#D4A574"
}
pareto -> merge: converged {
  style.stroke-width: 3
}
merge -> result {
  style.stroke-width: 3
}

caption: "Iterative reflection on minibatches, Pareto frontier for diversity" {
  shape: text
  style.font-size: 13
  style.font-color: "#757575"
  near: bottom-center
}
''', "examples/renders/gepa_core.png")


# --------------------------------------------------------------------------
# 2. The five mutations — fan-out from GEPA
# --------------------------------------------------------------------------

print("2. Five Mutations")
render_d2(r'''
direction: down

title: "Five ways to mutate GEPA" {
  shape: text
  style.font-size: 28
  style.bold: true
  near: top-center
}

gepa: GEPA Baseline {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
  style.font-size: 18
  style.bold: true
}

cr: |md
  **Contrastive Reflection**
  Mine success/failure pairs from history
  *Zero extra LLM cost*
| {
  style.fill: "#FCF0ED"
  style.stroke: "#A84F3B"
}

sp: |md
  **Synaptic Pruning**
  Overspecify then ablate sections
  *15-100x fewer rollouts*
| {
  style.fill: "#FDF8F0"
  style.stroke: "#5E422A"
}

sm: |md
  **Slime Mold**
  Progressive colony pruning
  *20 → 10 → 5 → 3 → 1*
| {
  style.fill: "#FDF8F0"
  style.stroke: "#5E422A"
}

to: |md
  **Tournament**
  64-candidate single elimination
  *~900 rollouts, no iteration*
| {
  style.fill: "#E3E8DF"
  style.stroke: "#485240"
}

bk: |md
  **Best-of-K**
  K candidates per iteration
  *Simple search multiplier*
| {
  style.fill: "#E3E8DF"
  style.stroke: "#485240"
}

gepa -> cr: augment reflection
gepa -> sp: replace loop
gepa -> sm: replace selection
gepa -> to: replace loop
gepa -> bk: widen candidates

caption: "Each mutation targets a different bottleneck in the optimization loop" {
  shape: text
  style.font-size: 13
  style.font-color: "#757575"
  near: bottom-center
}
''', "examples/renders/gepa_mutations.png")


# --------------------------------------------------------------------------
# 3. Synaptic Pruning — the most novel mutation
# --------------------------------------------------------------------------

print("3. Synaptic Pruning")
render_d2(r'''
direction: down

title: "Synaptic Pruning: overspecify, ablate, strengthen" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

p1: "Prompt 1 (~500 words)" {style.fill: "#F3EFE8"; style.stroke: "#B0A898"}
p2: "Prompt 2 (~500 words)" {style.fill: "#F3EFE8"; style.stroke: "#B0A898"}
p3: "Prompt 3 (~500 words)" {style.fill: "#F3EFE8"; style.stroke: "#B0A898"}

eval: |md
  **Evaluate all 3** on 40 examples
| {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}

best: Pick best {
  shape: diamond
  style.fill: "#FDF8F0"
  style.stroke: "#5E422A"
}

parse: Parse into sections {
  style.fill: "#F3EFE8"
  style.stroke: "#B0A898"
}

ablate: |md
  **Ablate each section**
  Remove it, measure score delta
| {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}

load: "Load-bearing (delta > 0.05)" {
  style.fill: "#E3E8DF"
  style.stroke: "#485240"
}

dead: "Prunable (delta < 0.01)" {
  style.fill: "#F3EFE8"
  style.stroke: "#B0B0A8"
  style.opacity: 0.6
}

strengthen: |md
  **Strengthen** load-bearing
  sections via reflection
| {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}

result: Lean, sharp prompt {
  shape: oval
  style.fill: "#E3E8DF"
  style.stroke: "#485240"
  style.font-size: 18
}

p1 -> eval
p2 -> eval
p3 -> eval
eval -> best
best -> parse
parse -> ablate
ablate -> load
ablate -> dead
load -> strengthen
strengthen -> result {style.stroke-width: 3}

caption: "Start big, remove what doesn't matter, double down on what does" {
  shape: text
  style.font-size: 13
  style.font-color: "#757575"
  near: bottom-center
}
''', "examples/renders/gepa_pruning.png")


# --------------------------------------------------------------------------
# 4. Tournament bracket
# --------------------------------------------------------------------------

print("4. Tournament")
render_d2(r'''
direction: down

title: "Tournament: 64 enter, 1 wins" {
  shape: text
  style.font-size: 24
  style.bold: true
  near: top-center
}

gen: |md
  **Generate 64 candidates**
  4 strategies: paraphrase,
  elaborate, contrast, specialize
| {
  style.fill: "#FCF0ED"
  style.stroke: "#A84F3B"
}

r1: "Round 1: 32 matches × 5 examples" {style.fill: "#F3EFE8"; style.stroke: "#B0A898"}
r2: "Round 2: 16 matches × 7 examples" {style.fill: "#F3EFE8"; style.stroke: "#B0A898"}
r3: "Round 3: 8 matches × 10 examples" {style.fill: "#FDF8F0"; style.stroke: "#5E422A"}
qf: "Quarterfinals: 4 matches × 15 examples" {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}
sf: "Semifinals: 2 matches × 20 examples" {
  style.fill: "#D4745E"
  style.stroke: "#853D2D"
  style.font-color: "#E8DCC4"
}

champion: Champion {
  shape: oval
  style.fill: "#E3E8DF"
  style.stroke: "#485240"
  style.font-size: 18
  style.bold: true
}

gen -> r1: "64 → 32" {style.stroke-width: 2}
r1 -> r2: "32 → 16"
r2 -> r3: "16 → 8"
r3 -> qf: "8 → 4"
qf -> sf: "4 → 2" {style.stroke-width: 2}
sf -> champion: "winner" {style.stroke-width: 3}

caption: "No iteration, no reflection — just competition. ~900 rollouts total." {
  shape: text
  style.font-size: 13
  style.font-color: "#757575"
  near: bottom-center
}
''', "examples/renders/gepa_tournament.png")


# --------------------------------------------------------------------------
# 5. Experiment landscape — dark theme
# --------------------------------------------------------------------------

print("5. Experiment Landscape (dark)")
render_d2(r'''
direction: right

title: "GEPA Mutations: 540 Experiments" {
  shape: text
  style.font-size: 28
  style.bold: true
  near: top-center
}

methods: |md
  ### 6 Methods
  GEPA, Contrastive, Pruning,
  Slime Mold, Tournament, Best-of-K
| {
  style.fill: "#3D1F17"
  style.stroke: "#D4745E"
  style.font-color: "#E8DCC4"
}

benchmarks: |md
  ### 6 Benchmarks
  HotpotQA, IFBench, HoVer,
  PUPA, LiveBench, AIME
| {
  style.fill: "#2E2214"
  style.stroke: "#D4A574"
  style.font-color: "#E8DCC4"
}

models: |md
  ### 3 Scales
  Qwen3-1.7B
  Qwen3-4B
  Qwen3-8B
| {
  style.fill: "#1A2830"
  style.stroke: "#6B8FA3"
  style.font-color: "#E8DCC4"
}

seeds: |md
  ### 5 Seeds
  42, 123, 456,
  789, 1024
| {
  style.fill: "#1E2B1E"
  style.stroke: "#8B9D83"
  style.font-color: "#E8DCC4"
}

result: |md
  ### 540 Runs
  Full factorial design
| {
  style.fill: "#853D2D"
  style.stroke: "#D4745E"
  style.font-color: "#E8DCC4"
  style.bold: true
  style.font-size: 16
}

methods -> benchmarks: "×" {style.stroke-width: 3}
benchmarks -> models: "×" {style.stroke-width: 3}
models -> seeds: "×" {style.stroke-width: 3}
seeds -> result: "=" {style.stroke-width: 3}

caption: "Every method tested on every benchmark at every scale" {
  shape: text
  style.font-size: 13
  style.font-color: "#8B8B8B"
  near: bottom-center
}
''', "examples/renders/gepa_landscape.png", dark=True)


print("\nAll renders in examples/renders/")
