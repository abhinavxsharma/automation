"""Tests for persistent and in-memory caption cache."""

from pathlib import Path
from unittest.mock import patch

from crowdgen_automation.tasks.caption_cache import (
    _hash_key,
    get_cached_caption,
    save_cached_caption,
)


def test_hash_key_stability() -> None:
    """Verify hash key generates consistent 16-char string."""
    k1 = _hash_key("https://example.com/image.jpg")
    k2 = _hash_key("https://example.com/image.jpg")
    assert k1 == k2
    assert len(k1) == 16


def test_save_and_get_cached_caption(tmp_path: Path) -> None:
    """Verify saved caption can be retrieved from cache."""
    cache_path = tmp_path / "test_cache.json"
    with patch("crowdgen_automation.tasks.caption_cache.CACHE_FILE", cache_path):
        captions = {"short_caption": "Short.", "detailed_caption": "Detailed.", "camera_angle": ""}
        save_cached_caption("https://example.com/img1.jpg", captions)
        retrieved = get_cached_caption("https://example.com/img1.jpg")
        assert retrieved == captions
        assert get_cached_caption("https://example.com/other.jpg") is None
