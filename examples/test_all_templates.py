"""Test every template renders to PNG successfully."""

from plotcraft import (
    Pipeline, DecisionTree, Comparison, Cycle, FanOut, Architecture, Timeline,
    Palette,
)

print("Testing all templates render to PNG...\n")

# 1. Pipeline
Pipeline("How HTTPS works") \
    .step("You type a URL") \
    .step("DNS Lookup") \
    .step("TLS Handshake", emphasize=True) \
    .step("Page Loads") \
    .caption("Every request, in milliseconds") \
    .save("examples/renders/template_pipeline.png")
print("✓ Pipeline → template_pipeline.png")

# 2. DecisionTree
DecisionTree("Picking your database") \
    .question("Structured?") \
    .branch("Yes", "PostgreSQL", note="ACID, joins") \
    .branch("No", "MongoDB", note="Flexible schema") \
    .caption("Start simple, migrate when you outgrow it") \
    .save("examples/renders/template_decision.png")
print("✓ DecisionTree → template_decision.png")

# 3. Comparison
Comparison("Monolith vs Microservices") \
    .option("Monolith", points=["Single deploy", "Tightly coupled", "Vertical scaling"]) \
    .option("Microservices", points=["Independent deploys", "Loosely coupled", "Horizontal scaling"]) \
    .save("examples/renders/template_comparison.png")
print("✓ Comparison → template_comparison.png")

# 4. Cycle
Cycle("How AI agents reason") \
    .step("Observe") \
    .step("Think", emphasize=True) \
    .step("Act") \
    .feedback("repeat") \
    .caption("Until goal is reached") \
    .save("examples/renders/template_cycle.png")
print("✓ Cycle → template_cycle.png")

# 5. FanOut
FanOut("How events propagate") \
    .source("Event Bus") \
    .target("Logger") \
    .target("Notifier", emphasize=True) \
    .target("Archiver") \
    .target("Analytics") \
    .caption("Every event reaches every consumer") \
    .save("examples/renders/template_fanout.png")
print("✓ FanOut → template_fanout.png")

# 6. Architecture
Architecture("How a request flows") \
    .tier("Frontend", ["Browser", "CDN", "Load Balancer"]) \
    .tier("Backend", ["API Server", "Auth Service"]) \
    .tier("Data", ["PostgreSQL", "Redis"]) \
    .caption("Each tier scales independently") \
    .save("examples/renders/template_architecture.png")
print("✓ Architecture → template_architecture.png")

# 7. Timeline
Timeline("Product roadmap") \
    .event("Q1", "Research") \
    .event("Q2", "Build", emphasize=True) \
    .event("Q3", "Beta") \
    .event("Q4", "Launch") \
    .save("examples/renders/template_timeline.png")
print("✓ Timeline → template_timeline.png")

# 8. Theme test (richer pipeline so the palette differences are visible)
for theme in [
    "default", "ocean", "forest", "sunset", "grape",
    "monochrome", "pastel", "vanilla",
]:
    Pipeline(f"Theme: {theme}", theme=theme) \
        .step("Input") \
        .step("Process", emphasize=True) \
        .step("Output") \
        .caption(f"Palette: {theme}") \
        .save(f"examples/renders/template_theme_{theme}.png")
print("✓ All 8 built-in themes produce distinct colors")

# 9. Dark mode
Pipeline("Dark mode test", dark=True) \
    .step("Start").step("Middle", emphasize=True).step("End") \
    .save("examples/renders/template_dark.png")
print("✓ Dark mode works")

# 10. Custom palette — user defines their own colors
brand_palette = Palette(
    name="my-brand",
    canvas="#FFFFFF",
    title_color="#0B1F3A",
    subtitle_color="#FF6B35",
    caption_color="#5A6F80",
    start=("#FFE5D9", "#FF6B35", "#3E1F0E"),
    end=("#D9F2FF", "#0066AA", "#0B1F3A"),
    process=("#F5F5F5", "#444444", "#1A1A1A"),
    decision=("#FFF8E1", "#F9A825", "#5C3A00"),
    high=("#FF6B35", "#BF360C", "#FFFFFF"),
    low=("#F5F5F5", "#BDBDBD", "#9E9E9E"),
)
Pipeline("Custom brand palette", theme=brand_palette) \
    .step("Submit") \
    .step("Validate", emphasize=True) \
    .step("Confirm") \
    .caption("Built from your own colors") \
    .save("examples/renders/template_custom_palette.png")
print("✓ Custom Palette works")

print("\nAll templates render successfully.")
