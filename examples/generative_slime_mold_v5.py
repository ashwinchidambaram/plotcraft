"""Generative illustration v5: Biology-meets-algorithm textbook figure.

The biological metaphor mapped explicitly to prompt optimization:
- Food sources = high-scoring test examples
- Veins = candidate prompt variations
- Pruning = elimination rounds
- Reinforcement = mutation via failure analysis
- Optimized network = champion prompt
"""

import json
import math
import random
import zlib


def seed_val(n):
    return zlib.adler32(n.encode())

def path_elem(id, points, stroke, width=2, opacity=100):
    s = seed_val(id)
    mx = min(p[0] for p in points); my = min(p[1] for p in points)
    rel = [[p[0]-mx, p[1]-my] for p in points]
    return {"type":"line","id":id,"x":mx,"y":my,
        "width":max(p[0] for p in rel) or 1,"height":max(p[1] for p in rel) or 1,
        "strokeColor":stroke,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":width,"strokeStyle":"solid",
        "roughness":1,"opacity":opacity,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False,"points":rel}

def ell(id, x, y, w, h, fill, stroke, opacity=100, sw=2):
    s = seed_val(id)
    return {"type":"ellipse","id":id,"x":x-w/2,"y":y-h/2,"width":w,"height":h,
        "strokeColor":stroke,"backgroundColor":fill,
        "fillStyle":"solid","strokeWidth":sw,"strokeStyle":"solid",
        "roughness":1,"opacity":opacity,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False}

def txt(id, x, y, w, h, content, size=14, color="#374151", align="center"):
    s = seed_val(id)
    return {"type":"text","id":id,"x":x,"y":y,"width":w,"height":h,
        "text":content,"originalText":content,
        "fontSize":size,"fontFamily":1,
        "textAlign":align,"verticalAlign":"top",
        "strokeColor":color,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid",
        "roughness":0,"opacity":100,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False,"containerId":None,"lineHeight":1.25}

def arrow_elem(id, x, y, pts, stroke="#6B7280", width=2, opacity=50):
    s = seed_val(id)
    return {"type":"arrow","id":id,"x":x,"y":y,
        "width":abs(pts[-1][0]) or 1,"height":abs(pts[-1][1]) or 1,
        "strokeColor":stroke,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":width,"strokeStyle":"solid",
        "roughness":1,"opacity":opacity,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False,"points":pts,
        "startBinding":None,"endBinding":None,
        "startArrowhead":None,"endArrowhead":"arrow"}


# ── Drawing helpers ──────────────────────────────────────────────

def wobble(x1, y1, x2, y2, rng, segs=10, amp=2.5):
    pts = []; dx, dy = x2-x1, y2-y1
    ln = math.sqrt(dx*dx+dy*dy) or 1; nx, ny = -dy/ln, dx/ln
    for i in range(segs+1):
        t = i/segs
        off = rng.gauss(0, amp) * math.sin(t*math.pi)
        pts.append([x1+dx*t+nx*off, y1+dy*t+ny*off])
    return pts

def vein(cx, cy, ex, ey, w, rng, elems, prefix, color="#D4A017", op=100):
    pts = wobble(cx, cy, ex, ey, rng, segs=max(6, int(math.sqrt((ex-cx)**2+(ey-cy)**2)/10)), amp=w*0.4)
    elems.append(path_elem(prefix, pts, color, width=max(1,w), opacity=op))

def sub_branches(ex, ey, angle, rng, elems, prefix, color, n=3, length=20, width=1.2, op=60):
    """Small sub-branches at a vein tip for organic density."""
    for i in range(n):
        ba = angle + rng.uniform(-0.7, 0.7)
        bl = rng.uniform(length*0.5, length)
        bx = ex + bl*math.cos(ba)
        by = ey + bl*math.sin(ba)
        vein(ex, ey, bx, by, width, rng, elems, f"{prefix}_sb{i}", color, op)

def petri_dish(cx, cy, r, elems, prefix):
    elems.append(ell(f"{prefix}_dish", cx, cy, r*2, r*2, "#FAFAF8", "#D1D5DB", 100, 2))
    elems.append(ell(f"{prefix}_inner", cx, cy, r*1.92, r*1.92, "transparent", "#E5E7EB", 35, 1))

