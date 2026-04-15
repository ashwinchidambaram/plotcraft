"""Tests for the Excalidraw renderer."""

import json
import os

import pytest

from plotcraft import (
    Diagram,
    ShapeKind,
    ColorTheme,
    TextRole,
    ArrowDirection,
    ConnectorStyle,
    LineWeight,
    AnchorName,
    SectionStyle,
)


def find_elements(data, elem_type=None, id_prefix=None):
    """Find elements in Excalidraw data by type or id prefix."""
    return [
        e
        for e in data["elements"]
        if (elem_type is None or e["type"] == elem_type)
        and (id_prefix is None or e["id"].startswith(id_prefix))
    ]


def test_single_rect_produces_valid_json():
    """A single RECT shape produces a valid Excalidraw JSON document."""
    d = Diagram()
    d.add("a", "Hello", shape=ShapeKind.RECT, row=0, col=0)
    result = d.render_excalidraw()

    assert result["type"] == "excalidraw"
    assert result["version"] == 2
    assert len(result["elements"]) > 0
    assert result["appState"]["viewBackgroundColor"] == "#F9F7F4"


def test_shape_kinds_map_correctly():
    """Each ShapeKind maps to the correct Excalidraw element type."""
    d = Diagram()
    d.add("rect", "R", shape=ShapeKind.RECT, row=0, col=0)
    d.add("square", "S", shape=ShapeKind.SQUARE, row=0, col=1)
    d.add("circle", "C", shape=ShapeKind.CIRCLE, row=0, col=2)
    d.add("oval", "O", shape=ShapeKind.OVAL, row=1, col=0)
    d.add("diamond", "D", shape=ShapeKind.DIAMOND, row=1, col=1)
    result = d.render_excalidraw()

    expected = {
        "rect": "rectangle",
        "square": "rectangle",
        "circle": "ellipse",
        "oval": "ellipse",
        "diamond": "diamond",
    }

    for shape_id, exc_type in expected.items():
        elems = find_elements(result, id_prefix=f"exc_shape_{shape_id}")
        assert len(elems) == 1, f"Expected 1 element for {shape_id}, got {len(elems)}"
        assert elems[0]["type"] == exc_type, (
            f"Shape {shape_id}: expected type '{exc_type}', got '{elems[0]['type']}'"
        )


def test_none_shape_is_free_floating_text():
    """ShapeKind.NONE produces only a text element with no containerId."""
    d = Diagram()
    d.add("free", "Free Label", shape=ShapeKind.NONE, row=0, col=0)
    result = d.render_excalidraw()

    # Should have no shape element for this id
    shape_elems = find_elements(result, id_prefix="exc_shape_free")
    assert len(shape_elems) == 0

    # Should have a text element
    text_elems = find_elements(result, elem_type="text", id_prefix="exc_text_free")
    assert len(text_elems) == 1
    text_elem = text_elems[0]
    assert text_elem.get("containerId") is None or text_elem.get("containerId") == ""


def test_color_theme_mapping():
    """ColorThemes map to the correct Excalidraw fill and stroke colors."""
    d = Diagram()
    d.add("s", "Start", shape=ShapeKind.RECT, color=ColorTheme.START, row=0, col=0)
    d.add("e", "End", shape=ShapeKind.RECT, color=ColorTheme.END, row=0, col=1)
    d.add("dec", "Decision", shape=ShapeKind.RECT, color=ColorTheme.DECISION, row=0, col=2)
    result = d.render_excalidraw()

    expected_colors = {
        "s": {"fill": "#FCF0ED", "stroke": "#A84F3B"},
        "e": {"fill": "#E3E8DF", "stroke": "#485240"},
        "dec": {"fill": "#FDF8F0", "stroke": "#5E422A"},
    }

    for shape_id, colors in expected_colors.items():
        elems = find_elements(result, id_prefix=f"exc_shape_{shape_id}")
        assert len(elems) == 1, f"No shape element found for {shape_id}"
        elem = elems[0]
        assert elem["backgroundColor"] == colors["fill"], (
            f"Shape {shape_id}: expected fill '{colors['fill']}', got '{elem['backgroundColor']}'"
        )
        assert elem["strokeColor"] == colors["stroke"], (
            f"Shape {shape_id}: expected stroke '{colors['stroke']}', got '{elem['strokeColor']}'"
        )


