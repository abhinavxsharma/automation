"""OpenRouter API key rotation and cooldown management."""

import logging
import os
import time
from pathlib import Path

logger = logging.getLogger(__name__)
_KEY_COOLDOWNS: dict[str, float] = {}
_BOTTOM_UP: bool = False


def load_keys(file_path: str = "openrouter_keys.txt", extra_keys: list[str] | None = None) -> list[str]:
    """Load unique API keys from file and environment variables."""
    keys: list[str] = []
    p = Path(file_path)
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            if (k := line.strip()) and not k.startswith("#") and k not in keys:
                keys.append(k)
    env_keys = os.getenv("OPENROUTER_API_KEYS", "") or os.getenv("OPENROUTER_API_KEY", "")
    for k in (env_keys.replace(";", ",").split(",") + (extra_keys or [])):
        if (k := k.strip()) and k not in keys:
            keys.append(k)
    return keys


def get_active_key(keys: list[str]) -> str | None:
    """Return first active key; traverses bottom-up (10->1) if rotation triggered."""
    now, order = time.monotonic(), list(reversed(keys)) if _BOTTOM_UP else keys
    for k in order:
        if now >= _KEY_COOLDOWNS.get(k, 0.0):
            return k
    return None


def mark_key_exhausted(key: str, cooldown_sec: float = 60.0) -> None:
    """Mark key exhausted, activate bottom-up rotation (10->1), and allow cooldown."""
    global _BOTTOM_UP
    _KEY_COOLDOWNS[key] = time.monotonic() + cooldown_sec
    _BOTTOM_UP = True
    masked = f"...{key[-6:]}" if len(key) >= 6 else "key"
    logger.warning("Key %s exhausted. In cooldown for %ds. Rotated bottom-up (10->1).", masked, int(cooldown_sec))


def reset_pool() -> None:
    """Clear all key cooldowns and rotation order (useful for tests)."""
    global _BOTTOM_UP
    _KEY_COOLDOWNS.clear()
    _BOTTOM_UP = False
