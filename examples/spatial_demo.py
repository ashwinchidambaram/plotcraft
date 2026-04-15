"""Spatial composition demo: Neural network training convergence."""

import json
import random
import zlib

def seed_val(name):
    return zlib.adler32(name.encode())

def circle(id, x, y, r, fill, stroke, opacity=100):
    s = seed_val(id)
    return {
        "type": "ellipse", "id": id,
        "x": x - r, "y": y - r, "width": r * 2, "height": r * 2,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": opacity, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s ^ 0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
    }

def text(id, x, y, w, h, content, size=16, color="#1E3A5F", align="center"):
    s = seed_val(id)
    return {
        "type": "text", "id": id,
        "x": x, "y": y, "width": w, "height": h,
        "text": content, "originalText": content,
        "fontSize": size, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "top",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s ^ 0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
        "containerId": None, "lineHeight": 1.25,
    }

def line(id, x, y, points, stroke="#D1D5DB", width=2, dash="solid"):
    s = seed_val(id)
    return {
        "type": "line", "id": id,
        "x": x, "y": y,
        "width": abs(points[-1][0] - points[0][0]) or 1,
        "height": abs(points[-1][1] - points[0][1]) or 1,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width,
        "strokeStyle": dash, "roughness": 1, "opacity": 100, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s ^ 0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
        "points": points,
    }

def arrow(id, x, y, points, stroke="#16A34A", width=3):
    s = seed_val(id)
    return {
        "type": "arrow", "id": id,
        "x": x, "y": y,
        "width": abs(points[-1][0]) or 1,
        "height": abs(points[-1][1]) or 1,
        "strokeColor": stroke, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width,
        "strokeStyle": "solid", "roughness": 1, "opacity": 100, "angle": 0,
        "seed": s, "version": 1, "versionNonce": s ^ 0xFFFF,
        "isDeleted": False, "groupIds": [], "boundElements": None,
        "link": None, "locked": False,
        "points": points,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
    }


elements = []
rng = random.Random(42)

# ── Title ────────────────────────────────────────────────────────

elements.append(text("title", 250, 30, 1000, 50,
    "How Gradient Descent Finds the Minimum",
    size=38, color="#1E3A5F"))
elements.append(text("subtitle", 300, 80, 900, 25,
    "Random initialization converges to a solution through iterative steps, each guided by the loss gradient",
    size=15, color="#6B7280"))

# ── Layout constants ─────────────────────────────────────────────

CENTER_Y = 320
cols = [80, 340, 600, 860, 1120, 1380]

# ── Column headers ───────────────────────────────────────────────

headers = [
    "Random Init", "Epoch 1", "Epoch 10", "Epoch 50", "Epoch 200", "Converged"
]
for i, label in enumerate(headers):
    elements.append(text(f"h_{i}", cols[i], 130, 200, 25, label,
        size=17, color="#1E3A5F"))

# ── Vertical dividers ────────────────────────────────────────────

for i in range(1, 6):
    dx = cols[i] - 30
    elements.append(line(f"div_{i}", dx, 120, [[0, 0], [0, 380]],
        stroke="#E5E7EB", width=1, dash="dashed"))

# ── Random Init: scattered points (high loss, random positions) ──

for i in range(25):
    px = cols[0] + 30 + rng.uniform(0, 170)
    py = CENTER_Y - 100 + rng.uniform(0, 200)
    r = rng.uniform(6, 10)
    elements.append(circle(f"init_{i}", px, py, r, "#FCA5A5", "#EF4444", opacity=70))

elements.append(text("loss0", cols[0] + 40, CENTER_Y + 120, 140, 20,
    "loss = 4.82", size=14, color="#EF4444"))

# ── Epoch 1: slightly less scattered ─────────────────────────────

for i in range(20):
    px = cols[1] + 40 + rng.uniform(0, 140)
    py = CENTER_Y - 80 + rng.uniform(0, 160)
    r = rng.uniform(7, 10)
    elements.append(circle(f"ep1_{i}", px, py, r, "#FDBA74", "#F97316", opacity=75))

