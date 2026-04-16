"""Freeform Scene API for PlotCraft.

High-level declarative API where the LLM describes WHAT (elements + connections)
and the layout engine decides WHERE (pixel positions, sizes, whitespace).

Outputs Excalidraw JSON directly — no grid, no intermediate model.
"""
from __future__ import annotations

import json
import math
import zlib
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

_CANVAS_LIGHT = "#F9F7F4"
_CANVAS_DARK = "#1A1A1A"

# Triple = (fill, stroke, text_color). fill may be None for text-only roles.
RoleColors = tuple[str | None, str, str]


@dataclass
class Palette:
    """Color palette controlling every visual element in a Scene.

    Each role gets a (fill, stroke, text) triple. Text-only roles (title,
    subtitle, caption, annotation) only use the text color.

    Use a built-in palette by name (e.g. ``Scene(theme="ocean")``) or build
    your own::

        from plotcraft import Scene, Palette

        custom = Palette(
            name="brand",
            canvas="#FFFFFF",
            start=("#E3F2FD", "#1565C0", "#0D47A1"),
            end=("#E8F5E9", "#2E7D32", "#1B5E20"),
            process=("#F5F5F5", "#616161", "#212121"),
            decision=("#FFF3E0", "#E65100", "#BF360C"),
            high=("#FFB300", "#E65100", "#FFFFFF"),
        )
        Scene(theme=custom)
    """

    name: str = "custom"
    canvas: str = "#F9F7F4"

    # Text-only role colors
    title_color: str = "#2C2C2C"
    subtitle_color: str = "#D4745E"
    caption_color: str = "#757575"
    annotation_color: str = "#757575"

    # Shape role triples (fill, stroke, text)
    start: RoleColors = ("#FCF0ED", "#A84F3B", "#2C2C2C")
    end: RoleColors = ("#E3E8DF", "#485240", "#2C2C2C")
    process: RoleColors = ("#F3EFE8", "#757575", "#2C2C2C")
    decision: RoleColors = ("#FDF8F0", "#5E422A", "#2C2C2C")

    # Emphasis variants
    high: RoleColors = ("#D4745E", "#853D2D", "#E8DCC4")
    low: RoleColors = ("#F3EFE8", "#B0B0A8", "#999999")

    def role(self, name: str) -> RoleColors:
        """Resolve a role to its (fill, stroke, text) triple."""
        if name == "title":
            return (None, "transparent", self.title_color)
        if name == "subtitle":
            return (None, "transparent", self.subtitle_color)
        if name == "caption":
            return (None, "transparent", self.caption_color)
        if name == "annotation":
            return (None, "transparent", self.annotation_color)
        if name == "start":
            return self.start
        if name == "end":
            return self.end
        if name == "decision":
            return self.decision
        if name == "high":
            return self.high
        if name == "low":
            return self.low
        return self.process


# ---------------------------------------------------------------------------
# Built-in palettes
# ---------------------------------------------------------------------------

# Default warm-earth aesthetic (terracotta/sage/sand).
_TERRACOTTA = Palette(
    name="terracotta",
    canvas="#F9F7F4",
    title_color="#2C2C2C",
    subtitle_color="#D4745E",
    caption_color="#757575",
    annotation_color="#757575",
    start=("#FCF0ED", "#A84F3B", "#2C2C2C"),
    end=("#E3E8DF", "#485240", "#2C2C2C"),
    process=("#F3EFE8", "#757575", "#2C2C2C"),
    decision=("#FDF8F0", "#5E422A", "#2C2C2C"),
    high=("#D4745E", "#853D2D", "#FFFFFF"),
    low=("#F3EFE8", "#B0B0A8", "#999999"),
)

# Cool blues, calm and technical.
_OCEAN = Palette(
    name="ocean",
    canvas="#F4F7FA",
    title_color="#0F2A40",
    subtitle_color="#1565C0",
    caption_color="#5A6F80",
    annotation_color="#5A6F80",
    start=("#E3F2FD", "#1565C0", "#0D2C4A"),
    end=("#E0F7F4", "#00796B", "#003D34"),
    process=("#ECEFF4", "#5A6F80", "#1B2733"),
    decision=("#FFF8E1", "#F9A825", "#5C3A00"),
    high=("#1976D2", "#0D47A1", "#FFFFFF"),
    low=("#ECEFF4", "#B0BEC5", "#90A4AE"),
)

# Verdant greens with yellow-orange accents — natural, organic.
_FOREST = Palette(
    name="forest",
    canvas="#F6F8F2",
    title_color="#1B3A1B",
    subtitle_color="#2E7D32",
    caption_color="#5D6E5A",
    annotation_color="#5D6E5A",
    start=("#E8F5E9", "#2E7D32", "#1B3A1B"),
    end=("#FFF8E1", "#9C7A1F", "#4F3A06"),
    process=("#EEF1E8", "#5D6E5A", "#1F2E1F"),
    decision=("#FFEFC2", "#C77800", "#5C3A00"),
    high=("#388E3C", "#1B5E20", "#FFFFFF"),
    low=("#EEF1E8", "#BDBDBD", "#9E9E9E"),
)

# Warm orange/red/yellow — energetic, bold.
_SUNSET = Palette(
    name="sunset",
    canvas="#FFF8F2",
    title_color="#3E1F0E",
    subtitle_color="#E64A19",
    caption_color="#8C5A4A",
    annotation_color="#8C5A4A",
    start=("#FFE0B2", "#EF6C00", "#3E1F0E"),
    end=("#FCE4EC", "#AD1457", "#4A0F2C"),
    process=("#FFF3E0", "#8C5A4A", "#3E1F0E"),
    decision=("#FFF9C4", "#F57F17", "#4A3500"),
    high=("#E64A19", "#BF360C", "#FFFFFF"),
    low=("#FFF3E0", "#D7CCC8", "#A1887F"),
)