def food_dot(cx, cy, elems, prefix, label="", r=8):
    elems.append(ell(f"{prefix}_h", cx, cy, r*3, r*3, "transparent", "#D97706", 15, 1))
    elems.append(ell(f"{prefix}", cx, cy, r*2, r*2, "#FEF3C7", "#D97706", 90, 1.5))
    if label:
        elems.append(txt(f"{prefix}_l", cx-20, cy+r+3, 40, 12, label,
                         size=9, color="#92400E", align="center"))

def central_blob(cx, cy, rng, elems, prefix, n=5, r=12, fill="#FCD34D", stroke="#B8860B", op=80):
    for i in range(n):
        dx = rng.gauss(0, r*0.3); dy = rng.gauss(0, r*0.3)
        w = rng.uniform(r*0.7, r*1.4); h = rng.uniform(r*0.6, r*1.2)
        elems.append(ell(f"{prefix}_c{i}", cx+dx, cy+dy, w, h, fill, stroke, op, 1))

def leader(x1, y1, x2, y2, elems, prefix, color="#6B7280"):
    elems.append(path_elem(f"{prefix}_ll", [[x1,y1],[x2,y2]], color, 1, 45))
    elems.append(ell(f"{prefix}_ld", x2, y2, 3, 3, color, color, 50, 1))


# ══════════════════════════════════════════════════════════════════

elements = []
DISH_R = 125
SP = 520

# Food sources — labeled as examples with scores
foods = [
    (-65, -78, "ex17"),
    (55, -72, "ex42"),
    (82, 12, "ex8"),
    (50, 72, "ex31"),
    (-58, 68, "ex55"),
    (-82, -5, "ex3"),
]

panels = [(280, 340), (280+SP, 340), (280+SP*2, 340)]


# ── Title block — generous spacing ───────────────────────────────

elements.append(txt("title", 350, 15, 1000, 45,
    "Slime Mold: Progressive Pruning", size=38, color="#1F2937"))
elements.append(txt("sub", 230, 62, 1200, 18,
    "Physarum optimizes its network by reinforcing paths to food — analogous to reinforcing high-scoring prompt candidates",
    size=13, color="#6B7280"))
elements.append(txt("mapping", 230, 88, 1200, 16,
    "food = test example  |  vein = candidate prompt  |  pruning = elimination  |  reinforcement = mutation  |  network = champion",
    size=11, color="#9CA3AF"))


# ══════════════════════════════════════════════════════════════════
# PANEL (a): EXPLORE — 20 candidates, all directions
# ══════════════════════════════════════════════════════════════════

cx, cy = panels[0]
rng_a = random.Random(42)

elements.append(txt("la", cx-130, 125, 30, 20, "(a)", size=16, color="#1F2937"))
elements.append(txt("la_t", cx-98, 125, 250, 20,
    "Explore: 20 candidates", size=15, color="#B45309"))

petri_dish(cx, cy, DISH_R, elements, "pa")

# Food sources with example labels
for i, (dx, dy, label) in enumerate(foods):
    food_dot(cx+dx, cy+dy, elements, f"fa_{i}", label)

# Central blob (candidate pool)
central_blob(cx, cy, rng_a, elements, "pa", n=6, r=14, fill="#FCD34D", stroke="#B8860B", op=85)

# Dense uniform branching — 20 main veins with sub-branches
for i in range(20):
    angle = (2*math.pi*i/20) + rng_a.uniform(-0.08, 0.08)
    length = DISH_R * rng_a.uniform(0.5, 0.82)
    ex = cx + length*math.cos(angle)
    ey = cy + length*math.sin(angle)
    vein(cx, cy, ex, ey, 2.2, rng_a, elements, f"pa_v{i}", "#D4A017", 65)
    # Sub-branches at tips for density
    sub_branches(ex, ey, angle, rng_a, elements, f"pa_v{i}", "#E3A621",
                 n=rng_a.randint(2,4), length=18, width=1, op=45)

