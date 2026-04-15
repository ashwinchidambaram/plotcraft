"""Tests for the Scene API."""

from plotcraft import Scene


def test_add_and_connect():
    s = Scene()
    s.add("A", role="start")
    s.add("B", role="end")
    s.connect("A", "B")
    assert len(s._elements) == 2
    assert len(s._connections) == 1


def test_connect_by_text():
    s = Scene()
    s.add("Hello World", role="process")
    s.add("Goodbye", role="end")
    s.connect("Hello World", "Goodbye")
    assert s._connections[0].source_id == "hello_world"


def test_annotate():
    s = Scene()
    s.add("Target", role="process")
    s.annotate("A note", near="Target")
    assert len(s._annotations) == 1
    assert s._annotations[0].near_id == "target"


def test_chaining():
    s = Scene()
    result = s.add("A").add("B").connect("A", "B")
    assert result is s


def test_layout_stores_pattern():
    s = Scene()
    s.add("A", role="start")
    s.layout("cycle")
    assert s._layout_pattern == "cycle"


def test_to_d2_generates_markup():
    s = Scene()
    s.add("Start", role="start")
    s.add("End", role="end")
    s.connect("Start", "End")
    s.layout("pipeline")
    d2 = s.to_d2()
    assert "start:" in d2.lower() or "Start" in d2
    assert "->" in d2


def test_to_d2_direction_right_for_pipeline():
    s = Scene()
    s.add("A", role="start")
    s.layout("pipeline")
    d2 = s.to_d2()
    assert "direction: right" in d2


def test_to_d2_direction_down_for_top_down():
    s = Scene()
    s.add("A", role="start")
    s.layout("top_down")
    d2 = s.to_d2()
    assert "direction: down" in d2


def test_to_excalidraw_generates_json():
    s = Scene()
    s.add("A", role="start")
    s.add("B", role="end")
    s.connect("A", "B")
    s.layout("pipeline")
    data = s.to_excalidraw()
    assert data["type"] == "excalidraw"
    assert len(data["elements"]) > 0


def test_dark_theme():
    s = Scene(dark=True)
    s.add("A", role="start")
    s.layout("pipeline")
    data = s.to_excalidraw()
    assert data["appState"]["viewBackgroundColor"] == "#1A1A1A"


def test_emphasis_high():
    s = Scene()
    s.add("Important", role="process", emphasis="high")
    d2 = s.to_d2()
    assert "shadow: true" in d2


def test_save_excalidraw(tmp_path):
    import json
    path = str(tmp_path / "test.excalidraw")
    s = Scene()
    s.add("A", role="start")
    s.layout("pipeline")
    s.save(path)
    with open(path) as f:
        data = json.load(f)
    assert data["type"] == "excalidraw"


def test_save_d2_source(tmp_path):
    path = str(tmp_path / "test.d2")
    s = Scene()
    s.add("A", role="start")
    s.layout("pipeline")
    s.save(path)
    with open(path) as f:
        content = f.read()
    assert "shape: oval" in content


def test_theme_parameter():
    s = Scene(theme="ocean")
    assert s.theme == "ocean"


def test_unknown_element_raises():
    s = Scene()
    s.add("A", role="start")
    try:
        s.connect("A", "nonexistent")
        assert False, "Should have raised"
    except ValueError:
        pass


def test_topo_sort_orders_by_connections():
    s = Scene()
    s.add("C", role="end")
    s.add("A", role="start")
    s.add("B", role="process")
    s.connect("A", "B")
    s.connect("B", "C")
    flow = [e for e in s._elements.values() if e.role not in ("title", "caption")]
    ordered = s._topo_sort(flow)
    ids = [e.id for e in ordered]
    assert ids.index("a") < ids.index("b") < ids.index("c")
