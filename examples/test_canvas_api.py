"""Test: recreate slime mold with the Canvas API — should be ~40 lines, not 300."""

from plotcraft.spatial import Canvas

c = Canvas(1600, 650)

c.title("Slime Mold: Progressive Pruning",
    "Physarum optimizes by reinforcing paths to food — analogous to reinforcing prompt candidates",
    mapping="food = test example | vein = candidate prompt | pruning = elimination | network = champion")

# Food source positions (consistent across panels)
foods = [(-65,-78), (55,-72), (82,12), (50,72), (-58,68), (-82,-5)]
food_labels = ["ex17", "ex42", "ex8", "ex31", "ex55", "ex3"]

# Panel (a): Explore
p1 = c.panel("(a)", "Explore: 20 candidates", title_color="#B45309")
for dx, dy in foods:
    p1.dot(dx, dy, label=food_labels[foods.index((dx,dy))])
p1.blob(0, 0, n=6, r=14)
for i in range(20):
    angle = (6.28 * i / 20)
    p1.branch(angle, 80, 2.5, color="#D4A017", opacity=65, max_depth=3)
p1.caption("All candidates explore uniformly\nEach vein = a prompt variation",
           extra_line="10 examples per candidate", extra_color="#B45309")

# Panel (b): Prune
p2 = c.panel("(b)", "Prune: keep 10, mutate", title_color="#92400E")
for dx, dy in foods:
    p2.dot(dx, dy, label=food_labels[foods.index((dx,dy))])
p2.blob(0, 0, n=4, r=11)
# Strong veins to food, ghost veins away
import math
for i in range(16):
    angle = 6.28 * i / 16
    near = any(abs(angle - math.atan2(dy,dx)) < 0.4 or
               abs(angle - math.atan2(dy,dx) + 6.28) < 0.4
               for dx,dy in foods)
    if near:
        # Find nearest food
        for dx, dy in foods:
            if abs(angle - math.atan2(dy,dx)) < 0.4:
                p2.vein(0, 0, dx, dy, width=5.5, color="#B8860B", opacity=95)
                break
    else:
        import random
        r = random.Random(i)
        l = r.uniform(25, 50)
        p2.vein(0, 0, l*math.cos(angle), l*math.sin(angle),
                width=0.8, color="#D1D5DB", opacity=25)
p2.caption("Prompts near high-scoring examples\nget reinforced and rewritten",
           extra_line="15 examples per candidate", extra_color="#92400E")

# Panel (c): Converge
p3 = c.panel("(c)", "Converge: champion", title_color="#166534")
for dx, dy in foods:
    p3.dot(dx, dy, label=food_labels[foods.index((dx,dy))])
p3.blob(0, 0, n=5, r=13, fill="#16A34A", stroke="#15803D")
for dx, dy in foods:
    p3.vein(0, 0, dx, dy, width=5, color="#16A34A", opacity=90)
# Cross connections
adj = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]
for a, b in adj:
    p3.vein(foods[a][0], foods[a][1], foods[b][0], foods[b][1],
            width=2.5, color="#22C55E", opacity=50)
p3.caption("Single optimized path survives\nEfficient coverage of all examples",
           extra_line="30 examples, full validation", extra_color="#166534")

# Arrows + legend + footer
c.arrow_between(p1, p2, "keep 10", "#B45309")
c.arrow_between(p2, p3, "keep 5 → 3 → 1", "#166534")

c.legend([
    ("Test example", "#FEF3C7", "#D97706"),
    ("Active candidate", "#FCD34D", "#B8860B"),
    ("Eliminated", "#E5E7EB", "#D1D5DB"),
    ("Champion", "#16A34A", "#15803D"),
])

c.footer("20 → 10 → 5 → 3 → 1  (~540-930 rollouts)  |  survivors rewritten each round")

c.save("examples/renders/canvas_api_test.png")
print("Done!")
