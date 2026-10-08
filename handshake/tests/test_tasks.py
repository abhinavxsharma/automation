"""Tests for Handshake task interaction modules."""

from unittest.mock import MagicMock, patch

from handshake_automation.config import Settings
from handshake_automation.tasks.distractors_filler import (
    fill_answer_format,
    fill_distractors,
)
from handshake_automation.tasks.domain_selector import (
    select_subdomain,
    set_source_and_license,
)
from handshake_automation.tasks.failure_justifier import fill_failure_justifications
from handshake_automation.tasks.form_filler import fill_step_input
from handshake_automation.tasks.model_tester import verify_model_failures
from handshake_automation.tasks.navigator import claim_or_resume_task, start_task_timer
from handshake_automation.tasks.submitter import confirm_and_submit
from handshake_automation.tasks.task_builder import build_lumiere_task


def test_start_task_timer() -> None:
    """Verify timer start button click."""
    mock_page = MagicMock()
    mock_btn = MagicMock()
    mock_btn.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_btn
    assert start_task_timer(mock_page) is True
    mock_btn.click.assert_called_once()


def test_claim_or_resume_task() -> None:
    """Verify resumes active task or claims available."""
    mock_page = MagicMock()
    mock_page.url = "https://ai.joinhandshake.com/tasks"
    mock_elem = MagicMock()
    mock_elem.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_elem

    assert claim_or_resume_task(mock_page, "https://ai.joinhandshake.com/tasks") is True


def test_select_subdomain() -> None:
    """Verify subdomain clicks."""
    mock_page = MagicMock()
    mock_elem = MagicMock()
    mock_elem.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_elem
    assert select_subdomain(mock_page) is True


def test_set_source_and_license() -> None:
    """Verify setting source and license."""
    mock_page = MagicMock()
    mock_elem = MagicMock()
    mock_elem.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_elem
    mock_page.locator.return_value.all.return_value = []
    assert set_source_and_license(mock_page) is True


def test_model_tester() -> None:
    """Verify testing models and confirming failure."""
    mock_page = MagicMock()
    mock_elem = MagicMock()
    mock_elem.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_elem
    assert verify_model_failures(mock_page) is True


def test_fill_failure_justifications() -> None:
    """Verify filling failure justification."""
    mock_page = MagicMock()
    mock_elem = MagicMock()
    mock_elem.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_elem
    assert fill_failure_justifications(mock_page, "Spatial", "Model miscalculated span.") is True


def test_fill_step_input() -> None:
    """Verify filling step input text."""
    mock_page = MagicMock()
    mock_inp = MagicMock()
    mock_inp.is_visible.return_value = True
    mock_inp.input_value.return_value = ""
    mock_page.locator.return_value.all.return_value = [mock_inp]
    mock_btn = MagicMock()
    mock_btn.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_btn

    assert fill_step_input(mock_page, "Sample text") is True


def test_fill_distractors() -> None:
    """Verify filling distractors."""
    mock_page = MagicMock()
    mock_inp = MagicMock()
    mock_inp.is_visible.return_value = True
    mock_page.locator.return_value.all.return_value = [mock_inp] * 5
    mock_btn = MagicMock()
    mock_btn.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_btn

    assert fill_distractors(mock_page, ["1", "2", "3", "4", "5"]) is True


def test_fill_answer_format() -> None:
    """Verify setting answer format."""
    mock_page = MagicMock()
    mock_inp = MagicMock()
    mock_inp.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_inp

    assert fill_answer_format(mock_page, "Decimal", 2) is True


def test_confirm_and_submit() -> None:
    """Verify confirming time and final submission."""
    mock_page = MagicMock()
    mock_btn = MagicMock()
    mock_btn.is_visible.return_value = True
    mock_page.locator.return_value.first = mock_btn

    with patch("time.sleep"):
        assert confirm_and_submit(mock_page, start_time=0.0, auto_submit=True, min_time_sec=0) is True


def test_task_builder() -> None:
    """Verify building complete lumiere task."""
    cfg = Settings(openrouter_api_key="mock", gemini_api_key="mock")
    with patch("handshake_automation.tasks.ai_author.author_task") as mock_author:
        mock_author.return_value = {
            "prompt": "Test prompt",
            "gtfa": "10.0",
            "image_description": "Test description",
            "solution": "Step 1...",
            "distractors": ["1", "2", "3", "4", "5"],
            "failure_justification": "Failed",
        }
        task = build_lumiere_task(cfg)
        assert task["is_original"] is True
        assert task["prompt"] == "Test prompt"


def test_nasa_jpl_rule_4_line_limit() -> None:
    """Verify that all production files in handshake_automation adhere to <= 60 lines."""
    from pathlib import Path

    pkg_root = Path("handshake_automation")
    oversized = []
    for py_file in pkg_root.rglob("*.py"):
        lines = len(py_file.read_text(encoding="utf-8").splitlines())
        if lines > 60:
            oversized.append(f"{py_file.name} ({lines} lines)")
    assert not oversized, f"Production files exceeding 60 lines: {oversized}"


def test_dag_solver_and_artifacts(tmp_path) -> None:
    """Verify DAG diagram generation, critical path solver, and artifact builder."""
    from handshake_automation.tasks.cs_diagram_creator import (
        create_network_flow_diagram,
    )
    from handshake_automation.tasks.problem_solver import solve_network_flow_task

    diag_file = tmp_path / "test_dag.png"
    info = create_network_flow_diagram(diag_file)
    assert diag_file.exists()
    assert info["supertype"] == "Computer Science"

    artifacts = solve_network_flow_task(info)
    assert artifacts["gtfa"] == "76"
    assert "75" in artifacts["distractors"]
    assert artifacts["answer_format"] == "Integer"
    assert "critical path" in artifacts["prompt"].lower()
    assert len(artifacts["distractors"]) >= 4


