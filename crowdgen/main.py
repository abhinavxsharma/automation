"""Main supervisor runner for CrowdGen Maven automation with auto-restart."""

import logging
import time

import requests
from playwright.sync_api import Error as PlaywrightError
from tenacity import RetryError

from crowdgen_automation.main import run

logger = logging.getLogger(__name__)
RUN_EXCS = (PlaywrightError, OSError, RuntimeError, TimeoutError, ValueError, KeyError, requests.RequestException, RetryError)


def main() -> None:
    """Run CrowdGen Maven automation workflow with resilient auto-restart."""
    restart_count = 0
    while True:
        try:
            run()
            logger.info("Automation completed all configured tasks.")
            break
        except KeyboardInterrupt:
            logger.info("Automation stopped by user (Ctrl+C). Exiting cleanly.")
            break
        except RUN_EXCS as exc:
            restart_count += 1
            logger.warning(
                "Automation error (restart #%d): %s. Auto-restarting in 5s...",
                restart_count,
                exc,
            )
            time.sleep(5)


if __name__ == "__main__":
    main()
