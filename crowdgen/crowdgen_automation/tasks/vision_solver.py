"""Multimodal vision solver for Project Origami/Oberon captioning."""

import json
import logging
import re

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from crowdgen_automation.config import Settings
from crowdgen_automation.tasks import caption_cache, key_pool

logger = logging.getLogger(__name__)
SYSTEM_PROMPT = ('Expert Project Origami captioner. JSON: {"detailed_caption": "1-3 present sentences, >=26 words, physical facts.", "short_caption": "1 sentence, 6-25 words.", "camera_angle": "Complete sentence (12-30 words) detailing viewpoint, angle, perspective with setting, e.g. \'A low-angle view from near ground level, showing a standing figure in a medium shot, with the sky behind them.\' Never short fragments. If not identifiable, \'\'."}. FORBIDDEN SUBJECTIVE WORDS: beautiful, beautifully, stunning, gorgeous, scenic, peaceful, charming, adorable, picturesque, wonderful, delicate, perfect, rustic, vibrant. FORBIDDEN ASSUMPTIVE WORDS: appears to be, seems, likely, probably, possibly, may/might/could be, suggesting. NO role guessing. NO speed words.')
SUBJ_REGEX = re.compile(r"\b(beautifully|beautiful|stunning|gorgeous|scenic|peaceful|charming|adorable|picturesque|delicate|vibrant)\s*", re.IGNORECASE)


def _sanitize(text: str) -> str:
    c = re.sub(r"^(?:Detailed|Short)\s*Caption\s*:\s*", "", text, flags=re.IGNORECASE)
    return re.sub(r"[ \t]+", " ", SUBJ_REGEX.sub("", re.sub(r"\bcontrast\s+beautifully\s+with\b", "contrast with", c, flags=re.IGNORECASE))).strip()


def _clean_json(text: str) -> dict[str, str]:
    c = re.sub(r"```(?:json)?\s*|\s*```", "", re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)).strip()
    data = json.loads(m.group(0) if (m := re.search(r"\{.*\}", c, re.DOTALL)) else c)
    res = {k: _sanitize(str(data.get(k, ""))) for k in ("detailed_caption", "short_caption", "camera_angle")}
    if (ang := res["camera_angle"]) and len(ang.split()) < 5 and (sh := res["short_caption"]):
        res["camera_angle"] = f"A {ang.rstrip('.')} view showing {sh[0].lower() + sh[1:].rstrip('.')}."
    return res


def _call_api(url: str, key: str, model: str, img: str, err: str | None) -> dict[str, str]:
    p = f"Describe image per Project Origami rules.{f' CRITICAL: Previous failed with error: {err}. Fix strictly.' if err else ''}"
    payload = {"model": model, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": [{"type": "text", "text": p}, {"type": "image_url", "image_url": {"url": img}}]}]}
    res = requests.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=45)
    res.raise_for_status()
    return _clean_json(res.json()["choices"][0]["message"]["content"])


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_captions(img_ref: str, cfg: Settings, error_feedback: str | None = None) -> dict[str, str]:
    """Generate compliant Project Origami captions via Vision AI."""
    if not error_feedback and (cached := caption_cache.get_cached_caption(img_ref)):
        return cached
    keys = key_pool.load_keys(extra_keys=[cfg.openrouter_api_key] if cfg.openrouter_api_key else None)
    while key := key_pool.get_active_key(keys):
        try:
            res = _call_api(f"{cfg.openrouter_base_url.rstrip('/')}/chat/completions", key, cfg.openrouter_vision_model, img_ref, error_feedback)
            caption_cache.save_cached_caption(img_ref, res)
            return res
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code in (402, 429):
                key_pool.mark_key_exhausted(key)
                continue
            raise
    if not cfg.gemini_api_key:
        raise RuntimeError("All OpenRouter API keys in openrouter_keys.txt exhausted.")
    res = _call_api("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", cfg.gemini_api_key, cfg.gemini_model, img_ref, error_feedback)
    caption_cache.save_cached_caption(img_ref, res)
    return res
