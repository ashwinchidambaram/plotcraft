from plotcraft.wobble import Wobbler, WobbleConfig
from plotcraft.types import Point


# ---------------------------------------------------------------------------
# Seeded reproducibility
# ---------------------------------------------------------------------------

def test_same_seed_same_wobble_point():
    """Two Wobblers with the same seed produce identical wobble_point output."""
    config = WobbleConfig(seed=7, amplitude=3.0)
    w1 = Wobbler(config)
    w2 = Wobbler(config)
    p = Point(10.0, 20.0)
    assert w1.wobble_point(p) == w2.wobble_point(p)


def test_same_seed_same_rect():
    """Two Wobblers with the same seed produce identical wobble_rect paths."""
    config = WobbleConfig(seed=99)
    w1 = Wobbler(config)
    w2 = Wobbler(config)
    assert w1.wobble_rect(0, 0, 100, 60) == w2.wobble_rect(0, 0, 100, 60)


def test_same_seed_same_circle():
    """Two Wobblers with the same seed produce identical wobble_circle paths."""
    config = WobbleConfig(seed=13)
    w1 = Wobbler(config)
    w2 = Wobbler(config)
    assert w1.wobble_circle(50, 50, 30) == w2.wobble_circle(50, 50, 30)


# ---------------------------------------------------------------------------
# Different seeds produce different output
# ---------------------------------------------------------------------------

def test_different_seeds_different_wobble_point():
    """Different seeds produce different wobble_point results."""
    w1 = Wobbler(WobbleConfig(seed=1))
    w2 = Wobbler(WobbleConfig(seed=2))
    p = Point(50.0, 50.0)
    assert w1.wobble_point(p) != w2.wobble_point(p)


def test_different_seeds_different_rect():
    """Different seeds produce different wobble_rect paths."""
    w1 = Wobbler(WobbleConfig(seed=10))
    w2 = Wobbler(WobbleConfig(seed=20))
    assert w1.wobble_rect(0, 0, 80, 40) != w2.wobble_rect(0, 0, 80, 40)


# ---------------------------------------------------------------------------
# Amplitude bounds
# ---------------------------------------------------------------------------

def test_wobble_point_within_amplitude():
    """wobble_point displacement never exceeds amplitude in either axis."""
    amp = 3.0
    w = Wobbler(WobbleConfig(seed=42, amplitude=amp))
    origin = Point(100.0, 100.0)
    for _ in range(500):
        result = w.wobble_point(origin)
        assert abs(result.x - origin.x) <= amp
        assert abs(result.y - origin.y) <= amp


def test_wobble_point_custom_amplitude_bounds():
    """wobble_point with explicit amplitude respects that amplitude."""
    w = Wobbler(WobbleConfig(seed=5, amplitude=1.0))
    custom_amp = 5.0
    origin = Point(0.0, 0.0)
    for _ in range(300):
        result = w.wobble_point(origin, amplitude=custom_amp)
        assert abs(result.x) <= custom_amp
        assert abs(result.y) <= custom_amp


# ---------------------------------------------------------------------------
# Disabled mode
# ---------------------------------------------------------------------------

def test_disabled_wobble_point_unchanged():
    """wobble_point returns the exact same Point when disabled."""
    w = Wobbler(WobbleConfig(enabled=False))
    p = Point(33.0, 77.0)
    assert w.wobble_point(p) == p


def test_disabled_wobble_bezier_points_unchanged():
    """wobble_bezier_points returns the exact same tuple when disabled."""
    w = Wobbler(WobbleConfig(enabled=False))
    pts = (Point(0.0, 0.0), Point(10.0, 5.0), Point(20.0, 0.0))
    assert w.wobble_bezier_points(pts) == pts


# ---------------------------------------------------------------------------
# Path validity
# ---------------------------------------------------------------------------

def test_wobble_rect_valid_svg_path():
    """wobble_rect returns a path starting with M, ending with Z, containing C."""
    w = Wobbler()
    path = w.wobble_rect(10, 10, 120, 60)
    assert path.startswith("M")
    assert path.endswith("Z")
    assert "C" in path


def test_wobble_circle_valid_svg_path():
    """wobble_circle returns a path starting with M and ending with Z."""
    w = Wobbler()
    path = w.wobble_circle(50, 50, 25)
    assert path.startswith("M")
    assert path.endswith("Z")


def test_wobble_ellipse_valid_svg_path():
    """wobble_ellipse returns a path starting with M and ending with Z."""
    w = Wobbler()
    path = w.wobble_ellipse(40, 40, 30, 15)
    assert path.startswith("M")
    assert path.endswith("Z")


def test_wobble_diamond_valid_svg_path():
    """wobble_diamond returns a path starting with M and ending with Z."""
    w = Wobbler()
    path = w.wobble_diamond(50, 50, 30, 20)
    assert path.startswith("M")
    assert path.endswith("Z")


def test_wobble_polygon_valid_svg_path():
    """wobble_polygon returns a path starting with M and ending with Z."""
    w = Wobbler()
    polygon_pts = [(0.0, 0.0), (50.0, 0.0), (50.0, 50.0), (0.0, 50.0)]
    path = w.wobble_polygon(polygon_pts)
    assert path.startswith("M")
    assert path.endswith("Z")


# ---------------------------------------------------------------------------
# wobble_bezier_points point count
# ---------------------------------------------------------------------------

def test_wobble_bezier_points_preserves_count():
    """wobble_bezier_points returns a tuple with the same number of points."""
    w = Wobbler()
    pts = (Point(0.0, 0.0), Point(10.0, 5.0), Point(20.0, 0.0), Point(30.0, 10.0))
    result = w.wobble_bezier_points(pts)
    assert len(result) == len(pts)


def test_wobble_bezier_points_single_point():
    """wobble_bezier_points works with a single point."""
    w = Wobbler()
    pts = (Point(5.0, 5.0),)
    result = w.wobble_bezier_points(pts)
    assert len(result) == 1


def test_wobble_bezier_points_empty():
    """wobble_bezier_points works with an empty tuple."""
    w = Wobbler()
    pts: tuple[Point, ...] = ()
    result = w.wobble_bezier_points(pts)
    assert result == ()


# ---------------------------------------------------------------------------
# wobble_circle delegates to wobble_ellipse
# ---------------------------------------------------------------------------

def test_wobble_circle_matches_ellipse_equal_radii():
    """wobble_circle(r) produces the same path as wobble_ellipse(rx=r, ry=r)."""
    config = WobbleConfig(seed=17)
    w_circle = Wobbler(config)
    w_ellipse = Wobbler(config)
    circle_path = w_circle.wobble_circle(60, 60, 20)
    ellipse_path = w_ellipse.wobble_ellipse(60, 60, 20, 20)
    assert circle_path == ellipse_path