def test_arrow_bindings_bidirectional():
    """Arrow has startBinding/endBinding, and both shapes list the arrow in boundElements."""
    d = Diagram()
    d.add("a", "Source", shape=ShapeKind.RECT, row=0, col=0)
    d.add("b", "Target", shape=ShapeKind.RECT, row=0, col=1)
    d.connect("a", "b")
    result = d.render_excalidraw()

    # Find the arrow element
    arrows = find_elements(result, elem_type="arrow")
    assert len(arrows) >= 1
    arrow = arrows[0]

    # Arrow should bind to source and target shapes
    assert arrow["startBinding"] is not None
    assert arrow["startBinding"]["elementId"] == "exc_shape_a"
    assert arrow["endBinding"] is not None
    assert arrow["endBinding"]["elementId"] == "exc_shape_b"

    # Both shapes should list the arrow in their boundElements
    shape_a = find_elements(result, id_prefix="exc_shape_a")[0]
    shape_b = find_elements(result, id_prefix="exc_shape_b")[0]

    arrow_id = arrow["id"]
    bound_ids_a = [be["id"] for be in shape_a.get("boundElements", [])]
    bound_ids_b = [be["id"] for be in shape_b.get("boundElements", [])]
    assert arrow_id in bound_ids_a, "Arrow not found in source shape's boundElements"
    assert arrow_id in bound_ids_b, "Arrow not found in target shape's boundElements"


def test_arrow_directions():
    """Each ArrowDirection maps to the correct arrowhead configuration."""
    cases = [
        (ArrowDirection.FORWARD, None, "arrow"),
        (ArrowDirection.BACKWARD, "arrow", None),
        (ArrowDirection.BOTH, "arrow", "arrow"),
        (ArrowDirection.NONE, None, None),
    ]

    for direction, expected_start, expected_end in cases:
        d = Diagram()
        d.add("a", "A", shape=ShapeKind.RECT, row=0, col=0)
        d.add("b", "B", shape=ShapeKind.RECT, row=0, col=1)
        d.connect("a", "b", direction=direction)
        result = d.render_excalidraw()

        arrows = find_elements(result, elem_type="arrow")
        assert len(arrows) >= 1, f"No arrow found for direction {direction}"
        arrow = arrows[0]

        assert arrow.get("startArrowhead") == expected_start, (
            f"Direction {direction}: expected startArrowhead={expected_start}, "
            f"got {arrow.get('startArrowhead')}"
        )
        assert arrow.get("endArrowhead") == expected_end, (
            f"Direction {direction}: expected endArrowhead={expected_end}, "
            f"got {arrow.get('endArrowhead')}"
        )


def test_connector_styles():
    """ConnectorStyle maps to the correct Excalidraw strokeStyle."""
    cases = [
        (ConnectorStyle.SOLID, "solid"),
        (ConnectorStyle.DASHED, "dashed"),
        (ConnectorStyle.DOTTED, "dotted"),
    ]

    for style, expected_stroke_style in cases:
        d = Diagram()
        d.add("a", "A", shape=ShapeKind.RECT, row=0, col=0)
        d.add("b", "B", shape=ShapeKind.RECT, row=0, col=1)
        d.connect("a", "b", style=style)
        result = d.render_excalidraw()

        arrows = find_elements(result, elem_type="arrow")
        assert len(arrows) >= 1
        assert arrows[0]["strokeStyle"] == expected_stroke_style, (
            f"Style {style}: expected strokeStyle='{expected_stroke_style}', "
            f"got '{arrows[0]['strokeStyle']}'"
        )


