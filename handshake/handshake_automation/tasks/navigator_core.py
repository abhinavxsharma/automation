"""Core page filter helpers for Handshake navigator."""

from playwright.sync_api import Page

from handshake_automation.tasks.task_ids import ACTIVE, EXPIRED


def _exp(url: str) -> bool:
    return any(x in url for x in EXPIRED)


def get_task_page(page: Page) -> Page:
    """Find active task page (prefer 83932e3d) or return current."""
    pp = [page] + [t for t in page.context.pages if t != page and not t.is_closed()]
    for p in pp:
        if ACTIVE in p.url:
            p.bring_to_front()
            return p
    for p in pp:
        if "/task/" in p.url and not _exp(p.url):
            p.bring_to_front()
            return p
    return page
