"""Tests for OpenRouter vision solver."""

from unittest.mock import MagicMock, patch

from crowdgen_automation.config import Settings
from crowdgen_automation.tasks.vision_solver import (
    _clean_json,
    _sanitize,
    generate_captions,
)


def test_sanitize_removes_labels_and_double_spaces() -> None:
    """Verify _sanitize strips leftover interface labels and extra spaces."""
    raw = "Detailed Caption:   A  red   apple on a white plate.  "
    assert _sanitize(raw) == "A red apple on a white plate."
    raw_short = "Short Caption: A blue boat on water."
    assert _sanitize(raw_short) == "A blue boat on water."


def test_sanitize_removes_subjective_words() -> None:
    """Verify _sanitize purges banned subjective words like beautifully, delicate, vibrant."""
    raw = "The bright yellow minerals contrast beautifully with the delicate white structure."
    assert _sanitize(raw) == "The bright yellow minerals contrast with the white structure."


def test_clean_json_valid_markdown_and_think_tags() -> None:
    """Verify strips <think> tags, markdown backticks, and interface labels."""
    raw = (
        "<think>Analyzing image details...</think>\n"
        "```json\n"
        '{"short_caption": "Short Caption: A red apple.", '
        '"detailed_caption": "Detailed Caption: A red apple sitting on a white ceramic plate in natural light."}\n'
        "```"
    )
    res = _clean_json(raw)
    assert res["short_caption"] == "A red apple."
    assert res["detailed_caption"] == (
        "A red apple sitting on a white ceramic plate in natural light."
    )


def test_clean_json_expands_short_angle_fragment() -> None:
    """Verify clean_json converts 1-3 word angle fragments into full descriptive sentences."""
    raw = (
        '{"short_caption": "A hand holds a stack of metallic coins on a wooden surface.", '
        '"detailed_caption": "A close-up view of coins stacked on wood.", '
        '"camera_angle": "high angle"}'
    )
    res = _clean_json(raw)
    assert "A high angle view showing" in res["camera_angle"]
    assert "coins on a wooden surface" in res["camera_angle"]


def test_generate_captions_success(mock_settings: Settings) -> None:
    """Verify generate_captions invokes OpenRouter with image URL and returns parsed JSON."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"short_caption": "A cozy cafe.", '
                        '"detailed_caption": "A quiet coffee shop with wooden chairs and warm ambient lighting."}'
                    )
                }
            }
        ]
    }
    with (
        patch("crowdgen_automation.tasks.caption_cache.get_cached_caption", return_value=None),
        patch("requests.post", return_value=mock_resp) as mock_post,
    ):
        res = generate_captions("https://example.com/img.jpg", mock_settings)
        assert res["short_caption"] == "A cozy cafe."
        assert "quiet coffee shop" in res["detailed_caption"]
        payload = mock_post.call_args[1]["json"]
        assert payload["model"] == "dots-studio/dots-3-note-preview:free"
        assert (
            payload["messages"][1]["content"][1]["image_url"]["url"]
            == "https://example.com/img.jpg"
        )


def test_generate_captions_with_error_feedback(mock_settings: Settings) -> None:
    """Verify error feedback is injected into user prompt for self-healing."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": (
                        '{"short_caption": "Fixed caption.", '
                        '"detailed_caption": "Fixed detailed description with more than 25 words."}'
                    )
                }
            }
        ]
    }
    with patch("requests.post", return_value=mock_resp) as mock_post:
        generate_captions(
            "data:image/jpeg;base64,123",
            mock_settings,
            error_feedback="Detailed caption under 25 words",
        )
        user_prompt = mock_post.call_args[1]["json"]["messages"][1]["content"][
            0
        ]["text"]
        assert "CRITICAL: Previous failed with error:" in user_prompt
        assert "Detailed caption under 25 words" in user_prompt


def test_generate_captions_google_ai_studio() -> None:
    """Verify generate_captions routes to Google AI Studio when gemini_api_key is set."""
    cfg = Settings(
        gemini_api_key="AIzaSyTestKey123",
        gemini_model="gemini-3-flash-preview",
        openrouter_api_key="",
    )
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": '{"short_caption": "Apple crate.", "detailed_caption": "A wooden crate filled with red apples."}'
                }
            }
        ]
    }
    with (
        patch("crowdgen_automation.tasks.caption_cache.get_cached_caption", return_value=None),
        patch("crowdgen_automation.tasks.key_pool.load_keys", return_value=[]),
        patch("requests.post", return_value=mock_resp) as mock_post,
    ):
        res = generate_captions("https://example.com/apples.jpg", cfg)
        assert res["short_caption"] == "Apple crate."
        url = mock_post.call_args[0][0]
        assert "generativelanguage.googleapis.com" in url
        headers = mock_post.call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer AIzaSyTestKey123"
        payload = mock_post.call_args[1]["json"]
        assert payload["model"] == "gemini-3-flash-preview"


def test_generate_captions_rotates_on_429() -> None:
    """Verify generate_captions rotates to next key when first key hits 429."""
    import requests

    from crowdgen_automation.tasks import key_pool

    key_pool.reset_pool()
    cfg = Settings(
        gemini_api_key="",
        openrouter_api_key="key1",
    )
    err_resp = MagicMock()
    err_resp.status_code = 429
    exc_429 = requests.HTTPError(response=err_resp)

    ok_resp = MagicMock()
    ok_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": '{"short_caption": "Rotated key.", "detailed_caption": "Caption generated after rotating keys."}'
                }
            }
        ]
    }

    with (
        patch("crowdgen_automation.tasks.caption_cache.get_cached_caption", return_value=None),
        patch("crowdgen_automation.tasks.key_pool.load_keys", return_value=["key1", "key2"]),
        patch("requests.post", side_effect=[exc_429, ok_resp]) as mock_post,
    ):
        res = generate_captions("https://example.com/item.jpg", cfg)
        assert res["short_caption"] == "Rotated key."
        assert mock_post.call_count == 2
        # First call used key1
        assert mock_post.call_args_list[0][1]["headers"]["Authorization"] == "Bearer key1"
        # Second call rotated to key2
        assert mock_post.call_args_list[1][1]["headers"]["Authorization"] == "Bearer key2"

