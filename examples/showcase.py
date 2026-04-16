"""PlotCraft Showcase — diagrams that explain real things."""

from plotcraft import Scene


# ══════════════════════════════════════════════════════════════════
# 1. How a neural network learns (top-down, earth theme)
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="earth")
s.add("How a Neural Network Learns", role="title")
s.add("Training Data", role="start", size="large")
s.add("Forward Pass", role="process", emphasis="high")
s.add("Compute Loss", role="decision")
s.add("Backpropagation", role="process", size="large", emphasis="high")
s.add("Update Weights", role="process")
s.add("Trained Model", role="end", size="large")

s.connect("Training Data", "Forward Pass")
s.connect("Forward Pass", "Compute Loss", label="predictions")
s.connect("Compute Loss", "Backpropagation", label="error signal")
s.connect("Backpropagation", "Update Weights", label="gradients")
s.connect("Update Weights", "Forward Pass", label="next batch", style="dashed")
s.connect("Compute Loss", "Trained Model", label="converged", style="dashed")

s.annotate("Input flows through layers", near="Forward Pass")
s.annotate("How wrong were we?", near="Compute Loss")
s.annotate("Chain rule through every layer", near="Backpropagation")

s.add("Repeat thousands of times until the loss stops decreasing", role="caption")
s.layout("top_down")
s.save("examples/renders/neural_network_learning.png")
print("1. Neural network learning")


# ══════════════════════════════════════════════════════════════════
# 2. How the internet routes a packet (pipeline, ocean theme)
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="ocean")
s.add("How a packet crosses the internet", role="title")
s.add("Your Browser", role="start", size="large")
s.add("DNS Lookup", role="process")
s.add("Local Router", role="process")
s.add("ISP Network", role="process", emphasis="high")
s.add("Internet Backbone", role="process", size="large", emphasis="high")
s.add("CDN Edge", role="process")
s.add("Origin Server", role="end", size="large")

s.connect("Your Browser", "DNS Lookup", label="google.com?")
s.connect("DNS Lookup", "Local Router", label="142.250.80.46")
s.connect("Local Router", "ISP Network")
s.connect("ISP Network", "Internet Backbone", label="BGP routing")
s.connect("Internet Backbone", "CDN Edge")
s.connect("CDN Edge", "Origin Server")

s.annotate("~1ms", near="DNS Lookup")
s.annotate("Multiple autonomous systems", near="Internet Backbone")
s.annotate("Nearest cache", near="CDN Edge")

s.add("50 milliseconds, 15 hops, 3 continents — and you just see a webpage", role="caption")
s.layout("pipeline")
s.save("examples/renders/internet_packet.png")
print("2. Internet packet routing")


# ══════════════════════════════════════════════════════════════════
# 3. How a compiler works (pipeline, grape theme)
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="grape")
s.add("How your code becomes machine instructions", role="title")
s.add("Source Code", role="start", size="large")
s.add("Lexer", role="process")
s.add("Parser", role="process", emphasis="high")
s.add("AST", role="process", size="large")
s.add("Optimizer", role="process", emphasis="high")
s.add("Code Gen", role="process")
s.add("Machine Code", role="end", size="large")

s.connect("Source Code", "Lexer", label="characters")
s.connect("Lexer", "Parser", label="tokens")
s.connect("Parser", "AST", label="syntax tree")
s.connect("AST", "Optimizer", label="IR")
s.connect("Optimizer", "Code Gen", label="optimized IR")
s.connect("Code Gen", "Machine Code", label="binary")

s.annotate("Breaks text into tokens", near="Lexer")
s.annotate("Dead code elimination,\nloop unrolling, inlining", near="Optimizer")

s.add("Every program you run went through these 6 stages", role="caption")
s.layout("pipeline")
s.save("examples/renders/compiler_pipeline.png")
print("3. Compiler pipeline")


# ══════════════════════════════════════════════════════════════════
# 4. How evolution works (cycle, default theme)
# ══════════════════════════════════════════════════════════════════

s = Scene()
s.add("How evolution drives adaptation", role="title")
s.add("Genetic Variation", role="start", size="large")
s.add("Natural Selection", role="decision", size="large")
s.add("Survival", role="process", emphasis="high")
s.add("Reproduction", role="process", size="large")
s.add("Mutation", role="process")