elements.append(text("loss1", cols[1] + 40, CENTER_Y + 120, 140, 20,
    "loss = 3.21", size=14, color="#F97316"))

# ── Epoch 10: forming clusters ───────────────────────────────────

cx10 = cols[2] + 110
cy10 = CENTER_Y
for i in range(15):
    angle = rng.uniform(0, 6.28)
    dist = rng.uniform(20, 70)
    px = cx10 + dist * rng.uniform(-1, 1)
    py = cy10 + dist * rng.uniform(-0.7, 0.7)
    elements.append(circle(f"ep10_{i}", px, py, 9, "#FDE68A", "#F59E0B", opacity=80))

elements.append(text("loss10", cols[2] + 40, CENTER_Y + 120, 140, 20,
    "loss = 1.47", size=14, color="#F59E0B"))

# ── Epoch 50: tighter cluster ────────────────────────────────────

cx50 = cols[3] + 100
cy50 = CENTER_Y
for i in range(10):
    px = cx50 + rng.uniform(-40, 40)
    py = cy50 + rng.uniform(-30, 30)
    elements.append(circle(f"ep50_{i}", px, py, 10, "#86EFAC", "#22C55E", opacity=85))

elements.append(text("loss50", cols[3] + 40, CENTER_Y + 120, 140, 20,
    "loss = 0.34", size=14, color="#22C55E"))

# ── Epoch 200: very tight ────────────────────────────────────────

cx200 = cols[4] + 100
cy200 = CENTER_Y
for i in range(6):
    px = cx200 + rng.uniform(-18, 18)
    py = cy200 + rng.uniform(-15, 15)
    elements.append(circle(f"ep200_{i}", px, py, 11, "#34D399", "#16A34A", opacity=90))

elements.append(text("loss200", cols[4] + 40, CENTER_Y + 120, 140, 20,
    "loss = 0.08", size=14, color="#16A34A"))

# ── Converged: single point ──────────────────────────────────────

cx_final = cols[5] + 100
elements.append(circle("final", cx_final, CENTER_Y, 28, "#16A34A", "#15803D"))

# Target crosshair
elements.append(line("cross_h", cx_final - 40, CENTER_Y, [[0, 0], [80, 0]],
    stroke="#15803D", width=1, dash="dashed"))
elements.append(line("cross_v", cx_final, CENTER_Y - 40, [[0, 0], [0, 80]],
    stroke="#15803D", width=1, dash="dashed"))

elements.append(text("loss_final", cols[5] + 40, CENTER_Y + 120, 140, 20,
    "loss = 0.001", size=14, color="#16A34A"))
elements.append(text("converged_label", cols[5] + 30, CENTER_Y + 45, 150, 20,
    "global minimum", size=14, color="#15803D"))

# ── Annotations ──────────────────────────────────────────────────

elements.append(text("scatter_note", cols[0] + 20, CENTER_Y + 150, 180, 30,
    "high variance\nrandom weights", size=12, color="#9CA3AF"))

elements.append(text("converge_note", cols[4] + 10, CENTER_Y + 150, 200, 30,
    "gradient steps shrink\nas learning rate decays", size=12, color="#9CA3AF"))

# ── Footer ───────────────────────────────────────────────────────

elements.append(text("footer", 400, CENTER_Y + 200, 700, 25,
    "Scattered → Clustered → Converged    (loss decreases by 4,800x)",
    size=17, color="#3B82F6"))


# ── Assemble and render ──────────────────────────────────────────

doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "plotcraft",
    "elements": elements,
    "appState": {"viewBackgroundColor": "#FFFFFF", "gridSize": None},
    "files": {},
}

out = "examples/renders/spatial_gradient_descent.excalidraw"
with open(out, "w") as f:
    json.dump(doc, f, indent=2)

import subprocess
result = subprocess.run(
    ["uv", "run", "python", "skills/plotcraft-diagram/references/render_excalidraw.py", out],
    capture_output=True, text=True, timeout=30,
)
if result.returncode == 0:
    print(f"-> {result.stdout.strip()}")
else:
    print(f"ERROR: {result.stderr}")
