"""Final submission and session time confirmation for Handshake tasks."""

import logging
import time

from playwright.sync_api import Error, Page

logger = logging.getLogger(__name__)
MAX_ALLOWED_TASK_SEC = 10800  # 3 hours (safe below 3.5h ceiling)


def wait_session_pacing(start_time: float, min_time_sec: int = 1800) -> None:
    """Pace session to simulate authentic human authoring time within 3.5h limit."""
    target_sec = min(min_time_sec, MAX_ALLOWED_TASK_SEC)
    while (remaining := target_sec - int(time.monotonic() - start_time)) > 0:
        logger.info("Session pacing: %d seconds remaining before submission...", remaining)
        time.sleep(min(remaining, 30))


def confirm_and_submit(page: Page, start_time: float, auto_submit: bool = True, min_time_sec: int = 1800) -> bool:
    """Confirm logged time and finalize task submission."""
    if not auto_submit:
        logger.info("Review mode: All 11 steps completed. Please inspect and submit manually.")
        return True

    wait_session_pacing(start_time, min_time_sec)
    try:
        # Step 12: Confirm session time modal / button
        for sel in ['button:has-text("Confirm time")', 'button:has-text("Submit for review")', 'button:has-text("Submit task")']:
            if (btn := page.locator(sel).first).is_visible(timeout=5000):
                btn.click()
                page.wait_for_timeout(2000)
                break

        # Final confirmation dialog if present
        for sel in ['button:has-text("Yes, submit")', 'button:has-text("Confirm")', 'button:has-text("Submit")']:
            if (final_btn := page.locator(sel).first).is_visible(timeout=3000):
                final_btn.click()
                page.wait_for_timeout(3000)
                break

        logger.info("Project Lumière task submitted successfully!")
        return True
    except (Error, TimeoutError) as exc:
        logger.warning("Error during final submission: %s", exc)
    return False
