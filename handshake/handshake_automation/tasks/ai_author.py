"""AI task authoring engine for Project Lumière graduate problems."""

import json
import logging
import re
from typing import Any

import requests

from handshake_automation.config import Settings
from handshake_automation.tasks import key_pool, problem_solver

logger = logging.getLogger(__name__)
LUMIERE_SYSTEM_PROMPT = (
    "Expert Project Lumière (Engineering) Task Author. Return JSON with keys:\n"
    "- 'prompt': Graduate-level engineering question requiring the diagram. Must use KaTeX ($...$). Must end verbatim with: 'The answer should be expressed in Mbps. Report your final answer as a 2 significant figure number without units. Any intermediate calculations should be carried out to 6 significant figures. All unstated fundamental constants should be used to 4 significant figures.'\n"
    "- 'gtfa': Single numerical/symbolic value without units.\n"
    "- 'image_description': Comprehensive description of image topology, loads, geometry, labels without revealing GTFA.\n"
    "- 'solution': Numbered steps (Step 1, Step 2...) showing visual evidence, KaTeX formulas, calculations, ending in GTFA.\n"
    "- 'distractors': Array of 5 plausible incorrect numerical answers.\n"
    "- 'answer_format': 'Decimal' or 'Integer'.\n"
    "- 'decimal_places': integer decimal precision.\n"
    "- 'failure_category': 'Topological' or 'Spatial' or 'Incorrect value extraction'.\n"
    "- 'failure_justification': KaTeX explanation of why models miscalculate due to visual misinterpretation."
)


def _call_api(url: str, key: str, model: str, payload_data: dict[str, Any]) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {"model": model, "max_tokens": 3000, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": LUMIERE_SYSTEM_PROMPT}, {"role": "user", "content": f"Create graduate problem for: {json.dumps(payload_data)}"}]}
    res = requests.post(url, headers=headers, json=body, timeout=60)
    res.raise_for_status()
    raw = res.json()["choices"][0]["message"]["content"]
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", raw, flags=re.DOTALL).strip()
    return json.loads(cleaned)


def author_task(diagram_info: dict[str, Any], cfg: Settings) -> dict[str, Any]:
    """Generate complete Project Lumière compliant task artifacts."""
    try:
        keys = key_pool.load_keys(extra_keys=[cfg.openrouter_api_key] if cfg.openrouter_api_key else None)
        while key := key_pool.get_active_key(keys):
            try:
                return _call_api(f"{cfg.openrouter_base_url.rstrip('/')}/chat/completions", key, cfg.openrouter_model, diagram_info)
            except requests.HTTPError as exc:
                if exc.response is not None and exc.response.status_code in (402, 404, 429):
                    key_pool.mark_key_exhausted(key)
                    continue
                raise
        if cfg.gemini_api_key:
            return _call_api("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", cfg.gemini_api_key, cfg.gemini_model, diagram_info)
    except (requests.RequestException, json.JSONDecodeError, KeyError, ValueError) as exc:
        logger.warning("API generation unavailable (%s). Falling back to mathematical solver.", exc)
    return problem_solver.solve_network_flow_task(diagram_info)
