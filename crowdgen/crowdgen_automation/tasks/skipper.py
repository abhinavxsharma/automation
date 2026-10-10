"""Task skip handler for Project Origami / Maven tasks."""

import logging
import time

from playwright.sync_api import Error, FrameLocator, Locator, Page

logger = logging.getLogger(__name__)
SKIP_SEL = 'button:has-text("Skip"), a:has-text("Skip"), [aria-label*="skip" i]'
ISSUE_SEL = 'label:has-text("Yes"), input[type="radio"][value*="Yes" i], label:has-text("Issue")'
UNUSABLE_SEL = 'label:has-text("Unusable Quality Image"), input[type="checkbox"][value*="Unusable" i]'
CLEAR_SEL = ('textarea[placeholder*="caption" i]', 'input[placeholder*="Leave blank" i]', 'input[name*="angle" i]')
SUBMIT_SEL = ('button:has-text("Submit")', 'button[type="submit"]', 'input[value="Submit"]')


def _find_loc(targets: list[Page | FrameLocator], selector: str) -> Locator | None:
    for tgt in targets:
        try:
            if (loc := tgt.locator(selector).first).is_visible(timeout=1000):
                return loc
        except (Error, TimeoutError):
            pass
    return None


def skip_task(context: Page | FrameLocator, page: Page | None = None) -> bool:
    """Skip task via native Skip button, or fallback to flagging unusable quality and submitting."""
    targets = [context, page] if page and page != context else [context]
    logger.warning("Skipping current Maven task...")
    if skip_btn := _find_loc(targets, SKIP_SEL):
        logger.info("Found native Skip button. Clicking to skip...")
        skip_btn.click()
        time.sleep(1)
        if conf := _find_loc(targets, 'button:has-text("Yes"), button:has-text("Confirm")'):
            conf.click()
        return True
    logger.info("No native Skip button found. Marking task as Unusable Quality to skip...")
    try:
        if issue_radio := _find_loc(targets, ISSUE_SEL):
            issue_radio.click()
        if unusable_cb := _find_loc(targets, UNUSABLE_SEL):
            unusable_cb.click()
        for sel in CLEAR_SEL:
            for tgt in targets:
                for el in tgt.locator(sel).all():
                    el.fill("")
        for sel in SUBMIT_SEL:
            if sub_btn := _find_loc(targets, sel):
                sub_btn.scroll_into_view_if_needed()
                sub_btn.click()
                time.sleep(1)
                if conf := _find_loc(targets, 'button:has-text("Yes, submit"), button:has-text("Confirm")'):
                    conf.click()
                logger.info("Skipped task by submitting unusable quality report.")
                return True
    except (Error, TimeoutError) as exc:
        logger.warning("Failed during skip fallback: %s", exc)
    return False
