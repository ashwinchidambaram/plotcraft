"""PlotCraft Gallery — diverse diagrams showing different subjects and themes."""

from plotcraft import Scene


# --------------------------------------------------------------------------
# 1. How HTTPS keeps you safe (default theme)
# --------------------------------------------------------------------------

s = Scene()
s.add("How HTTPS keeps your data safe", role="title")

s.add("You type a URL", role="start")
s.add("DNS Lookup", role="process")
s.add("TLS Handshake", role="process", emphasis="high")
s.add("Certificate Check", role="decision")
s.add("Encrypted Tunnel", role="process", size="large", emphasis="high")
s.add("Page Loads", role="end")

s.connect("You type a URL", "DNS Lookup")
s.connect("DNS Lookup", "TLS Handshake")
s.connect("TLS Handshake", "Certificate Check")
s.connect("Certificate Check", "Encrypted Tunnel", label="valid")
s.connect("Encrypted Tunnel", "Page Loads")

s.annotate("Server proves\nits identity", near="Certificate Check")
s.annotate("AES-256\nencryption", near="Encrypted Tunnel")

s.add("Every request, invisible, in milliseconds", role="caption")
s.layout("pipeline")
s.save("examples/renders/https.png")
print("1. HTTPS (default theme)")


# --------------------------------------------------------------------------
# 2. Choosing your next language (earth theme)
# --------------------------------------------------------------------------

s = Scene(theme="earth")
s.add("What should I learn next?", role="title")

s.add("Want a job?", role="decision")
s.add("Python", role="end", emphasis="high")
s.add("TypeScript", role="end", emphasis="high")
s.add("Want speed?", role="decision")
s.add("Rust", role="end")
s.add("Go", role="end")

s.connect("Want a job?", "Python", label="data/ML")
s.connect("Want a job?", "TypeScript", label="web")
s.connect("Want a job?", "Want speed?", label="systems")
s.connect("Want speed?", "Rust", label="max control")
s.connect("Want speed?", "Go", label="simplicity")

s.annotate("Most versatile\nchoice in 2025", near="Python")

s.add("There is no wrong answer — just start building", role="caption")
s.layout("decision_tree")
s.save("examples/renders/languages.png")
print("2. Languages (earth theme)")


# --------------------------------------------------------------------------
# 3. How coffee gets made (grape theme)
# --------------------------------------------------------------------------

s = Scene(theme="grape")
s.add("From bean to cup in 4 minutes", role="title")

s.add("Order placed", role="start")
s.add("Grind beans", role="process")
s.add("Pull espresso", role="process", emphasis="high")
s.add("Steam milk", role="process")
s.add("Pour latte art", role="process", emphasis="high")
s.add("Served", role="end", size="large")

s.connect("Order placed", "Grind beans")
s.connect("Grind beans", "Pull espresso")
s.connect("Pull espresso", "Steam milk")
s.connect("Steam milk", "Pour latte art")
s.connect("Pour latte art", "Served")

s.annotate("18g in, 36g out\n25 seconds", near="Pull espresso")
s.annotate("The moment of\ntruth", near="Pour latte art")

s.add("Precision at every step", role="caption")
s.layout("pipeline")
s.save("examples/renders/coffee.png")
print("3. Coffee (grape theme)")


# --------------------------------------------------------------------------
# 4. Startup funding journey (dark theme)
# --------------------------------------------------------------------------

s = Scene(dark=True)
s.add("The startup funding journey", role="title")

s.add("Idea", role="start")
s.add("Build MVP", role="process", emphasis="high")
s.add("Pre-seed", role="process")
s.add("Find market fit", role="decision", size="large")
s.add("Seed Round", role="process", emphasis="high")
s.add("Scale", role="process", size="large")
s.add("Series A", role="end", size="large", emphasis="high")

s.connect("Idea", "Build MVP")
s.connect("Build MVP", "Pre-seed", label="100K-500K")
s.connect("Pre-seed", "Find market fit")
s.connect("Find market fit", "Seed Round", label="traction")
s.connect("Find market fit", "Build MVP", label="pivot", style="dashed")
s.connect("Seed Round", "Scale", label="1-3M")
s.connect("Scale", "Series A", label="5-15M")

s.annotate("Most startups\nloop here", near="Find market fit")

s.add("The path is never straight", role="caption")
s.layout("top_down")
s.save("examples/renders/startup.png")
print("4. Startup (dark theme)")


# --------------------------------------------------------------------------
# 5. How Git works (ocean theme)
# --------------------------------------------------------------------------

s = Scene(theme="ocean")
s.add("How Git tracks your code", role="title")

s.add("Working Directory", role="start", size="large")
s.add("Staging Area", role="process", emphasis="high")
s.add("Local Repository", role="process", size="large")
s.add("Remote Repository", role="end", size="large", emphasis="high")

s.connect("Working Directory", "Staging Area", label="git add")
s.connect("Staging Area", "Local Repository", label="git commit")
s.connect("Local Repository", "Remote Repository", label="git push")
s.connect("Remote Repository", "Working Directory", label="git pull", style="dashed")

s.annotate("Choose what\nto include", near="Staging Area")
s.annotate("GitHub, GitLab,\nBitbucket", near="Remote Repository")

s.add("Every change is tracked, every version recoverable", role="caption")
s.layout("pipeline")
s.save("examples/renders/git.png")
print("5. Git (ocean theme)")


# --------------------------------------------------------------------------
# 6. How the immune system fights a virus (vanilla theme)
# --------------------------------------------------------------------------

s = Scene(theme="vanilla")
s.add("How your immune system fights a virus", role="title")

s.add("Virus enters body", role="start")
s.add("Innate response", role="process")
s.add("Dendritic cells\ndetect threat", role="process", emphasis="high")
s.add("T-cells activated", role="process", size="large", emphasis="high")
s.add("B-cells make\nantibodies", role="process")
s.add("Virus neutralized", role="end", size="large")
s.add("Memory cells\nformed", role="end")

s.connect("Virus enters body", "Innate response")
s.connect("Innate response", "Dendritic cells\ndetect threat")
s.connect("Dendritic cells\ndetect threat", "T-cells activated")
s.connect("T-cells activated", "B-cells make\nantibodies")
s.connect("B-cells make\nantibodies", "Virus neutralized")
s.connect("T-cells activated", "Virus neutralized", label="kill infected cells")
s.connect("Virus neutralized", "Memory cells\nformed", style="dashed")

s.annotate("Takes 7-10 days\nfirst time", near="T-cells activated")
s.annotate("Why vaccines\nwork", near="Memory cells\nformed")

s.add("Elegant, layered, and it remembers", role="caption")
s.layout("top_down")
s.save("examples/renders/immune.png")
print("6. Immune system (vanilla theme)")


# --------------------------------------------------------------------------
# 7. Theme showcase — same diagram, different themes
# --------------------------------------------------------------------------

for theme_name in ["default", "earth", "grape", "ocean", "cool", "mixed"]:
    s = Scene(theme=theme_name)
    s.add("Design", role="start")
    s.add("Build", role="process", emphasis="high")
    s.add("Test", role="decision")
    s.add("Ship", role="end", size="large")

    s.connect("Design", "Build")
    s.connect("Build", "Test")
    s.connect("Test", "Ship", label="pass")
    s.connect("Test", "Build", label="fix", style="dashed")

    s.layout("pipeline")
    s.save(f"examples/renders/theme_{theme_name}.png")

print("7. Theme showcase (6 variations)")


print("\nAll renders in examples/renders/")
