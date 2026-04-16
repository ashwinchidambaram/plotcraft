"""Excalidraw → PNG/SVG renderer.

Requires the `render` extra: pip install plotcraft[render]
This installs Playwright; you'll also need to install the Chromium binary:
    playwright install chromium
"""
from __future__ import annotations

import json
from pathlib import Path


_RENDER_TEMPLATE = Path(__file__).parent / "render_template.html"


def _check_playwright() -> None:
    """Raise a helpful error if Playwright isn't installed."""
    try:
        import playwright.sync_api  # noqa: F401
    except ImportError:
        raise ImportError(
            "PNG/SVG rendering requires Playwright.\n"
            "Install it: pip install plotcraft[render]\n"
            "Then install Chromium: playwright install chromium"
        )


def render_excalidraw_to_png(
    excalidraw_path: str | Path,
    output_path: str | Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
) -> Path:
    """Render an Excalidraw JSON file to PNG.

    Args:
        excalidraw_path: Path to the .excalidraw JSON file.
        output_path: Output PNG path. Defaults to the same name with .png.
        scale: Device scale factor (default 2 for high-DPI).
        max_width: Max viewport width in pixels.

    Returns:
        Path to the rendered PNG.
    """
    _check_playwright()
    from playwright.sync_api import sync_playwright

    excalidraw_path = Path(excalidraw_path)
    if output_path is None:
        output_path = excalidraw_path.with_suffix(".png")
    output_path = Path(output_path)

    with open(excalidraw_path) as f:
        data = json.load(f)
    if data.get("type") != "excalidraw":
        raise ValueError(f"Not an Excalidraw file: {excalidraw_path}")

    elements = data.get("elements", [])
    if not elements:
        raise ValueError("No elements in Excalidraw file")

    # Compute bounding box
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")
    for el in elements:
        if el.get("isDeleted"):
            continue
        x, y = el.get("x", 0), el.get("y", 0)
        w, h = el.get("width", 0), el.get("height", 0)
        if el.get("type") in ("arrow", "line"):
            for px, py in el.get("points", [[0, 0]]):
                min_x = min(min_x, x + px); min_y = min(min_y, y + py)
                max_x = max(max_x, x + px); max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x); min_y = min(min_y, y)
            max_x = max(max_x, x + w); max_y = max(max_y, y + h)

    if min_x == float("inf"):
        min_x, min_y, max_x, max_y = 0, 0, 800, 600

    pad = 80
    width = min(int(max_x - min_x + pad * 2), max_width)
    height = int(max_y - min_y + pad * 2)
    template_uri = _RENDER_TEMPLATE.absolute().as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
        )
        page.goto(template_uri)
        page.wait_for_function("window.__moduleReady === true", timeout=30000)
        result = page.evaluate(
            "async (data) => await window.renderDiagram(data)", data
        )
        if not result.get("success"):
            browser.close()
            raise RuntimeError(f"Render failed: {result.get('error')}")
        page.wait_for_function("window.__renderComplete === true", timeout=15000)
        svg_element = page.query_selector("#root svg")
        if svg_element is None:
            browser.close()
            raise RuntimeError("No SVG produced")
        svg_element.screenshot(path=str(output_path), omit_background=False)
        browser.close()

    return output_path


def render_excalidraw_to_svg(
    excalidraw_path: str | Path,
    output_path: str | Path | None = None,
) -> Path:
    """Render an Excalidraw JSON file to SVG."""
    _check_playwright()
    from playwright.sync_api import sync_playwright

    excalidraw_path = Path(excalidraw_path)
    if output_path is None:
        output_path = excalidraw_path.with_suffix(".svg")
    output_path = Path(output_path)

    with open(excalidraw_path) as f:
        data = json.load(f)

    template_uri = _RENDER_TEMPLATE.absolute().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(template_uri)
        page.wait_for_function("window.__moduleReady === true", timeout=30000)
        result = page.evaluate(
            "async (data) => await window.renderDiagram(data)", data
        )
        if not result.get("success"):
            browser.close()
            raise RuntimeError(f"Render failed: {result.get('error')}")
        svg_html = page.evaluate("document.querySelector('#root svg').outerHTML")
        browser.close()

    with open(output_path, "w") as f:
        f.write(svg_html)
    return output_path


def main() -> None:
    """CLI entry point: python -m plotcraft.render path.excalidraw"""
    import argparse
    parser = argparse.ArgumentParser(description="Render Excalidraw JSON to PNG/SVG")
    parser.add_argument("input", help="Path to .excalidraw file")
    parser.add_argument("-o", "--output", help="Output path")
    parser.add_argument("-f", "--format", choices=["png", "svg"], default="png")
    parser.add_argument("-s", "--scale", type=int, default=2)
    args = parser.parse_args()
    if args.format == "svg":
        out = render_excalidraw_to_svg(args.input, args.output)
    else:
        out = render_excalidraw_to_png(args.input, args.output, scale=args.scale)
    print(out)


if __name__ == "__main__":
    main()
