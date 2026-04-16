"""Showcase diagrams for the README.

Topics chosen to be accessible (and fun):
  1. The life cycle of a star            (Scene, branching + feedback)
  2. The water cycle                      (Scene, parallel paths)
  3. How TikTok's recommendation works    (Scene, big feedback loop)
  4. Are you out of Claude Code usage?    (DecisionTree, just for fun)
"""
from plotcraft import Scene, DecisionTree


# ══════════════════════════════════════════════════════════════════
# 1. The life cycle of a star
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="grape", dark=True, width=1600, height=1100)
s.add("The Life Cycle of a Star", role="title")

# Birth
s.add("Stellar Nursery", role="start", size="large")
s.add("Protostar", role="process")
s.add("Main Sequence", role="process", size="large", emphasis="high")

# The big fork
s.add("Mass?", role="decision", size="large")

# Low/medium mass path (our sun's fate)
s.add("Red Giant", role="process")
s.add("Planetary Nebula", role="process")
s.add("White Dwarf", role="end")

# High mass path
s.add("Red Supergiant", role="process", emphasis="high")
s.add("Supernova", role="process", emphasis="high", size="large")

# Second fork — what's left after the supernova?
s.add("Remnant?", role="decision")
s.add("Neutron Star", role="end")
s.add("Black Hole", role="end", size="large")

s.connect("Stellar Nursery", "Protostar", label="gravitational collapse")
s.connect("Protostar", "Main Sequence", label="fusion ignites")
s.connect("Main Sequence", "Mass?", label="hydrogen depleted")
s.connect("Mass?", "Red Giant", label="< 8 solar masses")
s.connect("Red Giant", "Planetary Nebula", label="outer shells expelled")
s.connect("Planetary Nebula", "White Dwarf", label="core remains")
s.connect("Mass?", "Red Supergiant", label="> 8 solar masses")
s.connect("Red Supergiant", "Supernova", label="core collapse")
s.connect("Supernova", "Remnant?")
s.connect("Remnant?", "Neutron Star", label="< 3 solar masses")
s.connect("Remnant?", "Black Hole", label="> 3 solar masses")

# The cycle: stellar death seeds new star formation
s.connect("Planetary Nebula", "Stellar Nursery",
          label="returns gas", style="dashed")
s.connect("Supernova", "Stellar Nursery",
          label="seeds heavy elements", style="dashed")

s.annotate("Hydrogen → Helium fusion.\nStars stay here for billions of years.",
           near="Main Sequence")
s.annotate("Our Sun's fate — about 5 billion years from now.",
           near="Red Giant")
s.annotate("One of the most violent events in the universe.\nForges every element heavier than iron.",
           near="Supernova")

s.add("Star death seeds new star birth", role="caption")
s.layout("top_down")
s.save("examples/renders/readme_star_lifecycle.png")
print("1. Star lifecycle rendered.")


# ══════════════════════════════════════════════════════════════════
# 2. The water cycle
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="ocean", width=1500, height=950)
s.add("The Water Cycle", role="title")

# Sources
s.add("Ocean", role="start", size="large")
# Going up
s.add("Evaporation", role="process", emphasis="high")
s.add("Transpiration", role="process")
# Sky
s.add("Condensation", role="process", size="large", emphasis="high")
s.add("Precipitation", role="process", size="large", emphasis="high")
# Coming down
s.add("Surface Runoff", role="process")
s.add("Infiltration", role="process")
s.add("Groundwater", role="end")

# Two paths up to the sky
s.connect("Ocean", "Evaporation", label="sun heats water")
s.connect("Ocean", "Transpiration", label="plants drink")
s.connect("Evaporation", "Condensation", label="rises and cools")
s.connect("Transpiration", "Condensation")

# Sky → ground
s.connect("Condensation", "Precipitation", label="droplets form")

# Two paths back to the ocean
s.connect("Precipitation", "Surface Runoff", label="rivers")
s.connect("Precipitation", "Infiltration", label="soaks into soil")
s.connect("Infiltration", "Groundwater", label="aquifer")

