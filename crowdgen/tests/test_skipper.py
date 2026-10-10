"""Tests for skipper task skipping module."""

from unittest.mock import MagicMock

from playwright.sync_api import Error

from crowdgen_automation.tasks.skipper import skip_task


def test_skip_task_native_button() -> None:
    """Verify skip_task clicks native skip button when present."""
    mock_page = MagicMock()
    mock_skip_btn = MagicMock()
    mock_skip_btn.is_visible.return_value = True

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "Skip" in sel:
            loc.first = mock_skip_btn
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_page.locator.side_effect = locator_side_effect
    res = skip_task(mock_page)
    assert res is True
    mock_skip_btn.click.assert_called_once()


def test_skip_task_fallback_unusable_quality() -> None:
    """Verify skip_task flags issue and unusable quality when native button is absent."""
    mock_page = MagicMock()
    mock_issue = MagicMock()
    mock_unusable = MagicMock()
    mock_submit = MagicMock()
    mock_field = MagicMock()
    mock_confirm = MagicMock()

    mock_issue.is_visible.return_value = True
    mock_unusable.is_visible.return_value = True
    mock_submit.is_visible.return_value = True
    mock_confirm.is_visible.return_value = True

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "Skip" in sel:
            loc.first.is_visible.return_value = False
        elif "Yes, submit" in sel or "Confirm" in sel:
            loc.first = mock_confirm
        elif "Issue" in sel or 'value*="Yes"' in sel:
            loc.first = mock_issue
        elif "Unusable" in sel:
            loc.first = mock_unusable
        elif "caption" in sel or "angle" in sel:
            loc.all.return_value = [mock_field]
            loc.first.is_visible.return_value = False
        elif "Submit" in sel:
            loc.first = mock_submit
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_page.locator.side_effect = locator_side_effect
    res = skip_task(mock_page)
    assert res is True
    mock_issue.click.assert_called_once()
    mock_unusable.click.assert_called_once()
    mock_field.fill.assert_called_with("")
    mock_submit.click.assert_called_once()
    mock_confirm.click.assert_called_once()


def test_skip_task_failure_returns_false() -> None:
    """Verify skip_task returns False if exception occurs and cannot submit."""
    mock_page = MagicMock()
    mock_page.locator.side_effect = Error("Browser disconnected")
    res = skip_task(mock_page)
    assert res is False
