"""System sleep prevention context manager."""

import ctypes
import logging
import sys
from collections.abc import Generator
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def keep_awake() -> Generator[None]:
    """Prevent system sleep during automation execution."""
    if sys.platform == "win32":
        es_continuous = 0x80000000
        es_system_required = 0x00000001
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(
                es_continuous | es_system_required
            )
            logger.info("Windows sleep prevention activated.")
            yield
        finally:
            ctypes.windll.kernel32.SetThreadExecutionState(es_continuous)
            logger.info("Windows sleep prevention released.")
    else:
        yield
