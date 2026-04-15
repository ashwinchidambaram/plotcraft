"""Spatial composition helpers for PlotCraft.

Encodes the patterns that produce good biology-textbook-style
illustrations in 1-2 shots instead of 5+ iterations.

Usage:
    from plotcraft.spatial import Canvas

    c = Canvas(1600, 650)
    c.title("Slime Mold: Progressive Pruning",
            "Physarum optimizes by reinforcing paths to food",
            mapping="food = example | vein = candidate | network = champion")

    p1 = c.panel("(a)", "Explore: 20 candidates", position="left")
    p2 = c.panel("(b)", "Prune: keep 10", position="center")
    p3 = c.panel("(c)", "Converge: champion", position="right")

    # Draw inside each panel...
    p1.circle(0, -40, 12, fill="#93C5FD")
    p1.vein(0, 0, 50, -60, width=3)
    p1.caption("All candidates explore uniformly")

    c.arrow_between(p1, p2, label="keep 10")
    c.legend([("Food source", "#FEF3C7", "#D97706"), ...])
    c.footer("20 → 10 → 5 → 3 → 1  (~540 rollouts)")
    c.save("output.png")
"""

import json
import math
import random
import zlib
import subprocess
import tempfile
import os


def _seed(name):
    return zlib.adler32(name.encode())


def _ell(id, x, y, w, h, fill, stroke, opacity=100, sw=2):
    s = _seed(id)
    return {"type": "ellipse", "id": id,
        "x": x-w/2, "y": y-h/2, "width": w, "height": h,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 1, "opacity": opacity, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s^0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False}


def _txt(id, x, y, w, h, content, size=14, color="#374151", align="center"):
    s = _seed(id)
    return {"type": "text", "id": id, "x": x, "y": y, "width": w, "height": h,
        "text": content, "originalText": content,
        "fontSize": size, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "top",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s^0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "containerId": None, "lineHeight": 1.25}


def _line(id, points, stroke, width=2, opacity=100):
    s = _seed(id)
    mx = min(p[0] for p in points); my = min(p[1] for p in points)
    rel = [[p[0]-mx, p[1]-my] for p in points]
    return {"type": "line", "id": id, "x": mx, "y": my,
        "width": max(p[0] for p in rel) or 1,
        "height": max(p[1] for p in rel) or 1,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width, "strokeStyle": "solid",
        "roughness": 1, "opacity": opacity, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s^0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "points": rel}


