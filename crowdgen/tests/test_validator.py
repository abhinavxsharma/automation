"""Tests for validation button and feedback parser."""

from unittest.mock import MagicMock

from crowdgen_automation.tasks.validator import click_validate


def test_click_validate_no_button_passes() -> None:
    """Verify passes cleanly if no explicit validate button exists."""
    mock_ctx = MagicMock()
    mock_ctx.locator.return_value.first.is_visible.return_value = False
    passed, err = click_validate(mock_ctx)
    assert passed is True
    assert err is None


def test_click_validate_success_alert_banner() -> None:
    """Verify returns success when 'VALID - all checks passed' banner is visible."""
    mock_ctx = MagicMock()
    mock_val_btn = MagicMock()
    mock_ok_loc = MagicMock()

    mock_val_btn.is_visible.return_value = True
    mock_ok_loc.is_visible.return_value = True
    mock_ok_loc.inner_text.return_value = "VALID - all checks passed."

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "Validate" in sel:
            loc.first = mock_val_btn
        elif "checks passed" in sel:
            loc.first = mock_ok_loc
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_ctx.locator.side_effect = locator_side_effect
    passed, err = click_validate(mock_ctx)
    assert passed is True
    assert err is None


def test_click_validate_success_submit_enabled() -> None:
    """Verify returns success when submit button becomes enabled."""
    mock_ctx = MagicMock()
    mock_val_btn = MagicMock()
    mock_err_loc = MagicMock()
    mock_sub_loc = MagicMock()

    mock_val_btn.is_visible.return_value = True
    mock_err_loc.is_visible.return_value = False
    mock_sub_loc.is_visible.return_value = True
    mock_sub_loc.get_attribute.return_value = None  # not disabled

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "Validate" in sel:
            loc.first = mock_val_btn
        elif "Submit" in sel:
            loc.first = mock_sub_loc
        elif "INVALID" in sel or "error" in sel:
            loc.first = mock_err_loc
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_ctx.locator.side_effect = locator_side_effect
    passed, err = click_validate(mock_ctx)
    assert passed is True
    assert err is None
    mock_val_btn.click.assert_called_once()


def test_click_validate_error_detected() -> None:
    """Verify returns error message when validation error appears."""
    mock_ctx = MagicMock()
    mock_val_btn = MagicMock()
    mock_err_loc = MagicMock()

    mock_val_btn.is_visible.return_value = True
    mock_err_loc.is_visible.return_value = True
    mock_err_loc.inner_text.return_value = "Long description must have at least 50 words"

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "Validate" in sel:
            loc.first = mock_val_btn
        elif "INVALID" in sel or "error" in sel:
            loc.first = mock_err_loc
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_ctx.locator.side_effect = locator_side_effect
    passed, err = click_validate(mock_ctx)
    assert passed is False
    assert err == "Long description must have at least 50 words"


def test_click_validate_subjective_language_error() -> None:
    """Verify INVALID - DETAILED subjective language is caught and never misidentified as valid."""
    mock_ctx = MagicMock()
    mock_val_btn = MagicMock()
    mock_err_loc = MagicMock()

    mock_val_btn.is_visible.return_value = True
    mock_err_loc.is_visible.return_value = True
    mock_err_loc.inner_text.return_value = (
        "INVALID - DETAILED [subjective_language]: contrast beautifully with the soft, sparkling texture"
    )

    def locator_side_effect(sel: str) -> MagicMock:
        loc = MagicMock()
        if "Validate" in sel:
            loc.first = mock_val_btn
        elif "INVALID" in sel:
            loc.first = mock_err_loc
        else:
            loc.first.is_visible.return_value = False
        return loc

    mock_ctx.locator.side_effect = locator_side_effect
    passed, err = click_validate(mock_ctx)
    assert passed is False
    assert "contrast beautifully" in str(err)
