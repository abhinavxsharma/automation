"""Fills 5 distractors and answer format/precision fields."""

import logging
from typing import Any

from playwright.sync_api import Error, Page

logger = logging.getLogger(__name__)


def fill_distractors(page: Page, distractors: list[Any]) -> bool:
    """Fill 5 distinct, plausible incorrect answers."""
    try:
        inputs = [i for i in page.locator('textarea, input[type="text"]').all() if i.is_visible()]
        for i, val in enumerate(distractors[:5]):
            if i < len(inputs):
                inputs[i].fill(str(val))
        btn = page.locator('button:has-text("Continue"), button:has-text("Next")').last
        if btn.is_visible() and btn.is_enabled():
            btn.click(force=True)
            page.wait_for_timeout(2000)
            logger.info("Filled 5 distractors.")
            return True
    except (Error, TimeoutError) as exc:
        logger.warning("Error filling distractors: %s", exc)
    return False


def fill_answer_format(page: Page, fmt: str = "Decimal", decimal_places: int = 2) -> bool:
    """Specify precision decimal places and select format."""
    try:
        # Fill decimal places if input is visible
        dec_input = page.locator('input[type="number"], input[placeholder*="decimal" i]').first
        if dec_input.is_visible():
            dec_input.fill(str(decimal_places))

        # Select format button (Decimal / Integer)
        for sel in [f'button:has-text("{fmt}")', f'div[role="option"]:has-text("{fmt}")', f'label:has-text("{fmt}")']:
            btn = page.locator(sel).first
            if btn.is_visible():
                btn.click()
                break

        nxt = page.locator('button:has-text("Continue"), button:has-text("Next")').last
        if nxt.is_visible() and nxt.is_enabled():
            nxt.click(force=True)
            page.wait_for_timeout(2000)
            logger.info("Selected format %s with %d decimals.", fmt, decimal_places)
            return True

    except (Error, TimeoutError) as exc:
        logger.warning("Error setting answer format: %s", exc)
    return False
