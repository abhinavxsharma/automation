"""Configuration settings for Handshake AI automation."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application global settings and runtime credentials."""

    tasks_url: str = os.getenv(
        "HANDSHAKE_TASKS_URL",
        "https://ai.joinhandshake.com/fellow/15f2e875-62ac-492c-9e96-d5569635671a/tasks",
    )
    timeout_ms: int = int(os.getenv("HANDSHAKE_TIMEOUT_MS", "45000"))
    max_tasks: int = int(os.getenv("HANDSHAKE_MAX_TASKS", "50"))
    auto_submit: bool = os.getenv("HANDSHAKE_AUTO_SUBMIT", "true").lower() == "true"
    min_time_sec: int = int(os.getenv("HANDSHAKE_MIN_TIME_SEC", "3600"))
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_model: str = os.getenv(
        "OPENROUTER_MODEL", "google/gemini-2.5-flash"
    )
    openrouter_fallback_model: str = os.getenv(
        "OPENROUTER_FALLBACK_MODEL", "google/gemini-2.5-flash"
    )
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


config = Settings()
