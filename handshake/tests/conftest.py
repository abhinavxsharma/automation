"""Pytest fixtures for Handshake AI automation tests."""

import pytest

from handshake_automation.config import Settings


@pytest.fixture
def mock_settings() -> Settings:
    """Fixture providing clean mock Settings."""
    return Settings(
        tasks_url="https://ai.joinhandshake.com/fellow/15f2e875-62ac-492c-9e96-d5569635671a/tasks",
        timeout_ms=1000,
        max_tasks=5,
        auto_submit=False,
        min_time_sec=0,
        openrouter_api_key="test_key",
        gemini_api_key="",
    )
