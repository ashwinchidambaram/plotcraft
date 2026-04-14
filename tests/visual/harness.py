"""Visual test harness — renders PlotCraft diagrams as screenshots via Playwright."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from plotcraft.diagram import Diagram


@dataclass
class VisualScenario:
    """A visual test scenario with expected/unexpected behavior constraints."""
    name: str
    description: str
    build_diagram: Callable[[], Diagram]
    expected_behaviors: list[str] = field(default_factory=list)
    unexpected_behaviors: list[str] = field(default_factory=list)


def render_screenshot(diagram: Diagram, name: str = "diagram", output_dir: str | None = None) -> Path:
    """Render a diagram to SVG, load in Chromium with fonts, screenshot as PNG.

    Returns path to the PNG screenshot.
    """
    from playwright.sync_api import sync_playwright

    svg_content = diagram.render()

    # Wrap SVG in HTML that loads Google Fonts
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Patrick+Hand&family=Indie+Flower&display=swap');
body {{
    margin: 0;
    padding: 20px;
    background: #fdf6e3;
    display: flex;
    justify-content: center;
}}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""

    # Write HTML to temp file
    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
    else:
        out = Path(tempfile.mkdtemp(prefix="plotcraft_visual_"))

    html_path = out / f"{name}.html"
    html_path.write_text(html)

    screenshot_path = out / f"{name}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(f"file://{html_path.absolute()}")

        # Wait for fonts to load
        page.wait_for_function("document.fonts.ready.then(() => true)", timeout=10000)
        # Small extra wait for rendering
        page.wait_for_timeout(500)

        # Screenshot the full page
        page.screenshot(path=str(screenshot_path), full_page=True)
        browser.close()

    return screenshot_path