def test_line_weights():
    """LineWeight maps to the correct Excalidraw strokeWidth."""
    cases = [
        (LineWeight.THIN, 1),
        (LineWeight.NORMAL, 2),
        (LineWeight.BOLD, 3),
    ]

    for weight, expected_width in cases:
        d = Diagram()
        d.add("a", "A", shape=ShapeKind.RECT, row=0, col=0)
        d.add("b", "B", shape=ShapeKind.RECT, row=0, col=1)
        d.connect("a", "b", line_weight=weight)
        result = d.render_excalidraw()

        arrows = find_elements(result, elem_type="arrow")
        assert len(arrows) >= 1
        assert arrows[0]["strokeWidth"] == expected_width, (
            f"Weight {weight}: expected strokeWidth={expected_width}, "
            f"got {arrows[0]['strokeWidth']}"
        )


def test_sections_render():
    """A section produces a dashed rectangle element and a text label element."""
    d = Diagram()
    d.add("a", "Alpha", shape=ShapeKind.RECT, row=0, col=0)
    d.add("b", "Beta", shape=ShapeKind.RECT, row=0, col=1)
    d.section("My Group", ["a", "b"])
    result = d.render_excalidraw()

    # Find rectangle elements that are not shape elements (section background)
    rects = find_elements(result, elem_type="rectangle")
    section_rects = [
        r for r in rects
        if r.get("strokeStyle") == "dashed" and not r["id"].startswith("exc_shape_")
    ]
    assert len(section_rects) >= 1, "No dashed rectangle found for section"

    # Find text elements that contain the section label
    texts = find_elements(result, elem_type="text")
    label_texts = [t for t in texts if t.get("text") == "My Group"]
    assert len(label_texts) >= 1, "No text element found with section label"


def test_deterministic_seeds():
    """Two renders of the same diagram produce identical seeds."""
    d = Diagram()
    d.add("a", "Hello", shape=ShapeKind.RECT, row=0, col=0)
    d.add("b", "World", shape=ShapeKind.RECT, row=0, col=1)
    d.connect("a", "b")

    result1 = d.render_excalidraw()
    result2 = d.render_excalidraw()

    seeds1 = [e.get("seed") for e in result1["elements"] if "seed" in e]
    seeds2 = [e.get("seed") for e in result2["elements"] if "seed" in e]

    assert len(seeds1) > 0, "No seeds found in elements"
    assert seeds1 == seeds2, "Seeds differ between renders"


def test_font_sizes_by_role():
    """TextRole maps to the correct Excalidraw fontSize."""
    expected_sizes = {
        TextRole.TITLE: 28,
        TextRole.SUBTITLE: 22,
        TextRole.BODY: 16,
        TextRole.CAPTION: 14,
    }

    for role, expected_size in expected_sizes.items():
        d = Diagram()
        d.add("item", "Text", shape=ShapeKind.RECT, role=role, row=0, col=0)
        result = d.render_excalidraw()

        text_elems = find_elements(result, elem_type="text", id_prefix="exc_text_item")
        assert len(text_elems) == 1, f"No text element found for role {role}"
        assert text_elems[0]["fontSize"] == expected_size, (
            f"Role {role}: expected fontSize={expected_size}, "
            f"got {text_elems[0]['fontSize']}"
        )


def test_save_excalidraw_file(tmp_path):
    """Diagram.save() with .excalidraw extension writes valid JSON."""
    path = str(tmp_path / "test.excalidraw")
    Diagram().add("s1", "Save Test", row=0, col=0).save(path)

    assert os.path.exists(path)
    with open(path) as f:
        data = json.load(f)

    assert data["type"] == "excalidraw"
    assert data["version"] == 2
    assert len(data["elements"]) > 0


def test_text_bound_to_shape():
    """For a RECT shape, a text element exists with containerId pointing to the shape."""
    d = Diagram()
    d.add("box", "Label Text", shape=ShapeKind.RECT, row=0, col=0)
    result = d.render_excalidraw()

    shape_elems = find_elements(result, id_prefix="exc_shape_box")
    assert len(shape_elems) == 1
    shape_id = shape_elems[0]["id"]

    text_elems = find_elements(result, elem_type="text", id_prefix="exc_text_box")
    assert len(text_elems) == 1
    assert text_elems[0]["containerId"] == shape_id, (
        f"Text containerId '{text_elems[0].get('containerId')}' does not match "
        f"shape id '{shape_id}'"
    )
