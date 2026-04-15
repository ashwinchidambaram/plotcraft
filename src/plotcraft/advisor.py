"""Design advisor module for PlotCraft.

Provides programmatic design guidance for LLM agents building diagrams,
including visual pattern suggestions and diagram validation.
"""

from __future__ import annotations

from dataclasses import dataclass

from plotcraft.types import ColorTheme, ShapeKind, TextRole


@dataclass(frozen=True)
class VisualPattern:
    """A named visual pattern with design hints for building a diagram."""

    name: str
    description: str
    keywords: tuple[str, ...]  # terms that suggest this pattern
    layout: str  # "horizontal", "vertical", "radial", "cycle", "tree"
    shape_hints: dict[str, ShapeKind]  # role_name -> suggested shape
    color_hints: dict[str, ColorTheme]  # role_name -> suggested theme


PATTERNS: list[VisualPattern] = [
    VisualPattern(
        name="pipeline",
        description="Sequential left-to-right flow",
        keywords=("steps", "flow", "process", "sequence", "workflow", "stages"),
        layout="horizontal",
        shape_hints={"start": ShapeKind.RECT, "step": ShapeKind.RECT, "end": ShapeKind.RECT},
        color_hints={"start": ColorTheme.START, "step": ColorTheme.NEUTRAL, "end": ColorTheme.END},
    ),
    VisualPattern(
        name="fan_out",
        description="One source radiating to multiple targets",
        keywords=("distribute", "broadcast", "source", "emit", "dispatch", "spawn"),
        layout="radial",
        shape_hints={"source": ShapeKind.CIRCLE, "target": ShapeKind.RECT},
        color_hints={"source": ColorTheme.START, "target": ColorTheme.NEUTRAL},
    ),
    VisualPattern(
        name="convergence",
        description="Multiple inputs merging to one output",
        keywords=("merge", "aggregate", "collect", "combine", "funnel", "gather"),
        layout="radial",
        shape_hints={"input": ShapeKind.RECT, "output": ShapeKind.CIRCLE},
        color_hints={"input": ColorTheme.NEUTRAL, "output": ColorTheme.END},
    ),
    VisualPattern(
        name="cycle",
        description="Circular flow returning to start",
        keywords=("loop", "iterate", "repeat", "feedback", "retry", "recursive", "react"),
        layout="cycle",
        shape_hints={"observe": ShapeKind.RECT, "decide": ShapeKind.DIAMOND, "act": ShapeKind.RECT},
        color_hints={"observe": ColorTheme.INFO, "decide": ColorTheme.DECISION, "act": ColorTheme.HIGHLIGHT},
    ),
    VisualPattern(
        name="decision_tree",
        description="Top-down branching logic",
        keywords=("branch", "if", "else", "condition", "switch", "route", "decide"),
        layout="vertical",
        shape_hints={"root": ShapeKind.DIAMOND, "branch": ShapeKind.DIAMOND, "leaf": ShapeKind.OVAL},
        color_hints={"root": ColorTheme.DECISION, "branch": ColorTheme.DECISION, "leaf": ColorTheme.END},
    ),
    VisualPattern(
        name="timeline",
        description="Linear progression with markers",
        keywords=("phases", "milestones", "history", "roadmap", "schedule", "progress"),
        layout="horizontal",
        shape_hints={"milestone": ShapeKind.CIRCLE, "phase": ShapeKind.RECT, "marker": ShapeKind.OVAL},
        color_hints={"milestone": ColorTheme.HIGHLIGHT, "phase": ColorTheme.NEUTRAL, "marker": ColorTheme.INFO},
    ),
    VisualPattern(
        name="hierarchy",
        description="Top-down parent-child structure",
        keywords=("parent", "child", "org", "taxonomy", "tree", "nested", "inherit"),
        layout="tree",
        shape_hints={"root": ShapeKind.RECT, "parent": ShapeKind.RECT, "child": ShapeKind.OVAL},
        color_hints={"root": ColorTheme.START, "parent": ColorTheme.NEUTRAL, "child": ColorTheme.INFO},
    ),
    VisualPattern(
        name="comparison",
        description="Side-by-side parallel structures",
        keywords=("vs", "compare", "tradeoff", "alternative", "option", "pros", "cons"),
        layout="horizontal",
        shape_hints={"label": ShapeKind.NONE, "option": ShapeKind.RECT, "point": ShapeKind.OVAL},
        color_hints={"label": ColorTheme.NEUTRAL, "option": ColorTheme.HIGHLIGHT, "point": ColorTheme.INFO},
    ),
    VisualPattern(
        name="annotated_flow",
        description="Flow diagram with supporting callouts and annotations",
        keywords=("annotate", "explain", "context", "callout", "note", "comment"),
        layout="horizontal",
        shape_hints={"step": ShapeKind.RECT, "callout": ShapeKind.RECT, "annotation": ShapeKind.NONE},
        color_hints={"step": ColorTheme.NEUTRAL, "callout": ColorTheme.WARNING, "annotation": ColorTheme.INFO},
    ),
    VisualPattern(
        name="visual_essay",
        description="Multi-section composition with mixed patterns and decoratives",
        keywords=("essay", "infographic", "editorial", "multi-section", "composition", "overview"),
        layout="vertical",
        shape_hints={"section_title": ShapeKind.NONE, "content": ShapeKind.RECT, "decor": ShapeKind.CIRCLE},
        color_hints={"section_title": ColorTheme.NEUTRAL, "content": ColorTheme.INFO, "decor": ColorTheme.HIGHLIGHT},
    ),
]


