"""Fills single-input steps and handles image uploads."""

import logging

from playwright.sync_api import Error, Page

logger = logging.getLogger(__name__)


def fill_step_input(page: Page, text: str, file_path: str | None = None) -> bool:
    """Upload image if present, fill active textarea/input, and continue."""
    try:
        if file_path:
            file_input = page.locator('input[type="file"]').first
            if file_input.count() > 0:
                file_input.set_input_files(file_path)
            elif (up_btn := page.locator('button[aria-label*="upload" i], button:has-text("Upload")').first).is_visible():
                with page.expect_file_chooser(timeout=5000) as fc_info:
                    up_btn.click()
                fc_info.value.set_files(file_path)
            page.wait_for_timeout(2000)

        active = page.locator('div[data-block-id]').last
        inp = active.locator('textarea, input[type="text"]').first
        if inp.is_visible() and not inp.input_value().strip():
            inp.fill(text)
        else:
            for el in page.locator('textarea, input[type="text"]').all():
                if el.is_visible() and not el.input_value().strip():
                    el.fill(text)
                    break

        btn = page.locator('button:has-text("Continue"), button:has-text("Next")').last
        if btn.is_visible() and btn.is_enabled():
            btn.click(force=True)
            page.wait_for_timeout(2000)
            return True
    except (Error, TimeoutError) as exc:
        logger.warning("Error filling step input: %s", exc)
    return False