# Purple/pink palette — playful, creative.
_GRAPE = Palette(
    name="grape",
    canvas="#FAF5FC",
    title_color="#311B45",
    subtitle_color="#7B1FA2",
    caption_color="#7A6A85",
    annotation_color="#7A6A85",
    start=("#F3E5F5", "#7B1FA2", "#311B45"),
    end=("#E1F5FE", "#0277BD", "#0D2C4A"),
    process=("#F3EBF7", "#7A6A85", "#2C1F3D"),
    decision=("#FFF8E1", "#C77800", "#5C3A00"),
    high=("#9C27B0", "#4A148C", "#FFFFFF"),
    low=("#F3EBF7", "#CFC2D9", "#9E8FAB"),
)

# All-grayscale, minimal, editorial.
_MONOCHROME = Palette(
    name="monochrome",
    canvas="#FAFAFA",
    title_color="#1A1A1A",
    subtitle_color="#424242",
    caption_color="#757575",
    annotation_color="#757575",
    start=("#FFFFFF", "#1A1A1A", "#1A1A1A"),
    end=("#E0E0E0", "#424242", "#1A1A1A"),
    process=("#F5F5F5", "#757575", "#1A1A1A"),
    decision=("#EEEEEE", "#212121", "#1A1A1A"),
    high=("#212121", "#000000", "#FFFFFF"),
    low=("#F5F5F5", "#BDBDBD", "#9E9E9E"),
)

# Soft pastels, gentle and approachable.
_PASTEL = Palette(
    name="pastel",
    canvas="#FDFBF7",
    title_color="#3A3A3A",
    subtitle_color="#A66E92",
    caption_color="#8C8377",
    annotation_color="#8C8377",
    start=("#FCE4EC", "#C2185B", "#3A1F2E"),
    end=("#C8E6C9", "#388E3C", "#1F3A22"),
    process=("#FFF3E0", "#8C8377", "#3A3A3A"),
    decision=("#E1F5FE", "#0288D1", "#0D2C4A"),
    high=("#FFB74D", "#F57C00", "#3E1F0E"),
    low=("#FFF3E0", "#D7CCC8", "#A1887F"),
)

# Vanilla / cream — soft warm neutrals.
_VANILLA = Palette(
    name="vanilla",
    canvas="#FFFBF0",
    title_color="#3E2C1B",
    subtitle_color="#8C6A3F",
    caption_color="#8C7A5A",
    annotation_color="#8C7A5A",
    start=("#FFF3D9", "#B8893E", "#3E2C1B"),
    end=("#F0E8D8", "#5C4A2E", "#1F1A0E"),
    process=("#FAF3E0", "#8C7A5A", "#3E2C1B"),
    decision=("#FFE9B3", "#9C7A1F", "#4F3A06"),
    high=("#D49E2C", "#8C5E0E", "#FFFFFF"),
    low=("#FAF3E0", "#D4C8B0", "#A89878"),
)

# Dark variant of terracotta, used when dark=True with no theme set.
_TERRACOTTA_DARK = Palette(
    name="terracotta-dark",
    canvas="#1A1A1A",
    title_color="#E8DCC4",
    subtitle_color="#D4745E",
    caption_color="#8B8B8B",
    annotation_color="#8B8B8B",
    start=("#3D1F17", "#D4745E", "#E8DCC4"),
    end=("#1E2B1E", "#8B9D83", "#E8DCC4"),
    process=("#2C2C2C", "#8B8B8B", "#E8DCC4"),
    decision=("#2E2214", "#D4A574", "#E8DCC4"),
    high=("#853D2D", "#D4745E", "#E8DCC4"),
    low=("#1A1A1A", "#555555", "#666666"),
)

# Dark variant of ocean.
_OCEAN_DARK = Palette(
    name="ocean-dark",
    canvas="#0E1A26",
    title_color="#E0F2FF",
    subtitle_color="#64B5F6",
    caption_color="#7A8C9C",
    annotation_color="#7A8C9C",
    start=("#0D2C4A", "#64B5F6", "#E0F2FF"),
    end=("#003D34", "#4DB6AC", "#E0F2FF"),
    process=("#1B2733", "#7A8C9C", "#E0F2FF"),
    decision=("#3E2C00", "#FFB300", "#FFE082"),
    high=("#1565C0", "#64B5F6", "#FFFFFF"),
    low=("#1B2733", "#37474F", "#546E7A"),
)

# Registry — keys are case-insensitive.
PALETTES: dict[str, Palette] = {
    "default":     _TERRACOTTA,
    "terracotta":  _TERRACOTTA,
    "ocean":       _OCEAN,
    "forest":      _FOREST,
    "sunset":      _SUNSET,
    "grape":       _GRAPE,
    "monochrome":  _MONOCHROME,
    "mono":        _MONOCHROME,
    "pastel":      _PASTEL,
    "vanilla":     _VANILLA,
    # Aliases for back-compat with the old (mostly-broken) D2 theme names.
    "earth":       _FOREST,
    "cool":        _OCEAN,
    "mixed":       _GRAPE,
    "neutral":     _MONOCHROME,
    # Dark variants (used when dark=True)
    "dark":               _TERRACOTTA_DARK,
    "terracotta-dark":    _TERRACOTTA_DARK,
    "ocean-dark":         _OCEAN_DARK,
}


def _resolve_palette(theme: str | Palette | dict | None, dark: bool) -> Palette:
    """Turn whatever the user passed into a concrete Palette."""
    # Custom Palette object passed directly.
    if isinstance(theme, Palette):
        return theme

    # Dict — treat as a partial override on top of the default light/dark base.
    if isinstance(theme, dict):
        base = _TERRACOTTA_DARK if dark else _TERRACOTTA
        # dataclasses.replace would require importing replace; build manually
        # to allow nested triples to be partially overridden later if needed.
        from dataclasses import replace
        return replace(base, **{k: v for k, v in theme.items() if hasattr(base, k)})

    # String name (or None → default).
    name = (theme or "default").lower()
    if dark:
        # Look for a dark variant first, fall back to the named palette,
        # then fall back to the dark default.
        if f"{name}-dark" in PALETTES:
            return PALETTES[f"{name}-dark"]
        if name in PALETTES:
            base = PALETTES[name]
            # Auto-darken: swap canvas + text colors for a quick dark variant
            # of any light palette the user picked. For best results add an
            # explicit "<name>-dark" entry above.
            return _auto_darken(base)
        return _TERRACOTTA_DARK

    return PALETTES.get(name, _TERRACOTTA)