s.connect("Genetic Variation", "Natural Selection")
s.connect("Natural Selection", "Survival", label="fit enough")
s.connect("Survival", "Reproduction")
s.connect("Reproduction", "Mutation")
s.connect("Mutation", "Genetic Variation", label="next generation", style="dashed")

s.annotate("Environmental pressure", near="Natural Selection")
s.annotate("Random DNA changes", near="Mutation")
s.annotate("Offspring inherit traits", near="Reproduction")

s.add("No designer needed — just variation, selection, and time", role="caption")
s.layout("cycle")
s.save("examples/renders/evolution.png")
print("4. Evolution")


# ══════════════════════════════════════════════════════════════════
# 5. How a startup dies (top-down, dark theme)
# ══════════════════════════════════════════════════════════════════

s = Scene(dark=True)
s.add("How most startups die", role="title")
s.add("Great Idea", role="start", size="large")
s.add("Build Product", role="process", emphasis="high")
s.add("No Users", role="decision", size="large")
s.add("Pivot", role="process")
s.add("Run Out of Money", role="process", emphasis="low")
s.add("Shut Down", role="end")
s.add("Find Market Fit", role="end", size="large", emphasis="high")

s.connect("Great Idea", "Build Product")
s.connect("Build Product", "No Users")
s.connect("No Users", "Pivot", label="try again")
s.connect("Pivot", "Build Product", label="rebuild", style="dashed")
s.connect("No Users", "Run Out of Money", label="too late")
s.connect("Run Out of Money", "Shut Down")
s.connect("No Users", "Find Market Fit", label="finally", style="dashed")

s.annotate("The loop most get stuck in", near="Pivot")
s.annotate("90% of startups", near="Shut Down")

s.add("The gap between building and finding users kills more startups than bad ideas", role="caption")
s.layout("top_down")
s.save("examples/renders/startup_death.png")
print("5. How startups die")


# ══════════════════════════════════════════════════════════════════
# 6. How memory works in your brain (fan-out, vanilla theme)
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="vanilla")
s.add("How your brain stores memories", role="title")
s.add("Experience", role="start", size="large")
s.add("Sensory Memory", role="process")
s.add("Working Memory", role="process", emphasis="high")
s.add("Forgotten", role="process", emphasis="low")
s.add("Long-Term Memory", role="end", size="large", emphasis="high")
s.add("Procedural", role="end")
s.add("Episodic", role="end")
s.add("Semantic", role="end")

s.connect("Experience", "Sensory Memory")
s.connect("Sensory Memory", "Working Memory", label="attention")
s.connect("Sensory Memory", "Forgotten", label="ignored")
s.connect("Working Memory", "Long-Term Memory", label="rehearsal + emotion")
s.connect("Long-Term Memory", "Procedural", label="how to ride a bike")
s.connect("Long-Term Memory", "Episodic", label="your wedding day")
s.connect("Long-Term Memory", "Semantic", label="Paris is in France")
s.connect("Working Memory", "Forgotten", label="not rehearsed", style="dashed")

s.annotate("~30 seconds\nwithout rehearsal", near="Working Memory")
s.annotate("Can last a lifetime", near="Long-Term Memory")

s.add("Attention decides what gets in, emotion decides what stays", role="caption")
s.layout("top_down")
s.save("examples/renders/memory_brain.png")
print("6. How memory works")


# ══════════════════════════════════════════════════════════════════
# 7. How a CPU executes an instruction (pipeline, cool theme)
# ══════════════════════════════════════════════════════════════════

s = Scene(theme="cool")
s.add("The 5-stage CPU pipeline", role="title")
s.add("Fetch", role="start", size="large")
s.add("Decode", role="process")
s.add("Execute", role="process", size="large", emphasis="high")
s.add("Memory", role="process")
s.add("Write Back", role="end", size="large")

s.connect("Fetch", "Decode")
s.connect("Decode", "Execute")
s.connect("Execute", "Memory")
s.connect("Memory", "Write Back")

s.annotate("Get instruction\nfrom RAM", near="Fetch")
s.annotate("ALU does the math", near="Execute")
s.annotate("Store result\nin register", near="Write Back")

s.add("Every instruction your computer runs passes through these 5 stages — billions per second", role="caption")
s.layout("pipeline")
s.save("examples/renders/cpu_pipeline.png")
print("7. CPU pipeline")


print("\nAll showcase renders in examples/renders/")
