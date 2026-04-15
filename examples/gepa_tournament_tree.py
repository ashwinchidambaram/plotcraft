"""Tournament: single-elimination bracket from a frozen 64-candidate pool.

Visual story:
- Left: 4 generation strategies producing 64 candidates
- Center: bracket narrowing 64→32→16→8→4→2→1 with increasing eval rigor
- Right: champion on full validation
- Bottom: rollout breakdown

Key insight: NO MUTATION. If the best prompt wasn't generated in step 1,
it can never be found. Pure diversity + competition.
"""

import json
import zlib


def _s(n): return zlib.adler32(n.encode())

def rect(id, x, y, w, h, fill, stroke, opacity=100, sw=1.5):
    s = _s(id)
    return {"type":"rectangle","id":id,"x":x,"y":y,"width":w,"height":h,
        "strokeColor":stroke,"backgroundColor":fill,
        "fillStyle":"solid","strokeWidth":sw,"strokeStyle":"solid",
        "roughness":1,"opacity":opacity,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False,"roundness":{"type":3}}

def circ(id, x, y, r, fill, stroke, opacity=100, sw=2):
    s = _s(id)
    return {"type":"ellipse","id":id,"x":x-r,"y":y-r,"width":r*2,"height":r*2,
        "strokeColor":stroke,"backgroundColor":fill,
        "fillStyle":"solid","strokeWidth":sw,"strokeStyle":"solid",
        "roughness":1,"opacity":opacity,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False}

def txt(id, x, y, w, h, content, size=14, color="#374151", align="left"):
    s = _s(id)
    return {"type":"text","id":id,"x":x,"y":y,"width":w,"height":h,
        "text":content,"originalText":content,
        "fontSize":size,"fontFamily":1,"textAlign":align,"verticalAlign":"top",
        "strokeColor":color,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid",
        "roughness":0,"opacity":100,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False,"containerId":None,"lineHeight":1.25}

def ln(id, pts, stroke, width=2, opacity=100):
    s = _s(id)
    mx = min(p[0] for p in pts); my = min(p[1] for p in pts)
    rel = [[p[0]-mx,p[1]-my] for p in pts]
    return {"type":"line","id":id,"x":mx,"y":my,
        "width":max(p[0] for p in rel) or 1,"height":max(p[1] for p in rel) or 1,
        "strokeColor":stroke,"backgroundColor":"transparent",
        "fillStyle":"solid","strokeWidth":width,"strokeStyle":"solid",
        "roughness":1,"opacity":opacity,"angle":0,
        "seed":s,"version":1,"versionNonce":s^0xFFFF,
        "isDeleted":False,"groupIds":[],"boundElements":None,
        "link":None,"locked":False,"points":rel}

def arr(id, x, y, pts, stroke="#374151", width=2, opacity=60):
    s = _s(id)
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


elements = []

# Colors
BLUE_F = "#DBEAFE"; BLUE_S = "#3B82F6"
GREEN = "#16A34A"; GREEN_S = "#15803D"; GREEN_F = "#DCFCE7"
RED_S = "#EF4444"; RED_F = "#FEE2E2"
ORANGE_F = "#FEF3C7"; ORANGE_S = "#F59E0B"
PURPLE_F = "#EDE9FE"; PURPLE_S = "#7C3AED"
GRAY = "#9CA3AF"

# Layout zones
GEN_X = 60       # generation strategies
POOL_X = 280     # frozen pool
BRACKET_X = 440  # bracket start
CHAMP_X = 1200   # champion
CY = 300         # center y


# ── Title ────────────────────────────────────────────────────────

elements.append(txt("title", 280, 20, 900, 42,
    "Tournament: Single-Elimination Bracket",
    size=36, color="#1F2937", align="center"))
elements.append(txt("sub", 220, 72, 1020, 18,
    "Maximum initial diversity, head-to-head elimination, no mutation — the pool is frozen after generation",
    size=13, color="#6B7280", align="center"))


# ══════════════════════════════════════════════════════════════════
# LEFT: 4 Generation Strategies
# ══════════════════════════════════════════════════════════════════

elements.append(txt("gen_h", GEN_X, 120, 200, 18,
    "4 Generation Strategies", size=14, color=ORANGE_S))

strategies = [
    ("Reasoning (x16)", ORANGE_F, ORANGE_S),
    ("Format (x16)", BLUE_F, BLUE_S),
    ("Detail Level (x16)", PURPLE_F, PURPLE_S),
    ("Error Prevention (x16)", RED_F, RED_S),
]

