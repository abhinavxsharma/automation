"""Tests for Handshake configuration."""

from handshake_automation.config import Settings, config


def test_default_config() -> None:
    """Verify default Settings initialization."""
    assert "ai.joinhandshake.com" in config.tasks_url
    assert isinstance(config.timeout_ms, int)
    assert isinstance(config.max_tasks, int)
    assert isinstance(config.auto_submit, bool)


def test_custom_settings(mock_settings: Settings) -> None:
    """Verify custom Settings properties."""
    assert mock_settings.timeout_ms == 1000
    assert mock_settings.max_tasks == 5
    assert mock_settings.auto_submit is False
