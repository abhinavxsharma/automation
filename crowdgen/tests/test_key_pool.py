"""Tests for OpenRouter key pool and rotation management."""

import time
from pathlib import Path
from unittest.mock import patch

from crowdgen_automation.tasks.key_pool import (
    get_active_key,
    load_keys,
    mark_key_exhausted,
    reset_pool,
)


def test_load_keys_from_file_and_env(tmp_path: Path) -> None:
    """Verify load_keys extracts unique keys from file, comments ignored, and env."""
    keys_file = tmp_path / "keys.txt"
    keys_file.write_text(
        "# Comment line\n"
        "key_file_1\n"
        "\n"
        "key_file_2\n"
        "key_file_1\n",  # duplicate
        encoding="utf-8",
    )
    with patch.dict("os.environ", {"OPENROUTER_API_KEYS": "key_env_1,key_file_2"}):
        keys = load_keys(str(keys_file), extra_keys=["key_extra"])
        assert keys == ["key_file_1", "key_file_2", "key_env_1", "key_extra"]


def test_get_active_key_and_cooldown() -> None:
    """Verify get_active_key returns first available and respects cooldown."""
    reset_pool()
    keys = ["k1", "k2", "k3"]
    assert get_active_key(keys) == "k1"

    # Mark k1 exhausted with 10s cooldown
    mark_key_exhausted("k1", cooldown_sec=10.0)
    assert get_active_key(keys) == "k2"

    # Mark k2 exhausted
    mark_key_exhausted("k2", cooldown_sec=10.0)
    assert get_active_key(keys) == "k3"

    # Mark k3 exhausted
    mark_key_exhausted("k3", cooldown_sec=10.0)
    assert get_active_key(keys) is None

    # Reset pool
    reset_pool()
    assert get_active_key(keys) == "k1"


def test_key_cooldown_expires() -> None:
    """Verify key becomes available again when cooldown expires."""
    reset_pool()
    keys = ["k_short"]
    mark_key_exhausted("k_short", cooldown_sec=0.01)
    time.sleep(0.02)
    assert get_active_key(keys) == "k_short"
