"""Fills model failure mode selections and KaTeX justifications."""

import logging

from playwright.sync_api import Error, Page

logger = logging.getLogger(__name__)


def fill_failure_justifications(page: Page, category: str, justification: str) -> bool:
    """Select failure mode checkbox and enter detailed KaTeX explanation."""
    try:
        # Check matching error type checkbox
        box = page.locator(f'label:has-text("{category}"), input[value*="{category.lower()}"]').first
        if not box.is_visible():
            box = page.locator('label:has-text("Spatial"), label:has-text("Incorrect value extraction")').first
        if box.is_visible():
            box.click()

        # Fill justification text
        area = page.locator('textarea, div[contenteditable="true"]').first
        if area.is_visible():
            area.fill(justification)
            logger.info("Filled model failure justification (%d chars).", len(justification))

        cont_btn = page.locator('button:has-text("Continue"), button:has-text("Next")').last
        if cont_btn.is_visible() and cont_btn.is_enabled():
            cont_btn.click(force=True)
            page.wait_for_timeout(2000)
            return True

    except (Error, TimeoutError) as exc:
        logger.warning("Could not fill failure justifications: %s", exc)
    return False
