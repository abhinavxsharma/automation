"""Prevent Windows from going to sleep during automation."""

import ctypes
import logging
import platform

logger = logging.getLogger(__name__)
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001


def prevent_sleep() -> bool:
    """Request Windows OS to stay awake."""
    if platform.system().lower() != "windows":
        return False
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        )
        logger.info("Windows sleep prevention activated.")
        return True
    except (AttributeError, OSError) as exc:
        logger.warning("Could not set Windows execution state: %s", exc)
        return False


def allow_sleep() -> None:
    """Release sleep assertion."""
    if platform.system().lower() == "windows":
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            logger.info("Windows sleep prevention released.")
        except (AttributeError, OSError):
            pass
