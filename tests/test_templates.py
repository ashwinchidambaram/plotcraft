"""Tests for the templates library."""

import json
from plotcraft import Pipeline, DecisionTree, Comparison, Cycle, FanOut, Architecture, Timeline


def _load(path):
    """Load excalidraw JSON from a save."""
    with open(path) as f:
        return json.load(f)


def test_pipeline_basic(tmp_path):
    out = tmp_path / "p.excalidraw"
    Pipeline("Test Pipeline") \
        .step("Start") \
        .step("Middle", emphasize=True) \
        .step("End") \
        .caption("Pipeline caption") \
        .save(str(out))
    data = _load(out)
    assert data["type"] == "excalidraw"
    assert len(data["elements"]) > 0


def test_pipeline_with_annotations(tmp_path):
    out = tmp_path / "p.excalidraw"
    Pipeline("Test") \
        .step("A", annotation="Note about A") \
        .step("B") \
        .save(str(out))
    data = _load(out)
    assert any(e.get("text") == "Note about A" for e in data["elements"] if e["type"] == "text")


def test_decision_tree(tmp_path):
    out = tmp_path / "d.excalidraw"
    DecisionTree("Pick a DB") \
        .question("Structured?") \
        .branch("Yes", "PostgreSQL", note="ACID") \
        .branch("No", "MongoDB", note="Flexible") \
        .save(str(out))
    data = _load(out)
    texts = [e.get("text", "") for e in data["elements"] if e["type"] == "text"]
    assert "Structured?" in texts or any("Structured" in t for t in texts)


def test_decision_tree_requires_question(tmp_path):
    out = tmp_path / "d.excalidraw"
    try:
        DecisionTree("Test").branch("Yes", "X").save(str(out))
        assert False, "Should require question"
    except ValueError as e:
        assert "question" in str(e).lower()


def test_comparison(tmp_path):
    out = tmp_path / "c.excalidraw"
    Comparison("A vs B") \
        .option("A", points=["Pro 1", "Pro 2"]) \
        .option("B", points=["Pro 3", "Pro 4"]) \
        .save(str(out))
    data = _load(out)
    assert len(data["elements"]) > 5


def test_cycle(tmp_path):
    out = tmp_path / "c.excalidraw"
    Cycle("Iterative loop") \
        .step("Observe") \
        .step("Think", emphasize=True) \
        .step("Act") \
        .feedback("repeat") \
        .save(str(out))
    data = _load(out)
    arrows = [e for e in data["elements"] if e["type"] == "arrow"]
    assert len(arrows) >= 3  # Observe→Think, Think→Act, Act→Observe


def test_fan_out(tmp_path):
    out = tmp_path / "f.excalidraw"
    FanOut("Events") \
        .source("Bus") \
        .target("A") \
        .target("B", emphasize=True) \
        .target("C") \
        .save(str(out))
    data = _load(out)
    arrows = [e for e in data["elements"] if e["type"] == "arrow"]
    assert len(arrows) >= 3


def test_fan_out_requires_source(tmp_path):
    out = tmp_path / "f.excalidraw"
    try:
        FanOut("Test").target("X").save(str(out))
        assert False, "Should require source"
    except ValueError:
        pass


def test_architecture(tmp_path):
    out = tmp_path / "a.excalidraw"
    Architecture("System") \
        .tier("Frontend", ["Browser"]) \
        .tier("Backend", ["API"]) \
        .tier("Data", ["DB"]) \
        .save(str(out))
    data = _load(out)
    texts = [e.get("text", "") for e in data["elements"] if e["type"] == "text"]
    assert any("Browser" in t for t in texts)
    assert any("API" in t for t in texts)
    assert any("DB" in t for t in texts)


def test_timeline(tmp_path):
    out = tmp_path / "t.excalidraw"
    Timeline("Roadmap") \
        .event("Q1", "Plan") \
        .event("Q2", "Build", emphasize=True) \
        .event("Q3", "Ship") \
        .save(str(out))
    data = _load(out)
    texts = [e.get("text", "") for e in data["elements"] if e["type"] == "text"]
    assert any("Q1" in t for t in texts)
    assert any("Q3" in t for t in texts)


def test_chaining_returns_self():
    """Templates use fluent builders — every method should return self."""
    p = Pipeline("X")
    assert p.step("a") is p
    assert p.caption("c") is p

    d = DecisionTree("X")
    assert d.question("?") is d
    assert d.branch("y", "z") is d
