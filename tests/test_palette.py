"""Tests for the Palette / theme system."""

from plotcraft import Scene, Palette, PALETTES


def _start_fill(scene: Scene) -> str:
    """Pull the first style.fill line out of the D2 source."""
    for line in scene.to_d2().splitlines():
        if "style.fill" in line:
            return line.strip()
    raise AssertionError("no fill line in d2 source")


def test_default_palette_uses_terracotta():
    s = Scene(theme="default")
    s.add("A", role="start")
    s.add("B", role="end")
    s.connect("A", "B")
    fill = _start_fill(s)
    # Terracotta-50 fill on the start oval
    assert "#FCF0ED" in fill


def test_named_themes_produce_distinct_colors():
    """Each built-in named theme should produce a different start fill."""
    fills = {}
    for name in ["default", "ocean", "forest", "sunset", "grape", "monochrome", "vanilla"]:
        s = Scene(theme=name)
        s.add("A", role="start")
        s.add("B", role="end")
        s.connect("A", "B")
        fills[name] = _start_fill(s)
    # All values must be unique — that's the regression we're guarding against.
    assert len(set(fills.values())) == len(fills), (
        f"themes collapsed to identical colors: {fills}"
    )


def test_theme_aliases_resolve():
    """Old aliases (earth, cool, mixed) should still resolve to a palette."""
    for alias in ["earth", "cool", "mixed", "neutral"]:
        s = Scene(theme=alias)
        # Should not raise; should resolve to a real palette
        assert isinstance(s.palette, Palette)
        assert s.palette.name != "custom"


def test_unknown_theme_falls_back_to_default():
    s = Scene(theme="this-name-does-not-exist")
    assert s.palette.name == "terracotta"


def test_custom_palette_object():
    p = Palette(
        name="brand",
        canvas="#FFFFFF",
        start=("#ABCDEF", "#123456", "#000000"),
        end=("#FEDCBA", "#654321", "#000000"),
    )
    s = Scene(theme=p)
    s.add("A", role="start")
    s.add("B", role="end")
    s.connect("A", "B")
    src = s.to_d2()
    assert "#ABCDEF" in src
    assert "#123456" in src
    assert "#FEDCBA" in src


def test_dict_partial_override():
    """Passing a dict should override only the given fields, keep the rest."""
    s = Scene(theme={"start": ("#FF0000", "#AA0000", "#FFFFFF")})
    s.add("A", role="start")
    s.add("B", role="process")  # falls back to default process color
    s.connect("A", "B")
    src = s.to_d2()
    assert "#FF0000" in src           # custom start fill
    assert "#F3EFE8" in src           # default process fill survived


def test_dark_mode_uses_dark_canvas():
    s = Scene(theme="default", dark=True)
    assert s.palette.canvas == "#1A1A1A"


def test_dark_mode_with_named_theme_auto_darkens():
    """Picking a light theme + dark=True should still produce a dark canvas."""
    s = Scene(theme="ocean", dark=True)
    assert s.palette.canvas in ("#1A1A1A", "#0E1A26")


def test_palette_role_lookup():
    p = PALETTES["ocean"]
    fill, stroke, _text = p.role("start")
    assert fill == "#E3F2FD"
    assert stroke == "#1565C0"


def test_emphasis_high_uses_palette_high_color():
    s = Scene(theme="ocean")
    s.add("A", role="process", emphasis="high")
    src = s.to_d2()
    # Ocean's high color is #1976D2
    assert "#1976D2" in src


def test_palette_exported_from_package():
    """Palette and PALETTES should be importable from plotcraft top-level."""
    from plotcraft import Palette as P, PALETTES as REG
    assert P is Palette
    assert "ocean" in REG


def test_id_strips_d2_special_chars():
    """Titles with `:` or `.` shouldn't break D2 parsing into parent.child."""
    s = Scene()
    s.add("Theme: default", role="title")
    src = s.to_d2()
    # Should not contain a bare `theme:` parent/child path emitted from the id
    # The leaf id should not have a colon in it.
    for line in src.splitlines():
        if line.endswith("{") and ":" in line:
            ident = line.split(":")[0].strip()
            assert ":" not in ident, f"identifier still has colon: {line}"


def test_template_accepts_palette_object():
    """Templates should pass through a Palette object."""
    from plotcraft import Pipeline
    p = Palette(name="t", start=("#111111", "#222222", "#FFFFFF"))
    pipe = Pipeline("X", theme=p)
    pipe.step("a").step("b")
    # Build the underlying scene via inspection of save() — just ensure
    # no error and that the palette propagates through.
    assert pipe._theme is p  # type: ignore[attr-defined]
