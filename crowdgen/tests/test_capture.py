"""Tests for snapshot and image capture utilities."""

from unittest.mock import MagicMock

from crowdgen_automation.tasks.capture import capture_task_image, get_task_context


def test_get_task_context_direct_page() -> None:
    """Verify returns main page when no maven iframe is present."""
    mock_page = MagicMock()
    mock_page.frames = []
    mock_page.locator.return_value.count.return_value = 0
    ctx = get_task_context(mock_page)
    assert ctx == mock_page


def test_capture_task_image_direct_url() -> None:
    """Verify returns direct URL when src starts with http."""
    mock_ctx = MagicMock()
    mock_loc = MagicMock()
    mock_ctx.locator.return_value.locator.return_value.first = mock_loc
    mock_loc.get_attribute.return_value = "https://images.example.com/item123.jpg"

    kind, ref = capture_task_image(mock_ctx)
    assert kind == "url"
    assert ref == "https://images.example.com/item123.jpg"


def test_capture_task_image_base64_screenshot() -> None:
    """Verify captures screenshot and encodes to base64 when blob or canvas."""
    mock_ctx = MagicMock()
    mock_loc = MagicMock()
    mock_ctx.locator.return_value.locator.return_value.first = mock_loc
    mock_loc.get_attribute.return_value = "blob:https://app.crowdgen.com/abc"
    mock_loc.screenshot.return_value = b"\xff\xd8\xff\xe0testjpegdata"

    kind, ref = capture_task_image(mock_ctx)
    assert kind == "base64"
    assert ref.startswith("data:image/jpeg;base64,")