# Feedback: everything returns to the sea
s.connect("Surface Runoff", "Ocean", style="dashed", label="back to sea")
s.connect("Groundwater", "Ocean", style="dashed", label="slow journey")

s.annotate("The sun's energy drives the entire cycle.",
           near="Evaporation")
s.annotate("Plants move billions of gallons per day,\noften more than rivers do.",
           near="Transpiration")
s.annotate("Some groundwater takes 10,000+ years\nto reach the sea.",
           near="Groundwater")

s.add("Earth's water has been cycling for 4 billion years", role="caption")
s.layout("top_down")
s.save("examples/renders/readme_water_cycle.png")
print("2. Water cycle rendered.")


# ══════════════════════════════════════════════════════════════════
# 3. How TikTok's recommendation algorithm works
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="sunset", dark=True, width=1700, height=1100)
s.add("How TikTok decides what to show you", role="title")

# Inputs
s.add("New Video Uploaded", role="start", size="large")
s.add("Extract Signals", role="process")

# The cold-start audience
s.add("Show to Small Test Audience", role="process", emphasis="high")
s.add("Track Engagement", role="process", size="large", emphasis="high")

# The decision: did it perform?
s.add("Performed well?", role="decision", size="large")

# Yes → bigger pool
s.add("Expand to Larger Audience", role="process", emphasis="high")
s.add("Goes Viral", role="end", size="large")

# No → suppressed
s.add("Suppress", role="process")
s.add("Buried in Feed", role="end")

# The user feedback layer
s.add("Your Watch History", role="process")
s.add("Your For You Page", role="process", emphasis="high")

# Forward flow
s.connect("New Video Uploaded", "Extract Signals",
          label="audio, captions, hashtags, faces")
s.connect("Extract Signals", "Show to Small Test Audience",
          label="match to interests")
s.connect("Show to Small Test Audience", "Track Engagement")
s.connect("Track Engagement", "Performed well?",
          label="watch time, replays, shares")
s.connect("Performed well?", "Expand to Larger Audience", label="yes")
s.connect("Performed well?", "Suppress", label="no")
s.connect("Expand to Larger Audience", "Goes Viral",
          label="repeat at each tier")
s.connect("Suppress", "Buried in Feed")

# The personal feedback loop
s.connect("Track Engagement", "Your Watch History",
          label="your behavior", style="dashed")
s.connect("Your Watch History", "Your For You Page",
          label="trains your model", style="dashed")
s.connect("Your For You Page", "Show to Small Test Audience",
          label="you're now part of someone's test pool", style="dashed")

s.annotate("Audio fingerprint, OCR on captions, object\ndetection in frames — all in seconds.",
           near="Extract Signals")
s.annotate("Watch time matters more than likes.\nA full re-watch is the strongest signal.",
           near="Track Engagement")
s.annotate("Each tier is bigger. Viral videos pass\nthrough 5-7 expanding waves.",
           near="Expand to Larger Audience")

s.add("Every video competes for attention. Every view trains the algorithm.",
      role="caption")
s.layout("top_down")
s.save("examples/renders/readme_tiktok.png")
print("3. TikTok algorithm rendered.")


# ══════════════════════════════════════════════════════════════════
# 4. Are you out of Claude Code usage? — a meme
# ══════════════════════════════════════════════════════════════════

DecisionTree("Are you out of Claude Code usage?", theme="sunset") \
    .question("Hit the limit?") \
    .branch("Buy more credits", "Open wallet", note="It weeps quietly") \
    .branch("Upgrade to Max plan", "Become Max user", note="No more limits, no more excuses") \
    .branch("Wait for reset", "Check the clock", note="Is it midnight UTC yet?") \
    .branch("Cry", "Stare at terminal", note="The only free option") \
    .caption("There are no wrong answers. Only expensive ones.") \
    .save("examples/renders/readme_claude_meme.png")
print("4. Claude Code meme rendered.")

print("\nAll showcase diagrams rendered.")
