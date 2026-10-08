"""Pytest fixtures and configuration for crowdgen tests."""

import pytest

from crowdgen_automation.config import Settings


@pytest.fixture
def mock_settings() -> Settings:
    """Return a predictable mock Settings object."""
    return Settings(
        login_url="https://app.crowdgen.com/login",
        timeout_ms=5000,
        max_tasks=10,
        aht_min_wait_sec=1,
        gemini_api_key="",
        openrouter_api_key="test_key",
        openrouter_base_url="https://openrouter.ai/api/v1",
        openrouter_vision_model="dots-studio/dots-3-note-preview:free",
        openrouter_fallback_model="qwen/qwen3.8-27b:free",
        target_remaining_sec=1,
    )