def _auto_darken(p: Palette) -> Palette:
    """Best-effort dark-mode version of a light palette.

    Inverts the canvas, swaps fills→strokes and lightens text. Not as good
    as a hand-tuned dark palette, but lets every named theme work in dark
    mode without duplicating every entry.
    """
    from dataclasses import replace

    def darken(triple: RoleColors) -> RoleColors:
        fill, stroke, _text = triple
        # Use the light stroke as the dark fill base, and the light fill
        # (often pale) as the dark stroke (it'll read as a soft outline).
        new_fill = stroke if stroke != "transparent" else "#2C2C2C"
        new_stroke = fill or "#8B8B8B"
        return (new_fill, new_stroke, "#F5F0E6")

    return replace(
        p,
        name=f"{p.name}-dark",
        canvas="#1A1A1A",
        title_color="#F5F0E6",
        subtitle_color=p.subtitle_color,
        caption_color="#8B8B8B",
        annotation_color="#8B8B8B",
        start=darken(p.start),
        end=darken(p.end),
        process=darken(p.process),
        decision=darken(p.decision),
        high=(p.high[1], p.high[0] or "#FFFFFF", "#FFFFFF"),
        low=("#1A1A1A", "#555555", "#666666"),
    )

# Role → Excalidraw shape type
_ROLE_SHAPE: dict[str, str] = {
    "title":      "text",
    "subtitle":   "text",
    "start":      "ellipse",
    "end":        "ellipse",
    "process":    "rectangle",
    "decision":   "diamond",
    "annotation": "text",
    "caption":    "text",
}

# (width, height) defaults per (role, size)
_ELEMENT_DIMS: dict[tuple[str, str], tuple[float, float]] = {
    # Titles / text
    ("title", "small"):     (300, 45),
    ("title", "medium"):    (450, 55),
    ("title", "large"):     (550, 65),
    ("subtitle", "small"):  (200, 35),
    ("subtitle", "medium"): (350, 42),
    ("subtitle", "large"):  (450, 50),
    ("caption", "small"):   (300, 25),
    ("caption", "medium"):  (450, 30),
    ("caption", "large"):   (550, 35),
    # Shapes
    ("start", "small"):     (120, 55),
    ("start", "medium"):    (150, 65),
    ("start", "large"):     (190, 80),
    ("end", "small"):       (120, 55),
    ("end", "medium"):      (150, 65),
    ("end", "large"):       (190, 80),
    ("process", "small"):   (140, 60),
    ("process", "medium"):  (180, 80),
    ("process", "large"):   (230, 95),
    ("process", "hero"):    (280, 110),
    ("decision", "small"):  (120, 120),
    ("decision", "medium"): (150, 150),
    ("decision", "large"):  (180, 180),
    ("annotation", "small"):  (120, 35),
    ("annotation", "medium"): (160, 45),
    ("annotation", "large"):  (200, 55),
}