# Labels
leader(cx+135, cy-150, cx+8, cy-5, elements, "lb_pool", "#B45309")
elements.append(txt("lb_pool_t", cx+100, cy-170, 120, 25,
    "candidate pool\n(20 prompts)", size=10, color="#B45309", align="left"))

elements.append(txt("cap_a", cx-130, cy+DISH_R+55, 260, 40,
    "All candidates explore uniformly\nEach vein = a prompt variation\ntested on random minibatches",
    size=10, color="#6B7280"))
elements.append(txt("cap_a2", cx-130, cy+DISH_R+100, 200, 15,
    "10 examples per candidate", size=10, color="#B45309"))


# ══════════════════════════════════════════════════════════════════
# PANEL (b): PRUNE — keep 10, mutate survivors
# ══════════════════════════════════════════════════════════════════

cx, cy = panels[1]
rng_b = random.Random(42)

elements.append(txt("lb", cx-130, 125, 30, 20, "(b)", size=16, color="#1F2937"))
elements.append(txt("lb_t", cx-98, 125, 300, 20,
    "Prune: keep 10, mutate survivors", size=15, color="#92400E"))

petri_dish(cx, cy, DISH_R, elements, "pb")

for i, (dx, dy, label) in enumerate(foods):
    food_dot(cx+dx, cy+dy, elements, f"fb_{i}", label)

central_blob(cx, cy, rng_b, elements, "pb", n=4, r=11, fill="#FCD34D", stroke="#B8860B", op=70)

# Branches — thick to food, ghost away, with sub-branches
for i in range(20):
    angle = (2*math.pi*i/20) + rng_b.uniform(-0.08, 0.08)

    # Check proximity to any food
    near_food = False
    nearest_fi = -1
    for fi, (dx, dy, _) in enumerate(foods):
        fa = math.atan2(dy, dx)
        diff = abs(angle - fa)
        if diff > math.pi: diff = 2*math.pi - diff
        if diff < 0.35:
            near_food = True
            nearest_fi = fi
            break

    if near_food:
        fx, fy = foods[nearest_fi][0], foods[nearest_fi][1]
        vein(cx, cy, cx+fx, cy+fy, 5.5, rng_b, elements, f"pb_s{i}", "#B8860B", 95)
        # Thick sub-branches near food
        sub_branches(cx+fx, cy+fy, math.atan2(fy, fx), rng_b, elements,
                     f"pb_s{i}", "#D4A017", n=3, length=15, width=2, op=70)
    else:
        # Ghost — fading, thin, short
        length = DISH_R * rng_b.uniform(0.2, 0.4)
        ex = cx + length*math.cos(angle)
        ey = cy + length*math.sin(angle)
        vein(cx, cy, ex, ey, 0.8, rng_b, elements, f"pb_g{i}", "#D1D5DB", 25)

# Mutation indicator
elements.append(ell("mut_diamond", cx, cy+DISH_R-15, 18, 18, "#EDE9FE", "#7C3AED", 70, 1.5))
leader(cx+12, cy+DISH_R-10, cx+60, cy+DISH_R+5, elements, "lb_mut", "#7C3AED")
elements.append(txt("lb_mut_t", cx+30, cy+DISH_R+5, 130, 14,
    "mutate via failure info", size=9, color="#7C3AED", align="left"))

elements.append(txt("cap_b", cx-130, cy+DISH_R+55, 260, 40,
    "Prompts near high-scoring examples\nget reinforced and rewritten\nWeak candidates eliminated",
    size=10, color="#6B7280"))
elements.append(txt("cap_b2", cx-130, cy+DISH_R+100, 200, 15,
    "15 examples per candidate", size=10, color="#92400E"))


# ══════════════════════════════════════════════════════════════════
# PANEL (c): CONVERGE — champion network
# ══════════════════════════════════════════════════════════════════

cx, cy = panels[2]
rng_c = random.Random(77)

elements.append(txt("lc", cx-130, 125, 30, 20, "(c)", size=16, color="#1F2937"))
elements.append(txt("lc_t", cx-98, 125, 300, 20,
    "Converge: champion prompt", size=15, color="#166534"))

petri_dish(cx, cy, DISH_R, elements, "pc")

for i, (dx, dy, label) in enumerate(foods):
    food_dot(cx+dx, cy+dy, elements, f"fc_{i}", label)

