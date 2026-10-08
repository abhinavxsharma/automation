"""Tests for crowdgen_automation configuration."""

from crowdgen_automation.config import Settings, config


def test_default_config_fields() -> None:
    """Verify default global configuration fields exist and are typed."""
    assert isinstance(config.login_url, str)
    assert isinstance(config.timeout_ms, int)
    assert isinstance(config.max_tasks, int)
    assert isinstance(config.aht_min_wait_sec, int)
    assert isinstance(config.openrouter_vision_model, str)
    assert isinstance(config.target_remaining_sec, int)


def test_custom_settings(mock_settings: Settings) -> None:
    """Verify custom settings overrides."""
    assert mock_settings.timeout_ms == 5000
    assert mock_settings.max_tasks == 10
    assert mock_settings.aht_min_wait_sec == 1
    assert mock_settings.target_remaining_sec == 1
    assert mock_settings.openrouter_api_key == "test_key"
