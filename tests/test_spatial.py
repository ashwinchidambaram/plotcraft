"""Tests for the Canvas spatial composition API."""

import json
from plotcraft import Canvas


def test_canvas_basic_save(tmp_path):
    c = Canvas(800, 600)
    c.title("Test Diagram")
    p = c.panel("(a)", "First panel")
    p.dot(0, 0, label="x")

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    assert out.exists()

    with open(out) as f:
        data = json.load(f)
    assert data["type"] == "excalidraw"
    assert len(data["elements"]) > 0


def test_canvas_panel_creation(tmp_path):
    c = Canvas()
    c.title("Title", subtitle="Subtitle", mapping="a = b")
    p1 = c.panel("(a)", "Panel A")
    p2 = c.panel("(b)", "Panel B")
    assert len(c._panels) == 2
    assert p1.cx < p2.cx  # panels arranged left to right


def test_canvas_circle_and_blob(tmp_path):
    c = Canvas()
    p = c.panel("(a)", "Test")
    p.circle(0, 0, 10, fill="#FF0000", stroke="#990000")
    p.blob(20, 20)

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    with open(out) as f:
        data = json.load(f)
    ellipses = [e for e in data["elements"] if e["type"] == "ellipse"]
    assert len(ellipses) >= 6  # circle + blob (5 ellipses by default) + dish


def test_canvas_vein_creates_line(tmp_path):
    c = Canvas()
    p = c.panel("(a)", "Test")
    p.vein(-30, -30, 30, 30, width=3, color="#FF0000")

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    with open(out) as f:
        data = json.load(f)
    lines = [e for e in data["elements"] if e["type"] == "line"]
    assert len(lines) >= 1


def test_canvas_arrow_between_panels(tmp_path):
    c = Canvas()
    p1 = c.panel("(a)", "A")
    p2 = c.panel("(b)", "B")
    c.arrow_between(p1, p2, label="next")

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    with open(out) as f:
        data = json.load(f)
    arrows = [e for e in data["elements"] if e["type"] == "arrow"]
    assert len(arrows) >= 1


def test_canvas_legend(tmp_path):
    c = Canvas()
    c.title("Title")
    c.panel("(a)", "A")
    c.legend([("Item 1", "#FF0000", "#990000"), ("Item 2", "#00FF00", "#009900")])

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    with open(out) as f:
        data = json.load(f)
    texts = [e for e in data["elements"] if e["type"] == "text"]
    assert any(e.get("text") == "Item 1" for e in texts)


def test_canvas_to_excalidraw_dict():
    c = Canvas()
    c.title("Test")
    p = c.panel("(a)", "Test")
    p.dot(0, 0)

    data = c.to_excalidraw()
    assert data["type"] == "excalidraw"
    assert data["version"] == 2
    assert "elements" in data


def test_canvas_branch_creates_lines(tmp_path):
    import math
    c = Canvas()
    p = c.panel("(a)", "Test")
    p.branch(angle=0, length=50, width=3)

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    with open(out) as f:
        data = json.load(f)
    lines = [e for e in data["elements"] if e["type"] == "line"]
    # branch creates at least a main vein, possibly sub-branches
    assert len(lines) >= 1


def test_canvas_footer(tmp_path):
    c = Canvas()
    c.title("Title")
    c.panel("(a)", "A")
    c.footer("This is the footer")

    out = tmp_path / "test.excalidraw"
    c.save(str(out))
    with open(out) as f:
        data = json.load(f)
    texts = [e for e in data["elements"] if e["type"] == "text"]
    assert any(e.get("text") == "This is the footer" for e in texts)
