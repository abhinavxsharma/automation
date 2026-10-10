"""Tests for task coordinator lifecycle."""

from unittest.mock import MagicMock, patch

from crowdgen_automation.config import Settings
from crowdgen_automation.tasks.coordinator import process_single_task


def test_process_single_task_success_first_attempt(mock_settings: Settings) -> None:
    """Verify single task succeeds on first attempt if validation passes."""
    mock_page = MagicMock()
    with (
        patch("crowdgen_automation.tasks.coordinator.get_task_context", return_value=mock_page),
        patch("crowdgen_automation.tasks.coordinator.capture_task_image", return_value=("url", "http://img.jpg")),
        patch("crowdgen_automation.tasks.coordinator.generate_captions", return_value={"short_caption": "S", "detailed_caption": "D"}),
        patch("crowdgen_automation.tasks.coordinator.fill_maven_form") as mock_fill,
        patch("crowdgen_automation.tasks.coordinator.click_validate", return_value=(True, None)),
        patch("crowdgen_automation.tasks.coordinator.submit_task", return_value=True) as mock_sub,
    ):
        res = process_single_task(mock_page, mock_settings, auto_submit=True)
        assert res is True
        mock_fill.assert_called_once()
        mock_sub.assert_called_once()


def test_process_single_task_retries_on_validation_failure(mock_settings: Settings) -> None:
    """Verify single task retries and passes validation error to prompt."""
    mock_page = MagicMock()
    with (
        patch("crowdgen_automation.tasks.coordinator.get_task_context", return_value=mock_page),
        patch("crowdgen_automation.tasks.coordinator.capture_task_image", return_value=("url", "http://img.jpg")),
        patch("crowdgen_automation.tasks.coordinator.generate_captions", return_value={"short_caption": "S", "detailed_caption": "D"}) as mock_vlm,
        patch("crowdgen_automation.tasks.coordinator.fill_maven_form"),
        patch("crowdgen_automation.tasks.coordinator.click_validate", side_effect=[(False, "Too short"), (True, None)]),
        patch("crowdgen_automation.tasks.coordinator.submit_task", return_value=True),
    ):
        res = process_single_task(mock_page, mock_settings, auto_submit=True)
        assert res is True
        assert mock_vlm.call_count == 2
        assert mock_vlm.call_args_list[1][1]["error_feedback"] == "Too short"


def test_process_single_task_skips_after_two_failures(mock_settings: Settings) -> None:
    """Verify single task skips when 2 attempts fail validation."""
    mock_page = MagicMock()
    with (
        patch("crowdgen_automation.tasks.coordinator.get_task_context", return_value=mock_page),
        patch("crowdgen_automation.tasks.coordinator.capture_task_image", return_value=("url", "http://img.jpg")),
        patch("crowdgen_automation.tasks.coordinator.generate_captions", return_value={"short_caption": "S", "detailed_caption": "D"}) as mock_vlm,
        patch("crowdgen_automation.tasks.coordinator.fill_maven_form"),
        patch("crowdgen_automation.tasks.coordinator.click_validate", side_effect=[(False, "Error 1"), (False, "Error 2")]),
        patch("crowdgen_automation.tasks.coordinator.skip_task", return_value=True) as mock_skip,
    ):
        res = process_single_task(mock_page, mock_settings, auto_submit=True)
        assert res is True
        assert mock_vlm.call_count == 2
        mock_skip.assert_called_once_with(mock_page, mock_page)


def test_process_single_task_skips_dense_document(mock_settings: Settings) -> None:
    """Verify single task immediately skips when detected as dense document."""
    mock_page = MagicMock()
    with (
        patch("crowdgen_automation.tasks.coordinator.get_task_context", return_value=mock_page),
        patch("crowdgen_automation.tasks.coordinator.capture_task_image", return_value=("url", "http://img.jpg")),
        patch("crowdgen_automation.tasks.coordinator.generate_captions", return_value={"is_dense": True}),
        patch("crowdgen_automation.tasks.coordinator.fill_maven_form") as mock_fill,
        patch("crowdgen_automation.tasks.coordinator.skip_task", return_value=True) as mock_skip,
    ):
        res = process_single_task(mock_page, mock_settings, auto_submit=True)
        assert res is True
        mock_skip.assert_called_once_with(mock_page, mock_page)
        mock_fill.assert_not_called()
