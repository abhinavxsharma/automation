"""Task discovery, claiming, and timer activation for Handshake AI."""

import logging

from playwright.sync_api import Error, Page

from handshake_automation.tasks.navigator_core import _exp, get_task_page

logger = logging.getLogger(__name__)


def start_task_timer(page: Page) -> bool:
    """Click Start Timer modal button if visible."""
    try:
        b = page.locator('button:has-text("Start timer"), [aria-label*="start timer" i]').first
        if b.is_visible(timeout=3000):
            b.click()
            page.wait_for_timeout(1000)
            return True
    except (Error, TimeoutError):
        pass
    return False


def claim_or_resume_task(page: Page, tasks_url: str) -> bool:
    """Find active task (83932e3d / In progress) and click Continue."""
    tab = get_task_page(page)
    if "/task/" in tab.url and not _exp(tab.url):
        logger.info("Using active task tab: %s", tab.url)
        start_task_timer(tab)
        return True
    if tasks_url not in page.url:
        page.goto(tasks_url, timeout=30000)
    page.wait_for_timeout(2000)
    if (b := page.locator('button:has-text("My tasks")').first).is_visible():
        b.click()
        c = page.locator('div, li').filter(has_text="83932e3d").last
        if not c.is_visible():
            c = page.locator('div, li').filter(has_text="In progress").filter(has_not_text="Fix").last
        if c.is_visible() and (k := c.locator('button:has-text("Continue")').first).is_visible():
            k.click()
            page.wait_for_timeout(3000)
            return start_task_timer(get_task_page(page))
    if (a := page.locator('button:has-text("Available tasks")').first).is_visible():
        a.click()
        page.locator('div:has-text("Create a clear")').first.click()
        if (s := page.locator('button:has-text("Start task")').first).is_visible():
            s.click()
            page.wait_for_timeout(3000)
            return start_task_timer(get_task_page(page))
    return False