# Green champion blob
central_blob(cx, cy, rng_c, elements, "pc", n=5, r=13, fill="#16A34A", stroke="#15803D", op=90)

# Thick optimized veins to each food source
for i, (dx, dy, _) in enumerate(foods):
    vein(cx, cy, cx+dx, cy+dy, 5, rng_c, elements, f"pc_v{i}", "#16A34A", 90)
    # Parallel flow stroke
    vein(cx, cy, cx+dx, cy+dy, 2, rng_c, elements, f"pc_f{i}", "#15803D", 35)

# Cross-connections (efficient network edges)
adj = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,3),(1,4)]
for j,(a,b) in enumerate(adj):
    ax,ay = cx+foods[a][0], cy+foods[a][1]
    bx,by = cx+foods[b][0], cy+foods[b][1]
    vein(ax, ay, bx, by, 2.5, rng_c, elements, f"pc_x{j}", "#22C55E", 50)

# Champion label
leader(cx+140, cy-50, cx+20, cy, elements, "lb_champ", "#166534")
elements.append(txt("lb_champ_t", cx+115, cy-70, 120, 25,
    "champion prompt\n(optimized)", size=10, color="#166534", align="left"))

elements.append(txt("cap_c", cx-130, cy+DISH_R+55, 260, 40,
    "Single best prompt remains\nEfficient coverage of all examples\nNetwork = prompt structure",
    size=10, color="#6B7280"))
elements.append(txt("cap_c2", cx-130, cy+DISH_R+100, 200, 15,
    "30 examples, full validation", size=10, color="#166534"))


# ── Transition arrows ────────────────────────────────────────────

for i, (lab, col) in enumerate([("keep 10", "#B45309"), ("keep 5 → 3 → 1", "#166534")]):
    ax = panels[i][0] + DISH_R + 20
    ay = panels[i][1]
    arrow_len = SP - DISH_R*2 - 40
    elements.append(arrow_elem(f"ta{i}", ax, ay, [[0,0],[arrow_len,0]], col, 3, 55))
    elements.append(txt(f"ta{i}_l", ax + arrow_len//2 - 40, ay-22, 100, 16, lab, size=12, color=col))


# ── Legend ────────────────────────────────────────────────────────

ly = panels[0][1] + DISH_R + 140

elements.append(txt("leg_t", 100, ly, 60, 14, "Legend:", size=12, color="#374151"))

items = [
    (180, "#FEF3C7", "#D97706", "Test example (food)"),
    (340, "#FCD34D", "#B8860B", "Active candidate (vein)"),
    (520, "#E5E7EB", "#D1D5DB", "Eliminated (pruned)"),
    (700, "#EDE9FE", "#7C3AED", "Mutation step"),
    (870, "#16A34A", "#15803D", "Champion (optimized)"),
]
for lx, fill, stroke, label in items:
    elements.append(ell(f"leg_{lx}", lx, ly+7, 12, 12, fill, stroke, 90, 1.5))
    elements.append(txt(f"leg_t{lx}", lx+10, ly, 130, 14, label, size=10, color="#6B7280", align="left"))


# ── Footer ───────────────────────────────────────────────────────

elements.append(txt("footer", 280, ly+30, 850, 16,
    "Progressive pruning: 20 → 10 → 5 → 3 → 1 candidates  |  ~540-930 rollouts  |  survivors rewritten each round",
    size=12, color="#3B82F6"))


# ── Render ───────────────────────────────────────────────────────

doc = {
    "type":"excalidraw","version":2,"source":"plotcraft",
    "elements":elements,
    "appState":{"viewBackgroundColor":"#FFFFFF","gridSize":None},
    "files":{},
}

out = "examples/renders/generative_slime_mold_v5.excalidraw"
with open(out,"w") as f:
    json.dump(doc, f, indent=2)

import subprocess
r = subprocess.run(
    ["uv","run","python","skills/plotcraft-diagram/references/render_excalidraw.py",out],
    capture_output=True, text=True, timeout=30)
print(f"-> {r.stdout.strip()}" if r.returncode==0 else f"ERROR: {r.stderr}")
