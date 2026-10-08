"""Unit transition and availability controller for Maven tasks."""

import logging
import re
import time

from playwright.sync_api import Error, Page

from crowdgen_automation.tasks.capture import IMG_SEL

logger = logging.getLogger(__name__)

NO_UNITS_SEL = "text=/no\\s+(next\\s+)?unit|no\\s+task|caught\\s+up|empty|no\\s+work/i"
UNIT_SEL = "text=/Unit\\s+[a-f0-9-]+/i"


def get_current_unit_id(page: Page) -> str:
    """Extract active unit identifier from URL or footer bar."""
    if m := re.search(r"/annotate/([^/?#]+)", page.url):
        return m.group(1)
    try:
        loc = page.locator(UNIT_SEL).first
        if loc.is_visible(timeout=500):
            return loc.inner_text().strip()
    except (Error, TimeoutError):
        pass
    return ""


def handle_no_units_available(page: Page, wait_sec: int = 25) -> None:
    """Poll and reload page when no units/tasks are currently available."""
    while True:
        try:
            if not page.locator(NO_UNITS_SEL).first.is_visible(timeout=1000):
                break
        except (Error, TimeoutError):
            break
        logger.warning("No units available. Waiting %ds before refreshing...", wait_sec)
        time.sleep(wait_sec)
        page.reload()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)


def wait_for_new_unit(page: Page, prev_unit: str, timeout_sec: int = 40) -> str:
    """Ensure page has transitioned to a brand new unit and old image is gone."""
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        handle_no_units_available(page)
        curr = get_current_unit_id(page)
        img = page.locator(IMG_SEL).first
        if curr and curr != prev_unit and img.is_visible(timeout=1000):
            logger.info("New unit active: %s (replaced %s).", curr, prev_unit or "initial")
            page.wait_for_timeout(2000)
            return curr
        page.wait_for_timeout(1000)
    return get_current_unit_id(page)