def _arrow(id, x, y, pts, stroke="#6B7280", width=2, opacity=50):
    s = _seed(id)
    return {"type": "arrow", "id": id, "x": x, "y": y,
        "width": abs(pts[-1][0]) or 1, "height": abs(pts[-1][1]) or 1,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width, "strokeStyle": "solid",
        "roughness": 1, "opacity": opacity, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s^0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False, "points": pts,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow"}


def _wobble(x1, y1, x2, y2, rng, segs=10, amp=2.5):
    pts = []; dx, dy = x2-x1, y2-y1
    ln = math.sqrt(dx*dx + dy*dy) or 1
    nx, ny = -dy/ln, dx/ln
    for i in range(segs + 1):
        t = i / segs
        off = rng.gauss(0, amp) * math.sin(t * math.pi)
        pts.append([x1 + dx*t + nx*off, y1 + dy*t + ny*off])
    return pts


# ══════════════════════════════════════════════════════════════════


class Panel:
    """A framed illustration panel within a Canvas.

    All coordinates are relative to the panel center.
    The panel draws a circular border (like a petri dish).
    """

    def __init__(self, canvas, cx, cy, radius, label, title, title_color, prefix):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.prefix = prefix
        self._rng = random.Random(hash(prefix))
        self._counter = 0

        # Draw the dish border
        canvas._add(_ell(f"{prefix}_dish", cx, cy, radius*2, radius*2,
            "#FAFAF8", "#D1D5DB", 100, 2))
        canvas._add(_ell(f"{prefix}_inner", cx, cy, radius*1.92, radius*1.92,
            "transparent", "#E5E7EB", 35, 1))

        # Panel label and title
        canvas._add(_txt(f"{prefix}_label", cx - radius - 10, canvas._panel_label_y,
            35, 20, label, size=16, color="#1F2937"))
        canvas._add(_txt(f"{prefix}_title", cx - radius + 25, canvas._panel_label_y,
            280, 20, title, size=15, color=title_color))

    def _id(self, suffix=""):
        self._counter += 1
        return f"{self.prefix}_{self._counter}{('_' + suffix) if suffix else ''}"

    def circle(self, dx, dy, r, fill="#93C5FD", stroke="#60A5FA", opacity=100):
        """Draw a circle at offset (dx, dy) from panel center."""
        self.canvas._add(_ell(self._id("c"), self.cx+dx, self.cy+dy,
            r*2, r*2, fill, stroke, opacity, 2))

    def dot(self, dx, dy, r=8, fill="#FEF3C7", stroke="#D97706", label=""):
        """Draw a labeled dot (food source / data point)."""
        self.canvas._add(_ell(self._id("h"), self.cx+dx, self.cy+dy,
            r*3, r*3, "transparent", stroke, 15, 1))
        self.canvas._add(_ell(self._id("d"), self.cx+dx, self.cy+dy,
            r*2, r*2, fill, stroke, 90, 1.5))
        if label:
            self.canvas._add(_txt(self._id("dl"), self.cx+dx-20, self.cy+dy+r+3,
                40, 12, label, size=9, color=stroke))

    def blob(self, dx, dy, n=5, r=12, fill="#FCD34D", stroke="#B8860B", opacity=80):
        """Amorphous blob via overlapping ellipses."""
        for i in range(n):
            ox = self._rng.gauss(0, r*0.3)
            oy = self._rng.gauss(0, r*0.3)
            w = self._rng.uniform(r*0.7, r*1.4)
            h = self._rng.uniform(r*0.6, r*1.2)
            self.canvas._add(_ell(self._id("b"), self.cx+dx+ox, self.cy+dy+oy,
                w, h, fill, stroke, opacity, 1))

    def vein(self, dx1, dy1, dx2, dy2, width=3, color="#D4A017", opacity=100):
        """Organic wobbly vein between two points (relative to center)."""
        x1, y1 = self.cx+dx1, self.cy+dy1
        x2, y2 = self.cx+dx2, self.cy+dy2
        pts = _wobble(x1, y1, x2, y2, self._rng,
            segs=max(6, int(math.sqrt((x2-x1)**2+(y2-y1)**2)/10)),
            amp=width*0.4)
        self.canvas._add(_line(self._id("v"), pts, color, max(1, width), opacity))

    def branch(self, angle, length, width, color="#D4A017", opacity=100,
               depth=0, max_depth=3, sub_count=2):
        """Recursive branching from center."""
        self._branch_from(0, 0, angle, length, width, color, opacity,
                          depth, max_depth, sub_count)

    def _branch_from(self, dx, dy, angle, length, width, color, opacity,
                     depth, max_depth, sub_count):
        if depth > max_depth or length < 10 or width < 0.8:
            return
        curve = self._rng.gauss(0, 0.1)
        edx = dx + length * math.cos(angle + curve)
        edy = dy + length * math.sin(angle + curve)
        self.vein(dx, dy, edx, edy, width, color, opacity)

        n = sub_count if self._rng.random() < 0.6 else max(1, sub_count - 1)
        for i in range(n):
            spread = self._rng.uniform(0.3, 0.55)
            ca = angle + (i - n/2 + 0.5) * spread
            self._branch_from(edx, edy, ca,
                length * self._rng.uniform(0.5, 0.65),
                width * self._rng.uniform(0.5, 0.65),
                color, opacity, depth+1, max_depth, sub_count)

    def leader(self, label, dx_label, dy_label, dx_target, dy_target, color="#6B7280"):
        """Leader line from label position to target position."""
        lx, ly = self.cx+dx_label, self.cy+dy_label
        tx, ty = self.cx+dx_target, self.cy+dy_target
        self.canvas._add(_line(self._id("ll"), [[lx, ly], [tx, ty]], color, 1, 45))
        self.canvas._add(_ell(self._id("ld"), tx, ty, 3, 3, color, color, 50, 1))
        self.canvas._add(_txt(self._id("lt"), lx-5, ly-15, 120, 14,
            label, size=10, color=color, align="left"))

    def caption(self, text, extra_line="", extra_color="#6B7280"):
        """Caption text below the panel dish."""
        gap = self.radius + 55  # KEY LEARNING: generous gap below dish
        self.canvas._add(_txt(self._id("cap"), self.cx-130, self.cy+gap,
            260, 45, text, size=10, color="#6B7280"))
        if extra_line:
            self.canvas._add(_txt(self._id("cap2"), self.cx-130, self.cy+gap+40,
                200, 15, extra_line, size=10, color=extra_color))


class Canvas:
    """Spatial composition canvas.

    Layout zones (top to bottom):
    - Title zone: title, subtitle, mapping line
    - Panel zone: framed illustrations with labels
    - Caption zone: text under each panel
    - Legend zone: color key
    - Footer zone: closing line

    Key spacing rules (learned from iteration):
    - Illustrations capped at ~250px diameter
    - 40%+ of vertical space reserved for text
    - Dishes-to-caption gap = radius * 0.4
    - Panel spacing = radius * 4
    - Text NEVER inside illustration framing
    """

    def __init__(self, width=1600, height=650):
        self.width = width
        self.height = height
        self._elements = []
        self._panels = []
        self._panel_label_y = 125  # default, updated by title()

    def _add(self, elem):
        self._elements.append(elem)

    def title(self, main, subtitle="", mapping=""):
        """Title block at top. Sets vertical position for panels below."""
        self._add(_txt("title", self.width*0.2, 15, self.width*0.6, 45,
            main, size=38, color="#1F2937"))
        y = 62
        if subtitle:
            self._add(_txt("subtitle", self.width*0.15, y, self.width*0.7, 18,
                subtitle, size=13, color="#6B7280"))
            y += 26
        if mapping:
            self._add(_txt("mapping", self.width*0.15, y, self.width*0.7, 16,
                mapping, size=11, color="#9CA3AF"))
            y += 22
        self._panel_label_y = y + 10

    def panel(self, label, title, position="left", radius=125,
              title_color="#374151"):
        """Create a framed panel. Position: 'left', 'center', 'right'."""
        n_panels = len(self._panels)
        spacing = (self.width - 200) / 3
        cx = 150 + spacing * (0.5 + n_panels)
        cy = self._panel_label_y + radius + 45

        prefix = f"p{len(self._panels)}"
        p = Panel(self, cx, cy, radius, label, title, title_color, prefix)
        self._panels.append(p)
        return p

    def arrow_between(self, p1, p2, label="", color="#6B7280"):
        """Draw a transition arrow between two panels."""
        x1 = p1.cx + p1.radius + 20
        x2 = p2.cx - p2.radius - 20
        y = p1.cy
        length = x2 - x1
        self._add(_arrow(f"arr_{len(self._elements)}", x1, y,
            [[0, 0], [length, 0]], color, 3, 55))
        if label:
            self._add(_txt(f"arrl_{len(self._elements)}",
                x1 + length/2 - 50, y - 22, 100, 16,
                label, size=12, color=color))

    def legend(self, items):
        """Legend row. Items: list of (label, fill, stroke)."""
        if not self._panels:
            return
        ly = max(p.cy + p.radius for p in self._panels) + 140
        self._add(_txt("leg_title", 100, ly, 60, 14, "Legend:",
            size=12, color="#374151"))
        x = 180
        for i, (label, fill, stroke) in enumerate(items):
            self._add(_ell(f"leg_d{i}", x, ly+7, 12, 12, fill, stroke, 90, 1.5))
            self._add(_txt(f"leg_t{i}", x+10, ly, 130, 14, label,
                size=10, color="#6B7280", align="left"))
            x += 160

    def footer(self, text, color="#3B82F6"):
        """Footer text at the bottom."""
        if not self._panels:
            return
        ly = max(p.cy + p.radius for p in self._panels) + 170
        self._add(_txt("footer", self.width*0.2, ly, self.width*0.6, 16,
            text, size=13, color=color))

    def to_excalidraw(self):
        return {
            "type": "excalidraw", "version": 2, "source": "plotcraft",
            "elements": self._elements,
            "appState": {"viewBackgroundColor": "#FFFFFF", "gridSize": None},
            "files": {},
        }

    def save(self, path):
        """Save and render. Supports .excalidraw, .png, .svg."""
        exc_path = path.rsplit(".", 1)[0] + ".excalidraw"
        with open(exc_path, "w") as f:
            json.dump(self.to_excalidraw(), f, indent=2)

        if path.endswith(".excalidraw"):
            return

        # Render via Playwright
        import shutil
        render_script = os.path.join(
            os.path.dirname(__file__), "..", "..", "skills",
            "plotcraft-diagram", "references", "render_excalidraw.py",
        )
        if not os.path.exists(render_script):
            # Try relative to cwd
            render_script = "skills/plotcraft-diagram/references/render_excalidraw.py"

        if os.path.exists(render_script):
            result = subprocess.run(
                ["uv", "run", "python", render_script, exc_path],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode != 0:
                print(f"Render error: {result.stderr}")
        else:
            print(f"Render script not found. Saved {exc_path}")
