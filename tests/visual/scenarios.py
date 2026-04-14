"""Visual test scenarios for PlotCraft hand-drawn design verification."""

from plotcraft import (
    Diagram, TextRole, ShapeKind, TextAlign, AnchorName,
    ArrowDirection, ConnectorStyle, LineWeight, ColorTheme,
    SectionStyle,
)
from tests.visual.harness import VisualScenario


def _build_basic_flowchart() -> Diagram:
    """Simple 4-node flowchart with connectors."""
    # RECT(BODY)=1r×2c, DIAMOND(BODY)=2r×2c, CIRCLE(BODY)=2r×1c
    return (
        Diagram()
        .add("start", "Start Here", role=TextRole.BODY, shape=ShapeKind.RECT, color=ColorTheme.START, row=0, col=0)
        .add("process", "Process Data", role=TextRole.BODY, shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=0, col=2)
        .add("decide", "Valid?", role=TextRole.BODY, shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=0, col=4)
        .add("end", "Done", role=TextRole.BODY, shape=ShapeKind.CIRCLE, color=ColorTheme.END, row=0, col=6)
        .connect("start", "process")
        .connect("process", "decide")
        .connect("decide", "end", label="Yes")
    )


def _build_all_shapes() -> Diagram:
    """One of each shape kind to verify they all render with wobble."""
    # RECT(BODY)=1r×2c, SQUARE(BODY)=2r×1c, CIRCLE(BODY)=2r×1c
    # OVAL(BODY)=2r×2c, DIAMOND(BODY)=2r×2c, NONE=free-floating
    return (
        Diagram()
        .add("rect", "Rectangle", shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=0, col=0)
        .add("sq", "Square", shape=ShapeKind.SQUARE, color=ColorTheme.HIGHLIGHT, row=0, col=2)
        .add("circ", "Circle", shape=ShapeKind.CIRCLE, color=ColorTheme.INFO, row=0, col=3)
        .add("oval", "Oval Shape", shape=ShapeKind.OVAL, color=ColorTheme.SUCCESS, row=2, col=0)
        .add("dia", "Diamond", shape=ShapeKind.DIAMOND, color=ColorTheme.DECISION, row=2, col=2)
        .add("none", "Free Text", shape=ShapeKind.NONE, role=TextRole.CAPTION, row=2, col=4)
    )


def _build_color_themes() -> Diagram:
    """All 9 color themes in a grid."""
    # Default role=BODY; some labels like "Decision"/"Highlight" span 2 cols,
    # so space columns by 2 to avoid placement collisions.
    d = Diagram()
    themes = list(ColorTheme)
    for i, theme in enumerate(themes):
        row = i // 3
        col = (i % 3) * 2
        d.add(theme.value, theme.value.title(), color=theme, row=row, col=col)
    return d


def _build_connectors() -> Diagram:
    """Various connector styles, weights, and directions."""
    # RECT(BODY)=1r×2c — space horizontally by 4 cols, vertically by 2 rows
    return (
        Diagram()
        .add("a", "Node A", row=0, col=0, color=ColorTheme.START)
        .add("b", "Node B", row=0, col=4, color=ColorTheme.NEUTRAL)
        .add("c", "Node C", row=2, col=0, color=ColorTheme.INFO)
        .add("d", "Node D", row=2, col=4, color=ColorTheme.END)
        .connect("a", "b", label="Solid", style=ConnectorStyle.SOLID, line_weight=LineWeight.NORMAL)
        .connect("c", "d", label="Dashed Bold", style=ConnectorStyle.DASHED, line_weight=LineWeight.BOLD)
        .connect("a", "c", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
                 direction=ArrowDirection.BOTH, style=ConnectorStyle.DOTTED)
        .connect("b", "d", source_anchor=AnchorName.BOTTOM_CENTER, target_anchor=AnchorName.TOP_CENTER,
                 direction=ArrowDirection.NONE)
    )