sy = 155
for i, (name, fill, stroke) in enumerate(strategies):
    elements.append(rect(f"strat_{i}", GEN_X, sy, 170, 28, fill, stroke, 90))
    elements.append(txt(f"stratn_{i}", GEN_X+8, sy+5, 155, 14,
        name, size=11, color="#374151"))
    sy += 34

# Seed prompt indicator
elements.append(circ("seed_dot", GEN_X+10, sy+10, 7, GREEN, GREEN_S))
elements.append(txt("seed_l", GEN_X+22, sy+3, 100, 14,
    "+ seed prompt", size=10, color=GRAY))


# ══════════════════════════════════════════════════════════════════
# FROZEN POOL
# ══════════════════════════════════════════════════════════════════

elements.append(rect("pool_box", POOL_X, 145, 110, 260, "#F9FAFB", "#6B7280", 60))
elements.append(txt("pool_t", POOL_X+10, 150, 90, 18,
    "64 pool", size=14, color="#374151", align="center"))

# Grid of tiny dots representing 64 candidates
dot_r = 5
cols_n = 6
for i in range(64):
    row = i // cols_n
    col = i % cols_n
    dx = POOL_X + 15 + col * 15
    dy = 178 + row * 15
    fill = GREEN if i == 0 else BLUE_F
    stroke = GREEN_S if i == 0 else BLUE_S
    op = 100 if i == 0 else 70
    elements.append(circ(f"pd_{i}", dx, dy, dot_r, fill, stroke, op, 1))

elements.append(txt("frozen_l", POOL_X+5, 355, 100, 14,
    "POOL FROZEN", size=10, color=RED_S))
elements.append(txt("frozen_l2", POOL_X+5, 370, 110, 12,
    "no new prompts after\nthis point", size=9, color=GRAY))

# Arrow from strategies to pool
elements.append(arr("a_gen_pool", GEN_X+175, 250, [[0,0],[POOL_X-GEN_X-185, 0]],
    ORANGE_S, 2, 50))


# ══════════════════════════════════════════════════════════════════
# BRACKET: Progressive elimination
# ══════════════════════════════════════════════════════════════════

elements.append(txt("bracket_h", BRACKET_X+50, 120, 350, 18,
    "Single-Elimination Bracket", size=14, color=BLUE_S))

rounds = [
    ("R1", "32 matchups", "5 ex", 32, BRACKET_X),
    ("R2", "16 matchups", "7 ex", 16, BRACKET_X + 130),
    ("R3", "8 matchups", "10 ex", 8, BRACKET_X + 260),
    ("R4", "4 matchups", "15 ex", 4, BRACKET_X + 390),
    ("R5", "2 matchups", "20 ex", 2, BRACKET_X + 520),
]

for i, (name, matchups, examples, survivors, rx) in enumerate(rounds):
    # Round header
    elements.append(txt(f"rh_{i}", rx, 145, 100, 14,
        name, size=13, color=BLUE_S))
    elements.append(txt(f"rm_{i}", rx, 160, 100, 12,
        matchups, size=9, color=GRAY))
    elements.append(txt(f"re_{i}", rx, 173, 100, 12,
        examples, size=9, color=BLUE_S))

    # Uniform dot size — the COUNT tells the elimination story
    dot_size = 6
    n_dots = survivors
    cols_r = min(6, n_dots)
    spacing = 16  # fixed spacing for uniform look
    for j in range(n_dots):
        row = j // cols_r
        col = j % cols_r
        dx = rx + 10 + col * spacing
        dy = 200 + row * spacing
        # Progressively deeper blue
        opacity = 60 + i * 8
        elements.append(circ(f"rd_{i}_{j}", dx, dy, dot_size,
            BLUE_F, BLUE_S, opacity, 1.5))

    pass  # Arrows handled below as one continuous flow line

# Rollout counts under each round
rollouts = ["320", "224", "160", "120", "80"]
for i, (_, _, _, _, rx) in enumerate(rounds):
    elements.append(txt(f"rc_{i}", rx, 400, 80, 14,
        f"{rollouts[i]} rollouts", size=9, color=GRAY))


# ══════════════════════════════════════════════════════════════════
# CHAMPION
# ══════════════════════════════════════════════════════════════════

# ── Continuous flow arrow below all dot grids ────────────────────

flow_y = 315  # below tallest grid (R1: 6 rows × 16px = 96px, starts at 200, ends ~296)
flow_start = BRACKET_X
flow_end = rounds[-1][4] + 40

