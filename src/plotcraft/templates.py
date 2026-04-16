"""Pre-built diagram templates for common patterns.

These templates produce high-quality diagrams from minimal data input.
Designed for small LLMs that struggle with picking layouts and writing
raw Scene/Canvas code.

Each template:
1. Takes structured data (lists of strings, dicts)
2. Picks the right Scene or Canvas internally
3. Handles all spacing, layout, color decisions
4. Saves to .png/.svg/.excalidraw

Usage:
    from plotcraft.templates import Pipeline, DecisionTree, Comparison

    Pipeline("How code reaches production") \\
        .step("Push commit") \\
        .step("Run tests", emphasize=True) \\
        .step("Deploy") \\
        .save("pipeline.png")
"""
from __future__ import annotations

from typing import Optional, Sequence, Union
from plotcraft.scene import Scene, Palette

ThemeLike = Union[str, Palette, dict]


# ══════════════════════════════════════════════════════════════════
# Pipeline — sequential stages
# ══════════════════════════════════════════════════════════════════

class Pipeline:
    """Sequential left-to-right flow.

    Pipeline("How HTTPS works") \\
        .step("You type a URL") \\
        .step("DNS Lookup") \\
        .step("TLS Handshake", emphasize=True) \\
        .step("Page Loads") \\
        .caption("Every request, in milliseconds") \\
        .save("https.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._steps: list[tuple[str, bool, Optional[str]]] = []  # (text, emphasize, annotation)
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def step(self, text: str, emphasize: bool = False, annotation: Optional[str] = None) -> "Pipeline":
        self._steps.append((text, emphasize, annotation))
        return self

    def caption(self, text: str) -> "Pipeline":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")

        for i, (text, emphasize, annotation) in enumerate(self._steps):
            if i == 0:
                role = "start"
            elif i == len(self._steps) - 1:
                role = "end"
            else:
                role = "process"
            kwargs = {"role": role}
            if emphasize:
                kwargs["emphasis"] = "high"
            s.add(text, **kwargs)
            if annotation:
                s.annotate(annotation, near=text)

        for i in range(len(self._steps) - 1):
            s.connect(self._steps[i][0], self._steps[i + 1][0])

        if self._caption:
            s.add(self._caption, role="caption")

        s.layout("pipeline")
        s.save(path)


# ══════════════════════════════════════════════════════════════════
# DecisionTree — branching logic
# ══════════════════════════════════════════════════════════════════

class DecisionTree:
    """Branching decision diagram.

    DecisionTree("Picking your database") \\
        .question("Structured?") \\
        .branch("Yes", "PostgreSQL", note="ACID, joins") \\
        .branch("No", "MongoDB", note="Flexible schema") \\
        .save("db.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._question: Optional[str] = None
        self._branches: list[tuple[str, str, Optional[str]]] = []  # (label, target, note)
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def question(self, text: str) -> "DecisionTree":
        self._question = text
        return self

    def branch(self, label: str, target: str, note: Optional[str] = None) -> "DecisionTree":
        self._branches.append((label, target, note))
        return self

    def caption(self, text: str) -> "DecisionTree":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        if not self._question:
            raise ValueError("DecisionTree needs a question — call .question(text)")

        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")
        s.add(self._question, role="decision", size="large")

        for label, target, note in self._branches:
            s.add(target, role="end", size="large")
            s.connect(self._question, target, label=label)
            if note:
                s.annotate(note, near=target)

        if self._caption:
            s.add(self._caption, role="caption")

        s.layout("decision_tree")
        s.save(path)


# ══════════════════════════════════════════════════════════════════
# Comparison — side-by-side options
# ══════════════════════════════════════════════════════════════════

class Comparison:
    """Side-by-side comparison of options.

    Comparison("Monolith vs Microservices") \\
        .option("Monolith", points=["Single deploy", "Tightly coupled"]) \\
        .option("Microservices", points=["Independent deploy", "Scale per service"]) \\
        .save("compare.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._options: list[tuple[str, list[str]]] = []  # (name, points)
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def option(self, name: str, points: Sequence[str]) -> "Comparison":
        self._options.append((name, list(points)))
        return self

    def caption(self, text: str) -> "Comparison":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")

        # Render each option as a labeled stack. Use explicit ids so that
        # repeated point text across options doesn't collide, while keeping
        # the visible label clean (no "OptionName: " prefix).
        for i, (name, points) in enumerate(self._options):
            role = "start" if i == 0 else "end"
            header_id = f"opt_{i}_header"
            s.add(name, id=header_id, role=role, size="large", emphasis="high")
            prev_id = header_id
            for j, point in enumerate(points):
                point_id = f"opt_{i}_{j}"
                s.add(point, id=point_id, role="process")
                s.connect(prev_id, point_id)
                prev_id = point_id

        if self._caption:
            s.add(self._caption, role="caption")

        s.layout("top_down")
        s.save(path)


# ══════════════════════════════════════════════════════════════════
# Cycle — feedback loop
# ══════════════════════════════════════════════════════════════════

class Cycle:
    """Feedback loop / iterative process.

    Cycle("How AI agents learn") \\
        .step("Observe") \\
        .step("Think", emphasize=True) \\
        .step("Act") \\
        .feedback("Repeat until done") \\
        .save("loop.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._steps: list[tuple[str, bool]] = []
        self._feedback_label: Optional[str] = None
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def step(self, text: str, emphasize: bool = False) -> "Cycle":
        self._steps.append((text, emphasize))
        return self

    def feedback(self, label: str) -> "Cycle":
        self._feedback_label = label
        return self

    def caption(self, text: str) -> "Cycle":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")
        for text, emphasize in self._steps:
            kwargs = {"role": "process"}
            if emphasize:
                kwargs["emphasis"] = "high"
            s.add(text, **kwargs)
        for i in range(len(self._steps) - 1):
            s.connect(self._steps[i][0], self._steps[i + 1][0])
        if self._steps:
            s.connect(self._steps[-1][0], self._steps[0][0],
                      label=self._feedback_label or "loop", style="dashed")
        if self._caption:
            s.add(self._caption, role="caption")
        s.layout("cycle")
        s.save(path)


# ══════════════════════════════════════════════════════════════════
# FanOut — one source to many targets
# ══════════════════════════════════════════════════════════════════

class FanOut:
    """One source distributing to multiple targets.

    FanOut("Event propagation") \\
        .source("Event Bus") \\
        .target("Logger") \\
        .target("Notifier", emphasize=True) \\
        .target("Archiver") \\
        .save("events.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._source: Optional[str] = None
        self._targets: list[tuple[str, bool]] = []
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def source(self, text: str) -> "FanOut":
        self._source = text
        return self

    def target(self, text: str, emphasize: bool = False) -> "FanOut":
        self._targets.append((text, emphasize))
        return self

    def caption(self, text: str) -> "FanOut":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        if not self._source:
            raise ValueError("FanOut needs a source — call .source(text)")
        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")
        s.add(self._source, role="start", size="large", emphasis="high")
        for text, emphasize in self._targets:
            kwargs = {"role": "process"}
            if emphasize:
                kwargs["emphasis"] = "high"
            s.add(text, **kwargs)
            s.connect(self._source, text)
        if self._caption:
            s.add(self._caption, role="caption")
        s.layout("fan_out")
        s.save(path)


# ══════════════════════════════════════════════════════════════════
# Architecture — tiered system
# ══════════════════════════════════════════════════════════════════

class Architecture:
    """Multi-tier architecture diagram.

    Architecture("How a request flows") \\
        .tier("Frontend", ["Browser", "CDN"]) \\
        .tier("Backend", ["API Server", "Auth"]) \\
        .tier("Data", ["PostgreSQL", "Redis"]) \\
        .save("arch.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._tiers: list[tuple[str, list[str]]] = []
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def tier(self, name: str, components: Sequence[str]) -> "Architecture":
        self._tiers.append((name, list(components)))
        return self

    def caption(self, text: str) -> "Architecture":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")

        # Render each tier as a SINGLE consolidated box: tier name as the
        # header, components listed inside via newlines. This avoids the
        # orphan-box problem of trying to layout N shapes per tier with
        # the top-down engine.
        tier_ids: list[str] = []
        for i, (tier_name, components) in enumerate(self._tiers):
            tier_id = f"tier_{i}"
            tier_ids.append(tier_id)
            label = tier_name + "\n" + "\n".join(f"• {c}" for c in components)
            if i == 0:
                role = "start"
            elif i == len(self._tiers) - 1:
                role = "end"
            else:
                role = "process"
            s.add(label, id=tier_id, role=role, size="large")

        # Tier-to-tier connections, top-down
        for i in range(len(tier_ids) - 1):
            s.connect(tier_ids[i], tier_ids[i + 1], weight="bold")

        if self._caption:
            s.add(self._caption, role="caption")

        s.layout("top_down")
        s.save(path)


# ══════════════════════════════════════════════════════════════════
# Timeline — sequential events on an axis
# ══════════════════════════════════════════════════════════════════

class Timeline:
    """Sequential events along a timeline.

    Timeline("Product roadmap") \\
        .event("Q1", "Research") \\
        .event("Q2", "Build", emphasize=True) \\
        .event("Q3", "Beta") \\
        .event("Q4", "Launch") \\
        .save("roadmap.png")
    """

    def __init__(self, title: str, theme: ThemeLike = "default", dark: bool = False):
        self._title = title
        self._events: list[tuple[str, str, bool]] = []  # (when, what, emphasize)
        self._caption: Optional[str] = None
        self._theme = theme
        self._dark = dark

    def event(self, when: str, what: str, emphasize: bool = False) -> "Timeline":
        self._events.append((when, what, emphasize))
        return self

    def caption(self, text: str) -> "Timeline":
        self._caption = text
        return self

    def save(self, path: str) -> None:
        s = Scene(theme=self._theme, dark=self._dark)
        s.add(self._title, role="title")

        for i, (when, what, emphasize) in enumerate(self._events):
            label = f"{when}: {what}"
            if i == 0:
                role = "start"
            elif i == len(self._events) - 1:
                role = "end"
            else:
                role = "process"
            kwargs = {"role": role}
            if emphasize:
                kwargs["emphasis"] = "high"
            s.add(label, **kwargs)

        for i in range(len(self._events) - 1):
            a = f"{self._events[i][0]}: {self._events[i][1]}"
            b = f"{self._events[i+1][0]}: {self._events[i+1][1]}"
            s.connect(a, b)

        if self._caption:
            s.add(self._caption, role="caption")

        s.layout("pipeline")
        s.save(path)