def _build_text_hierarchy() -> Diagram:
    """Title, subtitle, body, caption to show typography hierarchy."""
    # TITLE=3r×3c, SUBTITLE=2r×2c, BODY=1r×2c, CAPTION=1r×2c
    return (
        Diagram()
        .add("title", "Main Title", role=TextRole.TITLE, shape=ShapeKind.RECT, color=ColorTheme.HIGHLIGHT, row=0, col=0)
        .add("sub", "Subtitle Text", role=TextRole.SUBTITLE, shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=0, col=3)
        .add("body", "Body text content", role=TextRole.BODY, shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=3, col=0)
        .add("cap", "Small caption", role=TextRole.CAPTION, shape=ShapeKind.RECT, color=ColorTheme.NEUTRAL, row=3, col=3)
    )


SCENARIOS = [
    VisualScenario(
        name="basic_flowchart",
        description="Simple flowchart with 4 shapes and connectors",
        build_diagram=_build_basic_flowchart,
        expected_behaviors=[
            "Shapes have wobbly/hand-drawn edges, not perfectly geometric",
            "Text uses handwriting-style fonts (Caveat for titles, Patrick Hand for body)",
            "Canvas background is warm cream/off-white color (#fdf6e3)",
            "Shape fills appear translucent/semi-transparent",
            "Connectors are smooth curved lines with visible arrowheads",
            "Different color themes are visually distinct (green start, yellow decision, red end)",
        ],
        unexpected_behaviors=[
            "Shapes with perfectly straight edges and sharp 90-degree corners",
            "Arial, Helvetica, or other sans-serif system fonts visible in shapes",
            "Pure white (#ffffff) background",
            "Completely opaque solid fills with no transparency",
            "Text overflowing outside shape boundaries",
            "Shapes overlapping each other",
        ],
    ),
    VisualScenario(
        name="all_shapes",
        description="One of each shape kind to verify wobble on all types",
        build_diagram=_build_all_shapes,
        expected_behaviors=[
            "All shapes (rectangle, square, circle, oval, diamond) have wobbly/hand-drawn edges",
            "Diamond shape has 4 distinct vertices forming a rotated square",
            "Circle is roughly round but with organic imperfections",
            "Free text (NONE shape) appears without any visible container shape",
            "Each shape has a distinct fill color matching its theme",
        ],
        unexpected_behaviors=[
            "Any shape with perfectly geometric/computer-drawn edges",
            "Missing shapes (fewer than 6 visible elements)",
            "Shapes that look broken or garbled rather than intentionally hand-drawn",
        ],
    ),
    VisualScenario(
        name="color_themes",
        description="All 9 color themes displayed",
        build_diagram=_build_color_themes,
        expected_behaviors=[
            "9 distinct shapes are visible, each with a different fill color",
            "Fills are translucent/semi-transparent (background slightly visible through them)",
            "Colors are warm and muted (not neon or harsh)",
            "Each theme label is readable inside its shape",
        ],
        unexpected_behaviors=[
            "All shapes appear the same color",
            "Completely opaque fills with no transparency",
            "Any shape with text that is unreadable or cut off",
        ],
    ),
    VisualScenario(
        name="connectors",
        description="Various connector styles, weights, and directions",
        build_diagram=_build_connectors,
        expected_behaviors=[
            "Multiple connector lines are visible between shapes",
            "At least one connector has visible arrowhead(s)",
            "Solid, dashed, and dotted line styles are distinguishable",
            "Connector labels are readable with background behind text",
            "Bold connector is noticeably thicker than normal weight",
        ],
        unexpected_behaviors=[
            "Connectors that are perfectly straight rigid lines (should have slight curve/wobble)",
            "Missing arrowheads on connectors that should have them",
            "Labels that overlap with connector lines making them unreadable",
        ],
    ),
    VisualScenario(
        name="text_hierarchy",
        description="Title/subtitle/body/caption showing typography scale",
        build_diagram=_build_text_hierarchy,
        expected_behaviors=[
            "Clear size hierarchy: title is largest, caption is smallest",
            "At least 2 different handwriting-style fonts are visible",
            "Title text is noticeably larger and bolder than body text",
            "All text is readable and properly positioned within shapes",
        ],
        unexpected_behaviors=[
            "All text appears the same size",
            "Monospace or standard sans-serif fonts visible (Arial, Helvetica, Courier)",
            "Text extending outside shape boundaries",
        ],
    ),
]
