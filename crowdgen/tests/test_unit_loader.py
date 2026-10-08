"""Tests for Maven unit transition and availability loader."""

from unittest.mock import MagicMock

from crowdgen_automation.tasks.unit_loader import (
    get_current_unit_id,
    handle_no_units_available,
    wait_for_new_unit,
)


def test_get_current_unit_id_from_url() -> None:
    """Verify extracts unit id from annotate URL path."""
    mock_page = MagicMock()
    mock_page.url = "https://example.com/annotate/15cefe2c-e76b-460a-9d08-d175423deb90?mode=test"
    assert get_current_unit_id(mock_page) == "15cefe2c-e76b-460a-9d08-d175423deb90"


def test_get_current_unit_id_from_dom() -> None:
    """Verify extracts unit id from footer bar text."""
    mock_page = MagicMock()
    mock_page.url = "https://example.com/dashboard"
    mock_loc = MagicMock()
    mock_loc.is_visible.return_value = True
    mock_loc.inner_text.return_value = "Unit 35a1c0f5-68ea-4be6-8cd1-1a093181c297"
    mock_page.locator.return_value.first = mock_loc
    assert get_current_unit_id(mock_page) == "Unit 35a1c0f5-68ea-4be6-8cd1-1a093181c297"


def test_handle_no_units_available_when_none_present() -> None:
    """Verify does nothing when units are present."""
    mock_page = MagicMock()
    mock_page.locator.return_value.first.is_visible.return_value = False
    handle_no_units_available(mock_page, wait_sec=1)
    mock_page.reload.assert_not_called()


def test_wait_for_new_unit_detects_transition() -> None:
    """Verify returns new unit when unit id changes."""
    mock_page = MagicMock()
    mock_page.url = "https://example.com/annotate/new-unit-uuid"
    mock_img = MagicMock()
    mock_img.is_visible.return_value = True

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "img" in sel:
            loc.first = mock_img
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_page.locator.side_effect = locator_side_effect
    unit = wait_for_new_unit(mock_page, prev_unit="old-unit-uuid", timeout_sec=5)
    assert unit == "new-unit-uuid"
