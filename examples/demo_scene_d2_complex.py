"""Complex D2 diagrams to stress-test the Scene API."""

from plotcraft.scene import Scene

# --------------------------------------------------------------------------
# 1. Microservices Architecture (12 elements, 3 tiers, many connections)
# --------------------------------------------------------------------------

s = Scene()
s.add("How a ride request becomes a driver match", role="title")

# Client tier
s.add("Mobile App", role="start", size="large")
s.add("API Gateway", role="process", emphasis="high")

# Service tier
s.add("Auth Service", role="process")
s.add("Ride Matcher", role="process", size="large", emphasis="high")
s.add("Pricing Engine", role="process")
s.add("Notification", role="process")

# Data tier
s.add("User DB", role="end")
s.add("Ride Queue", role="end")
s.add("Cache", role="process", emphasis="low")

# Flow
s.connect("Mobile App", "API Gateway")
s.connect("API Gateway", "Auth Service")
s.connect("API Gateway", "Ride Matcher", weight="bold")
s.connect("API Gateway", "Pricing Engine")
s.connect("Ride Matcher", "Ride Queue", label="enqueue")
s.connect("Ride Matcher", "Notification", label="push alert")
s.connect("Auth Service", "User DB")
s.connect("Ride Matcher", "Cache", style="dashed")
s.connect("Pricing Engine", "Ride Matcher", label="surge price", style="dashed")

s.annotate("JWT validation", near="Auth Service")
s.annotate("< 200ms p99", near="Ride Matcher")

s.add("12 services, 1 request path, sub-second matching", role="caption")
s.layout("fan_out")
s.save("examples/renders/d2_microservices.svg", engine="d2")
print("1. Microservices done")


# --------------------------------------------------------------------------
# 2. CI/CD Pipeline with failure branches (decision + cycle + pipeline)
# --------------------------------------------------------------------------

s = Scene()
s.add("From commit to production in 8 minutes", role="title")

s.add("Push", role="start")
s.add("Lint", role="process")
s.add("Unit Tests", role="process", emphasis="high")
s.add("Build Image", role="process")
s.add("Security Scan", role="decision")
s.add("Stage Deploy", role="process", size="large")
s.add("Smoke Tests", role="decision")
s.add("Prod Deploy", role="end", size="large", emphasis="high")
s.add("Rollback", role="process", emphasis="low")

s.connect("Push", "Lint")
s.connect("Lint", "Unit Tests")
s.connect("Unit Tests", "Build Image")
s.connect("Build Image", "Security Scan")
s.connect("Security Scan", "Stage Deploy", label="pass")
s.connect("Security Scan", "Rollback", label="fail", style="dashed")
s.connect("Stage Deploy", "Smoke Tests")
s.connect("Smoke Tests", "Prod Deploy", label="pass", weight="bold")
s.connect("Smoke Tests", "Rollback", label="fail", style="dashed")
s.connect("Rollback", "Push", label="retry", style="dotted")

s.annotate("Parallel across 3 runners", near="Unit Tests")
s.annotate("Canary then full rollout", near="Prod Deploy")

s.add("Automated guardrails at every stage", role="caption")
s.layout("pipeline")
s.save("examples/renders/d2_cicd.svg", engine="d2")
print("2. CI/CD done")


# --------------------------------------------------------------------------
# 3. Event Sourcing (convergence + fan-out combined)
# --------------------------------------------------------------------------

s = Scene()
s.add("How event sourcing replaces CRUD", role="title")

# Commands come in
s.add("API Request", role="start")
s.add("Command Handler", role="process", emphasis="high")
s.add("Validate", role="decision")
s.add("Event Store", role="process", size="large", emphasis="high")

# Projections fan out
s.add("Read Model", role="process")
s.add("Search Index", role="process")
s.add("Analytics", role="process", emphasis="low")
s.add("Notifications", role="end")

s.connect("API Request", "Command Handler")
s.connect("Command Handler", "Validate")
s.connect("Validate", "Event Store", label="accepted")
s.connect("Event Store", "Read Model", label="project")
s.connect("Event Store", "Search Index", label="index")
s.connect("Event Store", "Analytics", label="aggregate")
s.connect("Event Store", "Notifications", label="trigger")
s.connect("Validate", "API Request", label="rejected", style="dashed")

s.annotate("Append-only log", near="Event Store")
s.annotate("Eventually consistent", near="Read Model")

s.add("Write once, read many ways", role="caption")
s.layout("top_down")
s.save("examples/renders/d2_eventsourcing.svg", engine="d2")
print("3. Event Sourcing done")


# --------------------------------------------------------------------------
# 4. ML Training Loop (cycle with branching) — dark theme
# --------------------------------------------------------------------------

s = Scene(dark=True)
s.add("Training a production ML model", role="title")

s.add("Raw Dataset", role="start", size="large")
s.add("Feature Pipeline", role="process", emphasis="high")
s.add("Train", role="process", size="large")
s.add("Evaluate", role="decision", size="large")
s.add("Champion Model", role="end", size="large", emphasis="high")
s.add("Shadow Deploy", role="process")
s.add("A/B Test", role="decision")
s.add("Promote", role="end")

s.connect("Raw Dataset", "Feature Pipeline")
s.connect("Feature Pipeline", "Train", weight="bold")
s.connect("Train", "Evaluate")
s.connect("Evaluate", "Train", label="retrain", style="dashed")
s.connect("Evaluate", "Champion Model", label="beats baseline", weight="bold")
s.connect("Champion Model", "Shadow Deploy")
s.connect("Shadow Deploy", "A/B Test")
s.connect("A/B Test", "Promote", label="wins")
s.connect("A/B Test", "Train", label="loses", style="dashed")

s.annotate("GPU cluster", near="Train")
s.annotate("5% traffic", near="Shadow Deploy")

s.add("Every model earns its place through evidence", role="caption")
s.layout("top_down")
s.save("examples/renders/d2_ml_training.svg", engine="d2")
print("4. ML Training done")


# --------------------------------------------------------------------------
# 5. OAuth2 Authorization Code Flow (detailed protocol)
# --------------------------------------------------------------------------

s = Scene()
s.add("How OAuth2 authorization code flow works", role="title")

s.add("User clicks Login", role="start")
s.add("Redirect to IdP", role="process")
s.add("User authenticates", role="process", emphasis="high")
s.add("Authorization code", role="process")
s.add("Exchange for tokens", role="process", emphasis="high")
s.add("Access Token", role="end", emphasis="high")
s.add("Refresh Token", role="end", emphasis="low")
s.add("Call API", role="process")

s.connect("User clicks Login", "Redirect to IdP")
s.connect("Redirect to IdP", "User authenticates")
s.connect("User authenticates", "Authorization code", label="consent granted")
s.connect("Authorization code", "Exchange for tokens", label="backend POST")
s.connect("Exchange for tokens", "Access Token")
s.connect("Exchange for tokens", "Refresh Token")
s.connect("Access Token", "Call API", label="Bearer header")
s.connect("Refresh Token", "Exchange for tokens", label="on expiry", style="dashed")

s.annotate("PKCE protects\nthis step", near="Authorization code")
s.annotate("Short-lived (1h)", near="Access Token")

s.add("The code never sees the browser, tokens never leave the backend", role="caption")
s.layout("pipeline")
s.save("examples/renders/d2_oauth.svg", engine="d2")
print("5. OAuth2 done")


print("\nAll complex renders in examples/renders/")
