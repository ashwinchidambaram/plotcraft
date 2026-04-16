"""Render the README gallery — every template on an accessible topic.

These are the diagrams the README links to. Each one matches a prompt
from the "Things you can ask Claude" section, so a reader can map
prompt → output 1:1.
"""
from plotcraft import (
    Pipeline, DecisionTree, Comparison, Cycle, FanOut, Architecture, Timeline,
)

OUT = "examples/renders"

# 1. Pipeline — the immune system, accessible to anyone
Pipeline("How your immune system fights an infection") \
    .step("Pathogen detected") \
    .step("T-cells respond", emphasize=True) \
    .step("Antibodies produced") \
    .step("Memory cells form") \
    .caption("Next time, your body remembers") \
    .save(f"{OUT}/readme_pipeline.png")

# 2. DecisionTree — the sweater question, very relatable
DecisionTree("Should you wear a sweater?") \
    .question("Are you cold?") \
    .branch("Yes", "Wear it", note="Comfort wins") \
    .branch("No", "Skip it", note="You'll overheat") \
    .caption("Trust your goosebumps") \
    .save(f"{OUT}/readme_decision.png")

# 3. Comparison — the eternal phone debate
Comparison("iPhone vs Android", theme="ocean") \
    .option("iPhone", points=[
        "Just works",
        "Locked ecosystem",
        "Premium pricing",
    ]) \
    .option("Android", points=[
        "Endless choice",
        "Customizable",
        "Wide price range",
    ]) \
    .save(f"{OUT}/readme_comparison.png")

# 4. Cycle — the writer's revision loop
Cycle("The writer's revision loop", theme="grape") \
    .step("Draft") \
    .step("Get feedback", emphasize=True) \
    .step("Revise") \
    .feedback("repeat") \
    .caption("Until the words sing") \
    .save(f"{OUT}/readme_cycle.png")

# 5. FanOut — what happens when you press Send
FanOut("What happens when you press Send", theme="sunset") \
    .source("Your email") \
    .target("Recipient inbox", emphasize=True) \
    .target("Spam filter") \
    .target("Sent folder") \
    .target("Backup server") \
    .caption("One click, many destinations") \
    .save(f"{OUT}/readme_fanout.png")

# 6. Architecture — how a restaurant works (everyone gets this one)
Architecture("How a restaurant works", theme="forest") \
    .tier("Front of House", ["Host", "Servers", "Bar"]) \
    .tier("Kitchen", ["Line cooks", "Chef", "Dishwasher"]) \
    .tier("Suppliers", ["Produce", "Meat", "Dry goods"]) \
    .caption("Every plate touches every layer") \
    .save(f"{OUT}/readme_architecture.png")

# 7. Timeline — a product launch year
Timeline("A product launch year", theme="vanilla") \
    .event("Q1", "Research") \
    .event("Q2", "Build", emphasize=True) \
    .event("Q3", "Beta") \
    .event("Q4", "Launch") \
    .save(f"{OUT}/readme_timeline.png")

print("All README gallery diagrams rendered.")
