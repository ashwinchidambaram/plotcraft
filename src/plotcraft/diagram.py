from __future__ import annotations
from plotcraft.types import (
    TextRole, ShapeKind, TextAlign, AnchorName, ArrowDirection, SectionStyle, BBox, ColorTheme,
    ConnectorStyle, LineWeight,
    TimelineEntry, TimelineOrientation, TreeNode,
)
from plotcraft.grid import Grid, GridConfig
from plotcraft.shapes import create_shape
from plotcraft.connectors import create_connector, route_all
from plotcraft.svg import SvgRenderer
from plotcraft.structures import build_timeline, build_tree
from plotcraft.wobble import Wobbler, WobbleConfig


class Diagram:
    """The single entry point for building diagrams."""

    def __init__(self, grid_config: GridConfig | None = None):
        self._grid = Grid(grid_config or GridConfig())
        self._shapes: dict[str, object] = {}  # shape_id -> Shape (tracked for validation)
        self._connectors: list[object] = []  # list of Connector stubs
        self._sections: list[dict] = []  # list of {label, shape_ids, style}
        self._timelines: list[dict] = []
        self._trees: list[dict] = []
        self._wobbler = Wobbler(WobbleConfig())
        self._renderer = SvgRenderer(wobbler=self._wobbler)

    def add(
        self,
        id: str,
        text: str,
        role: TextRole = TextRole.BODY,
        shape: ShapeKind = ShapeKind.RECT,
        align: TextAlign = TextAlign.CENTER,
        row: int | None = None,
        col: int | None = None,
        color: ColorTheme = ColorTheme.NEUTRAL,
    ) -> Diagram:
        """Add an element. Returns self for chaining."""
        if id in self._shapes:
            raise ValueError(f"Duplicate shape id: '{id}'")

        s = create_shape(id, text, kind=shape, role=role, align=align, color_theme=color)

        if row is not None and col is not None:
            self._grid.place(s, row, col)
        else:
            self._grid.auto_place(s)

        self._shapes[id] = s
        return self

    def connect(
        self,
        source_id: str,
        target_id: str,
        source_anchor: AnchorName = AnchorName.RIGHT_CENTER,
        target_anchor: AnchorName = AnchorName.LEFT_CENTER,
        label: str | None = None,
        direction: ArrowDirection = ArrowDirection.FORWARD,
        style: ConnectorStyle = ConnectorStyle.SOLID,
        line_weight: LineWeight = LineWeight.NORMAL,
    ) -> Diagram:
        """Connect two elements. Returns self for chaining."""
        if source_id not in self._shapes:
            raise ValueError(f"Unknown shape id: '{source_id}'")
        if target_id not in self._shapes:
            raise ValueError(f"Unknown shape id: '{target_id}'")

        conn_id = f"conn_{source_id}_{target_id}"
        conn = create_connector(conn_id, source_id, source_anchor, target_id, target_anchor, label, direction=direction, style=style, line_weight=line_weight)
        self._connectors.append(conn)
        return self

    def section(
        self,
        label: str,
        shape_ids: list[str],
        style: SectionStyle | None = None,
    ) -> Diagram:
        """Group shapes into a labeled section. Returns self for chaining."""
        for sid in shape_ids:
            if sid not in self._shapes:
                raise ValueError(f"Unknown shape id: '{sid}'")
        self._sections.append({
            "label": label,
            "shape_ids": shape_ids,
            "style": style or SectionStyle(),
        })
        return self

    def timeline(
        self,
        entries: list[TimelineEntry],
        orientation: TimelineOrientation = TimelineOrientation.HORIZONTAL,
        start_row: int = 0,
        start_col: int = 0,
    ) -> Diagram:
        """Add a timeline. Returns self for chaining."""
        self._timelines.append({
            "entries": entries,
            "orientation": orientation,
            "start_row": start_row,
            "start_col": start_col,
        })
        return self

    def tree(
        self,
        root: TreeNode,
        start_row: int = 0,
        start_col: int = 0,
    ) -> Diagram:
        """Add a tree. Returns self for chaining."""
        self._trees.append({
            "root": root,
            "start_row": start_row,
            "start_col": start_col,
        })
        return self

    def render(self) -> str:
        """Finalize layout, route connectors, return SVG string."""
        # Reset wobble RNG so repeated render() calls produce identical output.
        self._wobbler._rng.seed(self._wobbler._config.seed)
        placements = self._grid.all_placements()
        placements_dict = {p.shape.id: p for p in placements}

        routed = route_all(self._connectors, placements_dict)

        # Compute section bounds
        sections = []
        for sec in self._sections:
            style: SectionStyle = sec["style"]
            padding = style.padding
            label_height = style.label_font_size + 10.0

            min_x = float("inf")
            min_y = float("inf")
            max_x = float("-inf")
            max_y = float("-inf")
            for sid in sec["shape_ids"]:
                p = placements_dict[sid]
                bb = p.bounding_box
                min_x = min(min_x, bb.x)
                min_y = min(min_y, bb.y)
                max_x = max(max_x, bb.x + bb.width)
                max_y = max(max_y, bb.y + bb.height)

            bounds = BBox(
                x=min_x - padding,
                y=min_y - padding - label_height,
                width=(max_x - min_x) + 2 * padding,
                height=(max_y - min_y) + 2 * padding + label_height,
            )
            sections.append((sec["label"], bounds, style))

        # Build structure SVG fragments
        structure_fragments: list[str] = []
        grid_config = self._grid._config
        for tl in self._timelines:
            structure_fragments.append(build_timeline(
                tl["entries"], tl["orientation"],
                tl["start_row"], tl["start_col"], grid_config,
                wobbler=self._wobbler,
            ))
        for tr in self._trees:
            structure_fragments.append(build_tree(
                tr["root"], tr["start_row"], tr["start_col"], grid_config,
                wobbler=self._wobbler,
            ))

        canvas_size = self._grid.canvas_size()

        return self._renderer.render_diagram(
            placements, routed, canvas_size, sections, structure_fragments,
        )

    def show(self) -> None:
        """Open the diagram in the default browser for live preview."""
        import tempfile
        import webbrowser

        svg = self.render()
        # Write to a temp HTML file that auto-reloads nicely
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".svg", prefix="plotcraft_", delete=False
        ) as f:
            f.write(svg)
            path = f.name

        webbrowser.open(f"file://{path}")

    def save(self, path: str, scale: float = 2.0) -> None:
        """Render and write to file. Detects format from extension (.svg or .png)."""
        svg = self.render()
        if path.lower().endswith(".png"):
            import os
            # Ensure homebrew libs are discoverable for cairocffi
            if not os.environ.get("DYLD_LIBRARY_PATH"):
                for lib_dir in ("/opt/homebrew/lib", "/usr/local/lib"):
                    if os.path.isdir(lib_dir):
                        os.environ["DYLD_LIBRARY_PATH"] = lib_dir
                        break
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=path, scale=scale)
        else:
            with open(path, "w") as f:
                f.write(svg)