# One continuous arrow
elements.append(arr("flow_arrow", flow_start, flow_y,
    [[0, 0], [flow_end - flow_start, 0]], BLUE_S, 2, 45))

# Elimination markers at each round boundary
eliminations = ["64→32", "32→16", "16→8", "8→4", "4→2"]
for i in range(len(rounds)):
    rx = rounds[i][4]
    # Small tick mark
    elements.append(ln(f"flow_tick_{i}", [[rx+5, flow_y-5], [rx+5, flow_y+5]],
        BLUE_S, 1.5, 45))
    # Elimination count
    if i < len(eliminations):
        elements.append(txt(f"flow_elim_{i}", rx-5, flow_y+18, 60, 12,
            eliminations[i], size=9, color=BLUE_S, align="center"))


# ══════════════════════════════════════════════════════════════════

# Arrow from flow to champion
sf_rx = rounds[-1][4]
arrow_y = flow_y
elements.append(arr("a_to_champ", sf_rx + 50, arrow_y,
    [[0,0],[CHAMP_X - sf_rx - 80, 0]], GREEN_S, 3, 70))

# Champion node
elements.append(circ("champion", CHAMP_X, arrow_y, 30, GREEN, GREEN_S))
elements.append(txt("champ_l", CHAMP_X-35, arrow_y+38, 80, 18,
    "Champion", size=14, color=GREEN))
elements.append(txt("champ_l2", CHAMP_X-50, arrow_y+58, 110, 14,
    "full validation set", size=11, color=GRAY))

# Key insight callout — below champion with clear gap
elements.append(txt("insight1", CHAMP_X-60, arrow_y+90, 220, 16,
    "No mutation between rounds.", size=12, color=RED_S))
elements.append(txt("insight2", CHAMP_X-60, arrow_y+110, 220, 25,
    "If the best prompt wasn't\ngenerated in step 1,\nit can never be found.", size=11, color=GRAY))


# ── Rigor progression line ───────────────────────────────────────

ry = 430
elements.append(ln("rigor_line", [[BRACKET_X, ry],[BRACKET_X+580, ry]], "#E5E7EB", 1, 30))
elements.append(txt("rigor_l", BRACKET_X, ry+5, 500, 14,
    "evaluation rigor increases:  5 → 7 → 10 → 15 → 20 → full valset",
    size=11, color=BLUE_S))
elements.append(txt("rigor_total", BRACKET_X, ry+22, 300, 14,
    "total: ~904 rollouts (preliminary rounds)",
    size=11, color=GRAY))


# ── Legend ────────────────────────────────────────────────────────

ly = ry + 50
elements.append(rect("leg_bg", 60, ly, 700, 45, "#FAFAFA", "#E5E7EB", 70, 1))
elements.append(txt("leg_t", 70, ly+5, 50, 14, "Legend:", size=11, color="#374151"))

elements.append(circ("lc1", 140, ly+14, 6, GREEN, GREEN_S, 100, 1.5))
elements.append(txt("lt1", 150, ly+6, 80, 14, "Seed prompt", size=10, color=GRAY))

elements.append(circ("lc2", 260, ly+14, 6, BLUE_F, BLUE_S, 80, 1.5))
elements.append(txt("lt2", 270, ly+6, 80, 14, "Candidate", size=10, color=GRAY))

elements.append(circ("lc3", 370, ly+14, 8, GREEN, GREEN_S, 100, 2))
elements.append(txt("lt3", 382, ly+6, 80, 14, "Champion", size=10, color=GRAY))

elements.append(txt("leg_foot", 70, ly+28, 650, 12,
    "Head-to-head: both prompts evaluated on the SAME examples per matchup  |  Ties favor lower seed",
    size=9, color=GRAY))


# ── Render ───────────────────────────────────────────────────────

doc = {
    "type":"excalidraw","version":2,"source":"plotcraft",
    "elements":elements,
    "appState":{"viewBackgroundColor":"#FFFFFF","gridSize":None},
    "files":{},
}

out = "examples/renders/gepa_tournament_tree.excalidraw"
with open(out, "w") as f:
    json.dump(doc, f, indent=2)

import subprocess
r = subprocess.run(
    ["uv","run","python","skills/plotcraft-diagram/references/render_excalidraw.py",out],
    capture_output=True, text=True, timeout=30)
print(f"-> {r.stdout.strip()}" if r.returncode==0 else f"ERROR: {r.stderr}")
