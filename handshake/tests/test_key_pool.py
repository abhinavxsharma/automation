"""Tests for Handshake key pool and rotation management."""

import time
from pathlib import Path
from unittest.mock import patch

from handshake_automation.tasks.key_pool import (
    get_active_key,
    load_keys,
    mark_key_exhausted,
    reset_pool,
)


def test_load_keys(tmp_path: Path) -> None:
    """Verify loading keys from file and environment."""
    keys_file = tmp_path / "keys.txt"
    keys_file.write_text("# comment\nk1\n\nk2\nk1\n", encoding="utf-8")
    with patch.dict("os.environ", {"OPENROUTER_API_KEYS": "k_env,k2"}):
        keys = load_keys(str(keys_file), extra_keys=["k_extra"])
        assert keys == ["k1", "k2", "k_env", "k_extra"]


def test_key_rotation_and_cooldown() -> None:
    """Verify rotation on exhausted keys and cooldown reset."""
    reset_pool()
    keys = ["k1", "k2"]
    assert get_active_key(keys) == "k1"

    mark_key_exhausted("k1", cooldown_sec=10.0)
    assert get_active_key(keys) == "k2"

    mark_key_exhausted("k2", cooldown_sec=10.0)
    assert get_active_key(keys) is None

    reset_pool()
    assert get_active_key(keys) == "k1"


def test_cooldown_expiration() -> None:
    """Verify key becomes available after cooldown passes."""
    reset_pool()
    keys = ["k_quick"]
    mark_key_exhausted("k_quick", cooldown_sec=0.01)
    time.sleep(0.02)
    assert get_active_key(keys) == "k_quick"