# Font sizes per role
_ROLE_FONT: dict[str, tuple[int, str]] = {
    # role: (fontSize, textAlign)
    "title":      (32, "center"),
    "subtitle":   (22, "center"),
    "start":      (18, "center"),
    "end":        (18, "center"),
    "process":    (16, "center"),
    "decision":   (16, "center"),
    "annotation": (14, "left"),
    "caption":    (14, "center"),
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Element:
    id: str
    text: str
    role: str = "process"
    size: str = "medium"
    emphasis: str = "normal"
    # Computed by layout:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


@dataclass
class Connection:
    source_id: str
    target_id: str
    label: str | None = None
    style: str = "solid"     # solid, dashed, dotted
    weight: str = "normal"   # thin, normal, bold


@dataclass
class Annotation:
    id: str
    text: str
    near_id: str
    position: str = "right"  # left, right, above, below
    # Computed by layout:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------

class Scene:
    """Freeform diagram scene with auto-layout.

    Usage:
        s = Scene()
        s.add("Start here", role="start")
        s.add("Do work", role="process", size="large")
        s.add("Done", role="end")
        s.connect("Start here", "Do work")
        s.connect("Do work", "Done")
        s.layout("pipeline")
        s.save("output.excalidraw")
    """

    # Names of built-in palettes; keep here for autocomplete / discoverability.
    AVAILABLE_THEMES = tuple(sorted(PALETTES.keys()))

    def __init__(
        self,
        width: float = 1200,
        height: float = 800,
        dark: bool = False,
        theme: "str | Palette | dict | None" = "default",
    ):
        """Create a Scene.

        Args:
            width, height: canvas size in pixels (Excalidraw output only;
                D2 output ignores these and auto-sizes).
            dark: switch to a dark canvas + inverted text.
            theme: a built-in palette name (see ``Scene.AVAILABLE_THEMES``),
                a :class:`Palette` object, or a dict of overrides on the
                default palette.
        """
        self.width = width
        self.height = height
        self.dark = dark
        # Keep the original arg around for repr/debugging; the resolved
        # Palette instance is what the renderer reads from.
        self.theme = theme if isinstance(theme, str) else (
            theme.name if isinstance(theme, Palette) else "custom"
        )
        self.palette: Palette = _resolve_palette(theme, dark)
        self._elements: dict[str, Element] = {}
        self._connections: list[Connection] = []
        self._annotations: list[Annotation] = []
        self._order: list[str] = []  # insertion order for IDs
        self._id_counter = 0

    def _auto_id(self, text: str) -> str:
        """Generate a stable ID from text."""
        # D2 treats `:`, `.`, `(`, `)`, `{`, `}` as syntax — strip them so the
        # generated id is a single leaf node, not a parent.child path.
        import re
        clean = text.lower().replace(" ", "_").replace("\n", "_")
        clean = re.sub(r"[^a-z0-9_]", "", clean)
        # Truncate and ensure uniqueness
        base = clean[:30] or "elem"
        if base not in self._elements:
            return base
        self._id_counter += 1
        return f"{base}_{self._id_counter}"

    def add(
        self,
        text: str,
        id: str | None = None,
        role: str = "process",
        size: str = "medium",
        emphasis: str = "normal",
    ) -> Scene:
        """Add an element to the scene. Returns self for chaining."""
        eid = id or self._auto_id(text)
        dims = _ELEMENT_DIMS.get((role, size), _ELEMENT_DIMS.get((role, "medium"), (170, 75)))
        elem = Element(
            id=eid, text=text, role=role, size=size, emphasis=emphasis,
            width=dims[0], height=dims[1],
        )
        self._elements[eid] = elem
        self._order.append(eid)
        return self

    def connect(
        self,
        source: str,
        target: str,
        label: str | None = None,
        style: str = "solid",
        weight: str = "normal",
    ) -> Scene:
        """Connect two elements. Source/target can be IDs or text (auto-resolved)."""
        src = self._resolve_id(source)
        tgt = self._resolve_id(target)
        self._connections.append(Connection(src, tgt, label, style, weight))
        return self

    def annotate(
        self,
        text: str,
        near: str,
        position: str = "right",
    ) -> Scene:
        """Add an annotation near an element."""
        near_id = self._resolve_id(near)
        ann_id = f"ann_{near_id}_{len(self._annotations)}"
        self._annotations.append(Annotation(
            id=ann_id, text=text, near_id=near_id, position=position,
            width=160, height=45,
        ))
        return self

    def _resolve_id(self, ref: str) -> str:
        """Resolve a reference to an element ID (by ID or by text)."""
        if ref in self._elements:
            return ref
        # Search by text
        for eid, elem in self._elements.items():
            if elem.text == ref:
                return eid
        raise ValueError(f"No element found with id or text: '{ref}'")

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def layout(self, pattern: str = "pipeline") -> Scene:
        """Compute positions for all elements based on the pattern."""
        self._layout_pattern = pattern
        # Separate by role
        titles = [e for e in self._elements.values() if e.role == "title"]
        subtitles = [e for e in self._elements.values() if e.role == "subtitle"]
        captions = [e for e in self._elements.values() if e.role == "caption"]
        flow = [e for e in self._elements.values()
                if e.role not in ("title", "subtitle", "caption", "annotation")]

        # Place titles at top
        y_cursor = 40.0
        for t in titles:
            t.x = (self.width - t.width) / 2
            t.y = y_cursor
            y_cursor += t.height + 20

        for st in subtitles:
            st.x = (self.width - st.width) / 2
            st.y = y_cursor
            y_cursor += st.height + 15

        # Available area for flow
        flow_top = y_cursor + 30
        caption_space = 60 if captions else 0
        flow_bottom = self.height - caption_space - 30

        # Layout the flow elements
        if pattern == "pipeline":
            self._layout_pipeline(flow, flow_top, flow_bottom)
        elif pattern == "fan_out":
            self._layout_fan_out(flow, flow_top, flow_bottom)
        elif pattern == "convergence":
            self._layout_convergence(flow, flow_top, flow_bottom)
        elif pattern == "cycle":
            self._layout_cycle(flow, flow_top, flow_bottom)
        elif pattern == "decision_tree":
            self._layout_decision_tree(flow, flow_top, flow_bottom)
        elif pattern == "top_down":
            self._layout_top_down(flow, flow_top, flow_bottom)
        else:
            self._layout_pipeline(flow, flow_top, flow_bottom)

        # Place captions at bottom
        y_cursor = self.height - caption_space
        for c in captions:
            c.x = (self.width - c.width) / 2
            c.y = y_cursor
            y_cursor += c.height + 10

        # Place annotations near their targets
        self._layout_annotations()

        return self

    def _layout_pipeline(self, elements: list[Element], top: float, bottom: float):
        """Horizontal left-to-right flow."""
        if not elements:
            return

        # Order by connections if possible
        ordered = self._topo_sort(elements)
        gap = 80.0
        total_w = sum(e.width for e in ordered) + gap * (len(ordered) - 1)

        # Center horizontally
        start_x = max(60, (self.width - total_w) / 2)
        center_y = (top + bottom) / 2

        x = start_x
        for elem in ordered:
            elem.x = x
            elem.y = center_y - elem.height / 2
            x += elem.width + gap

    def _layout_fan_out(self, elements: list[Element], top: float, bottom: float):
        """One source at top, targets spread below."""
        if not elements:
            return

        # Find the source (most outgoing connections, or first "start" role)
        sources = [e for e in elements if e.role == "start"]
        if not sources:
            sources = [elements[0]]
        source = sources[0]
        targets = [e for e in elements if e.id != source.id]

        # Source centered at top of flow area
        source.x = (self.width - source.width) / 2
        source.y = top + 20

        # Targets spread horizontally below
        if targets:
            gap = 60.0
            total_w = sum(e.width for e in targets) + gap * (len(targets) - 1)
            start_x = max(60, (self.width - total_w) / 2)
            target_y = source.y + source.height + 120

            x = start_x
            for t in targets:
                t.x = x
                t.y = target_y
                x += t.width + gap

    def _layout_convergence(self, elements: list[Element], top: float, bottom: float):
        """Multiple inputs at top, one output at bottom."""
        if not elements:
            return

        # Find the target (most incoming connections, or first "end" role)
        ends = [e for e in elements if e.role == "end"]
        if not ends:
            ends = [elements[-1]]
        target = ends[0]
        inputs = [e for e in elements if e.id != target.id]

        # Inputs spread horizontally at top
        if inputs:
            gap = 60.0
            total_w = sum(e.width for e in inputs) + gap * (len(inputs) - 1)
            start_x = max(60, (self.width - total_w) / 2)
            x = start_x
            for inp in inputs:
                inp.x = x
                inp.y = top + 20
                x += inp.width + gap

        # Target centered below
        input_bottom = max((e.y + e.height) for e in inputs) if inputs else top + 100
        target.x = (self.width - target.width) / 2
        target.y = input_bottom + 120

    def _layout_cycle(self, elements: list[Element], top: float, bottom: float):
        """Triangular/rectangular arrangement for iterative loops.

        For 3 elements: triangle with first at top, second at bottom-right,
        third at bottom-left. This avoids the cramped circular layout and
        gives each element generous whitespace.
        """
        if not elements:
            return

        ordered = self._topo_sort(elements)
        n = len(ordered)
        if n <= 2:
            return self._layout_pipeline(elements, top, bottom)

        cx = self.width / 2
        cy = (top + bottom) / 2
        spread_x = min(280, (self.width - 300) / 2)
        spread_y = min(180, (bottom - top - 150) / 2)

        if n == 3:
            # Triangle: top-center, bottom-right, bottom-left
            ordered[0].x = cx - ordered[0].width / 2
            ordered[0].y = top + 20
            ordered[1].x = cx + spread_x - ordered[1].width / 2
            ordered[1].y = cy + spread_y / 2
            ordered[2].x = cx - spread_x - ordered[2].width / 2
            ordered[2].y = cy + spread_y / 2
        elif n == 4:
            # Rectangle: top-left, top-right, bottom-right, bottom-left
            ordered[0].x = cx - spread_x - ordered[0].width / 2
            ordered[0].y = top + 20
            ordered[1].x = cx + spread_x - ordered[1].width / 2
            ordered[1].y = top + 20
            ordered[2].x = cx + spread_x - ordered[2].width / 2
            ordered[2].y = cy + spread_y
            ordered[3].x = cx - spread_x - ordered[3].width / 2
            ordered[3].y = cy + spread_y
        else:
            # Fallback: oval arrangement with more generous spacing
            rx = min(350, (self.width - 250) / 2)
            ry = min(220, (bottom - top - 120) / 2)
            for i, elem in enumerate(ordered):
                angle = -math.pi / 2 + (2 * math.pi * i / n)
                elem.x = cx + rx * math.cos(angle) - elem.width / 2
                elem.y = cy + ry * math.sin(angle) - elem.height / 2

    def _layout_decision_tree(self, elements: list[Element], top: float, bottom: float):
        """Top-down branching."""
        if not elements:
            return

        # Find root (decision or first element)
        roots = [e for e in elements if e.role == "decision"]
        if not roots:
            roots = [elements[0]]
        root = roots[0]
        children = [e for e in elements if e.id != root.id]

        # Root centered at top
        root.x = (self.width - root.width) / 2
        root.y = top + 20

        # Children spread below
        if children:
            gap = 80.0
            total_w = sum(e.width for e in children) + gap * (len(children) - 1)
            start_x = max(60, (self.width - total_w) / 2)
            child_y = root.y + root.height + 100

            x = start_x
            for c in children:
                c.x = x
                c.y = child_y
                x += c.width + gap

    def _layout_top_down(self, elements: list[Element], top: float, bottom: float):
        """Vertical top-to-bottom flow."""
        if not elements:
            return

        ordered = self._topo_sort(elements)
        gap = 60.0
        total_h = sum(e.height for e in ordered) + gap * (len(ordered) - 1)

        start_y = max(top + 20, (top + bottom - total_h) / 2)
        cx = self.width / 2

        y = start_y
        for elem in ordered:
            elem.x = cx - elem.width / 2
            elem.y = y
            y += elem.height + gap

    def _layout_annotations(self):
        """Position annotations near their target elements."""
        for ann in self._annotations:
            target = self._elements.get(ann.near_id)
            if not target:
                continue

            gap = 20.0
            if ann.position == "right":
                ann.x = target.x + target.width + gap
                ann.y = target.y + (target.height - ann.height) / 2
            elif ann.position == "left":
                ann.x = target.x - ann.width - gap
                ann.y = target.y + (target.height - ann.height) / 2
            elif ann.position == "above":
                ann.x = target.x + (target.width - ann.width) / 2
                ann.y = target.y - ann.height - gap
            elif ann.position == "below":
                ann.x = target.x + (target.width - ann.width) / 2
                ann.y = target.y + target.height + gap

    def _topo_sort(self, elements: list[Element]) -> list[Element]:
        """Sort elements by connection order (topological sort)."""
        ids = {e.id for e in elements}
        elem_map = {e.id: e for e in elements}

        # Build adjacency from connections that involve these elements
        adj: dict[str, list[str]] = {eid: [] for eid in ids}
        in_deg: dict[str, int] = {eid: 0 for eid in ids}
        for conn in self._connections:
            if conn.source_id in ids and conn.target_id in ids:
                adj[conn.source_id].append(conn.target_id)
                in_deg[conn.target_id] += 1

        # Kahn's algorithm
        queue = [eid for eid in ids if in_deg[eid] == 0]
        # Stable sort: prefer insertion order
        order_idx = {eid: i for i, eid in enumerate(self._order) if eid in ids}
        queue.sort(key=lambda e: order_idx.get(e, 999))

        result: list[str] = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in adj[node]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)
            queue.sort(key=lambda e: order_idx.get(e, 999))

        # Add any remaining (cycles)
        for eid in self._order:
            if eid in ids and eid not in result:
                result.append(eid)

        return [elem_map[eid] for eid in result if eid in elem_map]

    # ------------------------------------------------------------------
    # Excalidraw generation
    # ------------------------------------------------------------------

    def to_excalidraw(self) -> dict:
        """Generate complete Excalidraw JSON document."""
        elements: list[dict] = []

        # Shapes and text
        for elem in self._elements.values():
            shape_type = _ROLE_SHAPE.get(elem.role, "rectangle")
            colors = self._get_colors(elem)

            if shape_type == "text":
                # Free-floating text (title, subtitle, caption, annotation)
                elements.append(self._make_text(
                    elem.id, elem.text, elem.x, elem.y, elem.width, elem.height,
                    color=colors[2], font_size=_ROLE_FONT.get(elem.role, (16, "center"))[0],
                    align=_ROLE_FONT.get(elem.role, (16, "center"))[1],
                ))
            else:
                # Shape with bound text
                # For bound text, Excalidraw auto-centers when containerId is set.
                # We set text x/y/w/h to match the container — Excalidraw overrides
                # the position based on textAlign + verticalAlign.
                text_id = f"{elem.id}_text"
                font_size = _ROLE_FONT.get(elem.role, (16, "center"))[0]
                # Estimate text height for Excalidraw (lineHeight * fontSize * numLines)
                num_lines = elem.text.count("\n") + 1
                text_h = font_size * 1.25 * num_lines
                shape = self._make_shape(
                    elem.id, shape_type, elem.x, elem.y, elem.width, elem.height,
                    fill=colors[0], stroke=colors[1],
                    bound_text_id=text_id,
                )
                elements.append(shape)
                elements.append(self._make_text(
                    text_id, elem.text,
                    elem.x + elem.width / 2 - 50,  # rough center, Excalidraw overrides
                    elem.y + (elem.height - text_h) / 2,
                    100, text_h,
                    color=colors[2],
                    font_size=font_size,
                    align="center",
                    container_id=elem.id,
                    v_align="middle",
                ))

        # Annotations
        for ann in self._annotations:
            elements.append(self._make_text(
                ann.id, ann.text, ann.x, ann.y, ann.width, ann.height,
                color=self.palette.annotation_color,
                font_size=14, align="left",
            ))

        # Arrows
        for conn in self._connections:
            src = self._elements.get(conn.source_id)
            tgt = self._elements.get(conn.target_id)
            if not src or not tgt:
                continue

            arrow_elems = self._make_arrow(conn, src, tgt)
            elements.extend(arrow_elems)

        return {
            "type": "excalidraw",
            "version": 2,
            "source": "plotcraft",
            "elements": elements,
            "appState": {
                "viewBackgroundColor": _CANVAS_DARK if self.dark else _CANVAS_LIGHT,
                "gridSize": None,
            },
            "files": {},
        }

    def save(self, path: str, engine: str = "auto") -> None:
        """Save diagram to file.

        Args:
            path: Output file path. Extension determines format:
                  .excalidraw → Excalidraw JSON
                  .svg → SVG (uses D2 if engine="d2" or "auto")
                  .png → PNG (uses D2 if engine="d2" or "auto")
                  .d2 → D2 source markup
            engine: "excalidraw", "d2", or "auto" (default).
                    "auto" uses D2 for .svg/.png, Excalidraw for .excalidraw.
        """
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""

        if ext == "excalidraw":
            data = self.to_excalidraw()
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        elif ext == "d2":
            with open(path, "w") as f:
                f.write(self.to_d2())
        elif ext in ("svg", "png"):
            use_d2 = engine in ("d2", "auto")
            if use_d2:
                self._render_d2(path, ext)
            else:
                # Use bundled Excalidraw renderer (requires plotcraft[render])
                exc_path = path.rsplit(".", 1)[0] + ".excalidraw"
                data = self.to_excalidraw()
                with open(exc_path, "w") as f:
                    json.dump(data, f, indent=2)
                from plotcraft.render import render_excalidraw_to_png, render_excalidraw_to_svg
                if ext == "png":
                    render_excalidraw_to_png(exc_path, path)
                else:
                    render_excalidraw_to_svg(exc_path, path)
        else:
            # Default: Excalidraw JSON
            data = self.to_excalidraw()
            with open(path, "w") as f:
                json.dump(data, f, indent=2)

    # ------------------------------------------------------------------
    # D2 generation
    # ------------------------------------------------------------------

    def to_d2(self) -> str:
        """Generate D2 markup from the scene.

        Title and caption are rendered using D2's `near` keyword to keep
        them out of the graph layout. Flow direction is set based on
        the layout pattern.
        """
        lines: list[str] = []

        d2_shapes = {
            "start": "oval",
            "end": "oval",
            "process": "rectangle",
            "decision": "diamond",
        }

        # Determine flow direction from the layout pattern
        pattern = getattr(self, "_layout_pattern", "pipeline")
        if pattern in ("pipeline",):
            lines.append("direction: right")
        else:
            lines.append("direction: down")
        lines.append("")

        # Title/subtitle/caption use `near` to stay out of the layout
        for elem in self._elements.values():
            if elem.role == "title":
                lines.append(f"{elem.id}: {elem.text} {{")
                lines.append("  shape: text")
                lines.append("  style.font-size: 28")
                lines.append("  style.bold: true")
                lines.append(f'  style.font-color: "{self.palette.title_color}"')
                lines.append("  near: top-center")
                lines.append("}")
                lines.append("")
            elif elem.role == "subtitle":
                lines.append(f"{elem.id}: {elem.text} {{")
                lines.append("  shape: text")
                lines.append("  style.font-size: 20")
                lines.append("  style.bold: true")
                lines.append(f'  style.font-color: "{self.palette.subtitle_color}"')
                lines.append("  near: top-center")
                lines.append("}")
                lines.append("")
            elif elem.role == "caption":
                lines.append(f"{elem.id}: {elem.text} {{")
                lines.append("  shape: text")
                lines.append("  style.font-size: 13")
                lines.append(f'  style.font-color: "{self.palette.caption_color}"')
                lines.append("  near: bottom-center")
                lines.append("}")
                lines.append("")

        # Flow elements (shapes that participate in the graph)
        for elem in self._elements.values():
            if elem.role in ("title", "subtitle", "caption", "annotation"):
                continue

            shape = d2_shapes.get(elem.role, "rectangle")
            colors = self._get_colors(elem)
            fill, stroke, text_color = colors

            label = elem.text.replace("\n", "\\n")
            lines.append(f"{elem.id}: {label} {{")
            lines.append(f"  shape: {shape}")

            font_size = _ROLE_FONT.get(elem.role, (16, "center"))[0]
            lines.append(f"  style.font-size: {font_size}")

            if fill and fill != "transparent":
                lines.append(f'  style.fill: "{fill}"')
            if stroke and stroke != "transparent":
                lines.append(f'  style.stroke: "{stroke}"')
            if text_color:
                lines.append(f'  style.font-color: "{text_color}"')

            if elem.emphasis == "high" and elem.role not in ("title", "subtitle", "caption"):
                lines.append("  style.stroke-width: 3")
                lines.append("  style.shadow: true")
            elif elem.emphasis == "low":
                lines.append("  style.opacity: 0.6")

            lines.append("}")
            lines.append("")

        # Annotations: connected to targets with subtle dashed lines
        for ann in self._annotations:
            label = ann.text.replace("\n", "\\n")
            ann_color = self.palette.annotation_color
            lines.append(f"{ann.id}: {label} {{")
            lines.append("  shape: text")
            lines.append("  style.font-size: 13")
            lines.append(f'  style.font-color: "{ann_color}"')
            lines.append("}")
            lines.append(f"{ann.near_id} -- {ann.id} {{")
            lines.append("  style.stroke-dash: 3")
            lines.append("  style.opacity: 0.3")
            lines.append("}")
            lines.append("")

        # Connections
        for conn in self._connections:
            style_parts: list[str] = []

            if conn.style == "dashed":
                style_parts.append("style.stroke-dash: 5")
            elif conn.style == "dotted":
                style_parts.append("style.stroke-dash: 2")

            weight_map = {"thin": 1, "normal": 2, "bold": 3}
            sw = weight_map.get(conn.weight, 2)
            if sw != 2:
                style_parts.append(f"style.stroke-width: {sw}")

            src_elem = self._elements.get(conn.source_id)
            if src_elem:
                src_colors = self._get_colors(src_elem)
                if src_colors[1] and src_colors[1] != "transparent":
                    style_parts.append(f'style.stroke: "{src_colors[1]}"')

            if conn.label:
                label = conn.label.replace("\n", "\\n").replace("$", "")
                line = f"{conn.source_id} -> {conn.target_id}: {label}"
            else:
                line = f"{conn.source_id} -> {conn.target_id}"

            if style_parts:
                line += " {"
                lines.append(line)
                for sp in style_parts:
                    lines.append(f"  {sp}")
                lines.append("}")
            else:
                lines.append(line)

        return "\n".join(lines) + "\n"

    @staticmethod
    def _ensure_d2() -> str:
        """Find the D2 binary, auto-installing if missing.

        Returns the path to the D2 executable.
        """
        import shutil
        import os
        import sys
        import subprocess
        import platform
        from pathlib import Path

        # 1. Check PATH
        existing = shutil.which("d2")
        if existing:
            return existing

        # 2. Check our cached install location
        cache_dir = Path.home() / ".cache" / "plotcraft"
        cached = cache_dir / "d2"
        if cached.exists() and os.access(cached, os.X_OK):
            return str(cached)

        # 3. Auto-install via the official installer script
        print("PlotCraft: installing D2 for first-time rendering (one-time)...")
        cache_dir.mkdir(parents=True, exist_ok=True)

        system = platform.system().lower()
        if system in ("darwin", "linux"):
            # Use the official installer with custom prefix
            try:
                env = os.environ.copy()
                env["PREFIX"] = str(cache_dir.parent)  # Will install to ~/.cache/bin
                result = subprocess.run(
                    "curl -fsSL https://d2lang.com/install.sh | sh -s -- -p " + str(cache_dir.parent),
                    shell=True, capture_output=True, text=True, timeout=120, env=env,
                )
                if result.returncode != 0:
                    raise RuntimeError(result.stderr or result.stdout)
                # Find the installed binary
                for candidate in [cache_dir.parent / "bin" / "d2", cache_dir / "d2"]:
                    if candidate.exists():
                        # Symlink to our cache location for stability
                        if not cached.exists():
                            try:
                                cached.symlink_to(candidate)
                            except OSError:
                                shutil.copy2(candidate, cached)
                        print("PlotCraft: D2 installed.")
                        return str(candidate)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to auto-install D2.\n"
                    f"Install manually:\n"
                    f"  macOS:  brew install d2\n"
                    f"  Linux:  curl -fsSL https://d2lang.com/install.sh | sh\n"
                    f"  Other:  https://d2lang.com/releases\n"
                    f"Error: {e}"
                )

        raise RuntimeError(
            f"D2 is not installed and auto-install isn't available on {system}.\n"
            f"Install manually: https://d2lang.com/releases"
        )

    def _render_d2(self, output_path: str, fmt: str = "svg") -> None:
        """Render using D2 CLI.

        Requires D2 to be installed: https://d2lang.com/
        Install via: brew install d2 (macOS) or see docs for other platforms.
        """
        import shutil
        import subprocess
        import tempfile
        import os

        d2_binary = self._ensure_d2()

        d2_source = self.to_d2()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".d2", prefix="plotcraft_", delete=False,
        ) as f:
            f.write(d2_source)
            d2_source_path = f.name

        try:
            # We don't pass D2's --theme: PlotCraft sets explicit
            # style.fill / style.stroke / style.font-color in the D2 source
            # from the active Palette, which would override D2 themes anyway.
            # Dark mode uses --theme 200 only as a fallback for any element
            # PlotCraft didn't style explicitly (e.g. the canvas backdrop
            # if the user is rendering to PNG via D2 directly).
            cmd = [
                d2_binary,
                "--sketch",
                "--layout", "dagre",
                "--pad", "60",
            ]
            if self.dark:
                cmd.extend(["--theme", "200"])

            cmd.extend([d2_source_path, output_path])

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise RuntimeError(f"D2 rendering failed: {result.stderr}")
        finally:
            os.unlink(d2_source_path)

    # ------------------------------------------------------------------
    # Element builders
    # ------------------------------------------------------------------

    def _seed(self, elem_id: str) -> int:
        return zlib.adler32(elem_id.encode())

    def _get_colors(self, elem: Element) -> tuple[str | None, str, str]:
        """Get (fill, stroke, text_color) for an element from the active palette."""
        if elem.emphasis in ("high", "low") and elem.role not in ("title", "subtitle", "caption"):
            return self.palette.role(elem.emphasis)
        return self.palette.role(elem.role)

    def _make_shape(
        self, elem_id: str, shape_type: str,
        x: float, y: float, w: float, h: float,
        fill: str | None, stroke: str,
        bound_text_id: str | None = None,
    ) -> dict:
        seed = self._seed(elem_id)
        d: dict = {
            "type": shape_type,
            "id": elem_id,
            "x": x, "y": y, "width": w, "height": h,
            "strokeColor": stroke,
            "backgroundColor": fill or "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "angle": 0,
            "seed": seed,
            "version": 1,
            "versionNonce": seed ^ 0xFFFF,
            "isDeleted": False,
            "groupIds": [],
            "boundElements": [],
            "link": None,
            "locked": False,
        }
        if bound_text_id:
            d["boundElements"] = [{"id": bound_text_id, "type": "text"}]
        if shape_type == "rectangle":
            d["roundness"] = {"type": 3}
        return d

    def _make_text(
        self, elem_id: str, text: str,
        x: float, y: float, w: float, h: float,
        color: str, font_size: int = 16, align: str = "center",
        container_id: str | None = None, v_align: str = "top",
    ) -> dict:
        seed = self._seed(elem_id)
        return {
            "type": "text",
            "id": elem_id,
            "x": x, "y": y, "width": w, "height": h,
            "text": text,
            "originalText": text,
            "fontSize": font_size,
            "fontFamily": 3,
            "textAlign": align,
            "verticalAlign": v_align,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "angle": 0,
            "seed": seed,
            "version": 1,
            "versionNonce": seed ^ 0xFFFF,
            "isDeleted": False,
            "groupIds": [],
            "boundElements": None,
            "link": None,
            "locked": False,
            "containerId": container_id,
            "lineHeight": 1.25,
        }

    def _make_arrow(self, conn: Connection, src: Element, tgt: Element) -> list[dict]:
        """Create arrow between two elements.

        Uses straight lines from source edge to target edge. The exit point
        on the source aims directly at the target center, producing clean
        diagonal or straight connections without ugly L-bends.
        """
        GAP = 14.0

        src_cx = src.x + src.width / 2
        src_cy = src.y + src.height / 2
        tgt_cx = tgt.x + tgt.width / 2
        tgt_cy = tgt.y + tgt.height / 2

        # Compute the angle from source center to target center
        dx = tgt_cx - src_cx
        dy = tgt_cy - src_cy
        angle = math.atan2(dy, dx)

        # Exit point: where a ray from src center toward tgt center hits the src edge
        sx, sy = self._edge_point(src, angle, GAP)
        # Entry point: where a ray from tgt center toward src center hits the tgt edge
        ex, ey = self._edge_point(tgt, angle + math.pi, GAP)

        # Simple straight line — no bends
        rel_points = [[0, 0], [ex - sx, ey - sy]]

        arrow_id = f"arrow_{conn.source_id}_{conn.target_id}"
        seed = self._seed(arrow_id)
        stroke_w = {"thin": 1, "normal": 2, "bold": 3}.get(conn.weight, 2)
        src_colors = self._get_colors(src)
        stroke = src_colors[1] if src_colors[1] != "transparent" else "#757575"

        arrow = {
            "type": "arrow",
            "id": arrow_id,
            "x": sx, "y": sy,
            "width": abs(ex - sx) or 1, "height": abs(ey - sy) or 1,
            "strokeColor": stroke,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": stroke_w,
            "strokeStyle": conn.style,
            "roughness": 1,
            "opacity": 100,
            "angle": 0,
            "seed": seed,
            "version": 1,
            "versionNonce": seed ^ 0xFFFF,
            "isDeleted": False,
            "groupIds": [],
            "boundElements": None,
            "link": None,
            "locked": False,
            "points": rel_points,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
        }

        result = [arrow]

        # Arrow label — offset to the side of the midpoint
        if conn.label:
            label_id = f"{arrow_id}_label"
            mid_x = (sx + ex) / 2
            mid_y = (sy + ey) / 2
            label_w = len(conn.label) * 8 + 12
            label_h = 20

            # Offset perpendicular to arrow direction
            perp_x = -math.sin(angle) * 14
            perp_y = math.cos(angle) * 14

            result.append(self._make_text(
                label_id, conn.label,
                mid_x + perp_x - label_w / 2,
                mid_y + perp_y - label_h / 2,
                label_w, label_h,
                color="#757575" if not self.dark else "#8B8B8B",
                font_size=13, align="center",
            ))

        return result

    @staticmethod
    def _edge_point(elem: Element, angle: float, gap: float) -> tuple[float, float]:
        """Find where a ray at `angle` from element center exits the element edge."""
        cx = elem.x + elem.width / 2
        cy = elem.y + elem.height / 2
        hw = elem.width / 2
        hh = elem.height / 2

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # For rectangles/diamonds: find intersection with bounding box
        if abs(cos_a) * hh > abs(sin_a) * hw:
            # Hits left or right edge
            t = hw / abs(cos_a)
        else:
            # Hits top or bottom edge
            t = hh / abs(sin_a)

        return (cx + cos_a * (t + gap), cy + sin_a * (t + gap))
