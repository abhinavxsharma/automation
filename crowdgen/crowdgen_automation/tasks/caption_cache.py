"""Persistent and in-memory caption cache for Project Origami."""

import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
CACHE_FILE = Path(".caption_cache.json")
_CACHE: dict[str, dict[str, str]] = {}


def _hash_key(img_ref: str) -> str:
    return hashlib.sha256(img_ref.encode("utf-8", errors="ignore")).hexdigest()[:16]


def load_cache() -> dict[str, dict[str, str]]:
    """Load cached captions from disk."""
    global _CACHE
    if _CACHE:
        return _CACHE
    if CACHE_FILE.is_file():
        try:
            _CACHE = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            _CACHE = {}
    return _CACHE


def get_cached_caption(img_ref: str) -> dict[str, str] | None:
    """Retrieve previously generated caption for identical image if available."""
    cache = load_cache()
    key = _hash_key(img_ref)
    if key in cache:
        logger.info("Found cached caption for image (hash: %s). Reusing.", key)
        return cache[key]
    return None


def save_cached_caption(img_ref: str, captions: dict[str, str]) -> None:
    """Save generated captions for image to memory and disk cache."""
    cache = load_cache()
    key = _hash_key(img_ref)
    cache[key] = captions
    try:
        CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    except OSError as exc:
        logger.debug("Could not write caption cache to disk: %s", exc)
