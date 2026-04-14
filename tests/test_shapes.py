import math
import pytest
from plotcraft.types import ShapeKind, TextRole, AnchorName
from plotcraft.shapes import create_shape, Shape


def test_rect_contains_text():
    """Rect content_bbox is larger than text_size + padding."""
    shape = create_shape("r1", "Hello World", kind=ShapeKind.RECT, padding=20)
    assert shape.content_bbox.width >= shape.text_size.width + 40
    assert shape.content_bbox.height >= shape.text_size.height + 40


def test_square_is_square():
    """Square has equal width and height."""
    shape = create_shape("s1", "Test", kind=ShapeKind.SQUARE)
    assert shape.content_bbox.width == shape.content_bbox.height


def test_circle_encloses_text():
    """Circle diameter >= diagonal of text bbox."""
    shape = create_shape("c1", "Circle Text", kind=ShapeKind.CIRCLE, padding=20)
    diagonal = math.sqrt(shape.text_size.width**2 + shape.text_size.height**2)
    assert shape.content_bbox.width >= diagonal + 40  # 2*padding


def test_oval_wider_for_wide_text():
    """Oval with wide text should be wider than tall."""
    shape = create_shape("o1", "This is a wider piece of text", kind=ShapeKind.OVAL)
    # Wide text should make width > height
    assert shape.content_bbox.width > shape.content_bbox.height


def test_anchor_count():
    """Every shape exposes exactly 9 anchors."""
    shape = create_shape("a1", "Anchors")
    assert len(shape.anchors()) == 9


def test_anchor_top_center():
    """TOP_CENTER is at (width/2, 0) relative to bbox origin."""
    shape = create_shape("t1", "Test")
    tc = shape.anchor(AnchorName.TOP_CENTER)
    assert tc.x == pytest.approx(shape.content_bbox.width / 2)
    assert tc.y == pytest.approx(0.0)


def test_anchor_symmetry():
    """LEFT_CENTER.x == 0, RIGHT_CENTER.x == width."""
    shape = create_shape("sym", "Symmetric")
    assert shape.anchor(AnchorName.LEFT_CENTER).x == pytest.approx(0.0)
    assert shape.anchor(AnchorName.RIGHT_CENTER).x == pytest.approx(shape.content_bbox.width)


def test_title_larger_than_body():
    """Same text with TITLE role produces larger shape than BODY."""
    title = create_shape("t", "Same Text", role=TextRole.TITLE)
    body = create_shape("b", "Same Text", role=TextRole.BODY)
    assert title.content_bbox.width > body.content_bbox.width
    assert title.content_bbox.height > body.content_bbox.height


def test_long_text_wraps():
    """Text exceeding max_text_width wraps, making shape taller."""
    short = create_shape("short", "Hi", max_text_width=200)
    long_shape = create_shape("long", "This is a very long piece of text that should definitely wrap to multiple lines", max_text_width=200)
    assert long_shape.content_bbox.height > short.content_bbox.height
    assert len(long_shape.wrapped_lines) > 1


def test_shape_is_frozen():
    """Shape attributes cannot be mutated."""
    shape = create_shape("f1", "Frozen")
    with pytest.raises(AttributeError):
        shape.id = "changed"


def test_none_smaller_bbox_than_rect():
    """NONE creates valid shape with smaller bbox than RECT for same text."""
    none_shape = create_shape("n1", "Label Text", kind=ShapeKind.NONE, padding=20)
    rect_shape = create_shape("r2", "Label Text", kind=ShapeKind.RECT, padding=20)
    assert none_shape.content_bbox.width > 0
    assert none_shape.content_bbox.height > 0
    assert none_shape.content_bbox.width < rect_shape.content_bbox.width
    assert none_shape.content_bbox.height < rect_shape.content_bbox.height


def test_none_bbox_nonzero():
    """NONE shape still has a non-zero bounding box."""
    shape = create_shape("n2", "Tiny", kind=ShapeKind.NONE)
    assert shape.content_bbox.width > 0
    assert shape.content_bbox.height > 0


def test_diamond_creates_successfully():
    """DIAMOND shape creates with valid dimensions."""
    shape = create_shape("d1", "Decision?", kind=ShapeKind.DIAMOND)
    assert shape.kind == ShapeKind.DIAMOND
    assert shape.content_bbox.width > 0
    assert shape.content_bbox.height > 0


def test_diamond_bbox_larger_than_rect():
    """DIAMOND bbox is larger than RECT for same text due to 1.5x multiplier."""
    diamond = create_shape("d1", "Same Text", kind=ShapeKind.DIAMOND, padding=20)
    rect = create_shape("r1", "Same Text", kind=ShapeKind.RECT, padding=20)
    assert diamond.content_bbox.width > rect.content_bbox.width
    assert diamond.content_bbox.height > rect.content_bbox.height


def test_all_shape_kinds():
    """All ShapeKind values produce valid shapes."""
    for kind in ShapeKind:
        shape = create_shape(f"k_{kind.value}", "Test", kind=kind)
        assert shape.content_bbox.width > 0
        assert shape.content_bbox.height > 0


def test_title_short_text_meets_minimums():
    """TITLE with short text ('Hi') meets minimum width/height from RoleScale."""
    shape = create_shape("t_min", "Hi", role=TextRole.TITLE)
    assert shape.content_bbox.width >= 280
    assert shape.content_bbox.height >= 80


def test_title_larger_than_body_same_text_role_scale():
    """TITLE is larger than BODY with the same text due to role scale."""
    title = create_shape("t_rs", "Hi", role=TextRole.TITLE)
    body = create_shape("b_rs", "Hi", role=TextRole.BODY)
    assert title.content_bbox.width > body.content_bbox.width
    assert title.content_bbox.height > body.content_bbox.height


def test_body_long_text_grows_beyond_minimums():
    """BODY with long text still grows beyond role scale minimums."""
    shape = create_shape(
        "b_long",
        "This is a very long piece of text that should definitely cause the shape to grow well beyond any minimum dimensions",
        role=TextRole.BODY,
        max_text_width=400,
    )
    # BODY minimums are 0, but text content should push dimensions up significantly
    assert shape.content_bbox.width > 100
    assert shape.content_bbox.height > 0


def test_caption_less_padding_than_body():
    """CAPTION has less padding than BODY due to smaller padding_multiplier."""
    caption = create_shape("c_pad", "Same Text", role=TextRole.CAPTION)
    body = create_shape("b_pad", "Same Text", role=TextRole.BODY)
    # Caption padding_multiplier=0.8 < Body padding_multiplier=1.0
    # Caption also has smaller font, so text_size differs; compare padding contribution
    # With same padding base, caption's scaled padding is smaller
    caption_padding_w = caption.content_bbox.width - caption.text_size.width
    body_padding_w = body.content_bbox.width - body.text_size.width
    assert caption_padding_w < body_padding_w