def suggest_pattern(keywords: list[str]) -> list[VisualPattern]:
    """Suggest visual patterns based on concept keywords.

    Returns patterns sorted by relevance (most keyword matches first).
    Only returns patterns with at least 1 keyword match.

    Matching is case-insensitive and partial (e.g., "looping" matches "loop").
    """
    normalized = [kw.lower() for kw in keywords]

    scored: list[tuple[int, VisualPattern]] = []
    for pattern in PATTERNS:
        score = sum(
            1
            for input_kw in normalized
            for pattern_kw in pattern.keywords
            if pattern_kw in input_kw or input_kw in pattern_kw
        )
        if score > 0:
            scored.append((score, pattern))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [pattern for _, pattern in scored]


def validate_diagram(diagram: object) -> list[str]:
    """Validate a diagram against design best practices.

    Takes a Diagram instance, returns list of warning strings.
    Empty list means no issues found.

    Uses duck typing — accesses diagram._shapes and diagram._connectors directly.
    """
    warnings: list[str] = []

    shapes: dict = diagram._shapes  # type: ignore[attr-defined]
    connectors: list = diagram._connectors  # type: ignore[attr-defined]

    if not shapes:
        return warnings

    # Build outgoing/incoming connector counts per shape
    outgoing: dict[str, int] = {sid: 0 for sid in shapes}
    incoming: dict[str, int] = {sid: 0 for sid in shapes}
    for conn in connectors:
        src = conn.source_shape_id
        tgt = conn.target_shape_id
        if src in outgoing:
            outgoing[src] += 1
        if tgt in incoming:
            incoming[tgt] += 1

    # 1. Diamond with insufficient branches
    for sid, shape in shapes.items():
        if shape.kind == ShapeKind.DIAMOND:
            n = outgoing.get(sid, 0)
            if n < 2:
                warnings.append(
                    f"Diamond '{sid}' has {n} outgoing connector(s) — "
                    "decision shapes typically need 2+ branches"
                )

    # 2. Container overuse
    total = len(shapes)
    non_none_count = sum(1 for s in shapes.values() if s.kind != ShapeKind.NONE)
    if total > 5:
        pct = round(non_none_count / total * 100)
        if pct > 70:
            warnings.append(
                f"Consider using free-text labels (ShapeKind.NONE) — "
                f"{pct}% of elements use container shapes"
            )

    # 3. Missing visual hierarchy
    has_hierarchy = any(
        s.role in (TextRole.TITLE, TextRole.SUBTITLE) for s in shapes.values()
    )
    if not has_hierarchy:
        warnings.append(
            "No visual hierarchy — consider adding a TITLE or SUBTITLE element"
        )

    # 4. Disconnected elements
    for sid, shape in shapes.items():
        if shape.kind == ShapeKind.NONE:
            continue
        if outgoing.get(sid, 0) == 0 and incoming.get(sid, 0) == 0:
            warnings.append(
                f"Shape '{sid}' has no connections — isolated elements may confuse viewers"
            )

    # 5. Missing semantic color
    all_neutral = all(s.color_theme == ColorTheme.NEUTRAL for s in shapes.values())
    if all_neutral:
        warnings.append(
            "All shapes use neutral color — consider semantic colors "
            "(START, END, DECISION) to encode meaning"
        )

    return warnings


SHAPE_SEMANTICS: dict[ShapeKind, str] = {
    ShapeKind.RECT: "Process, action, or step",
    ShapeKind.SQUARE: "Equal-weight process or checkpoint",
    ShapeKind.CIRCLE: "Terminal state, milestone, or endpoint",
    ShapeKind.OVAL: "Start point, end point, or soft boundary",
    ShapeKind.DIAMOND: "Decision, condition, or branch point",
    ShapeKind.NONE: "Label, annotation, or free-text (preferred for descriptions)",
}
