"""Handles model response testing and 2/2 failure verification."""

import logging

from playwright.sync_api import Error, Page

logger = logging.getLogger(__name__)


def verify_model_failures(page: Page) -> bool:
    """Trigger model testing and verify both models fail per Lumiere rules."""
    try:
        for sel in ['button:has-text("Test models")', 'button:has-text("Generate responses")', 'button:has-text("Submit to models")']:
            if (test_btn := page.locator(sel).first).is_visible():
                logger.info("Triggering platform model response generation...")
                test_btn.click()
                page.wait_for_timeout(10000)
                break

        agree_btn = page.locator('button:has-text("I agree to the above"), [role="button"]:has-text("I agree to the above")').first
        if agree_btn.is_visible(timeout=15000):
            agree_btn.click()
            logger.info("Confirmed 2/2 model failure agreement (stumped both models).")
            page.wait_for_timeout(1000)
        elif page.locator('text="cannot stump 2 out of 2", text="make the prompt more difficult"').first.is_visible():
            logger.error("Platform alert: 2/2 models did NOT fail! Must strengthen prompt.")
            return False

        cont_btn = page.locator('button:has-text("Continue"), button:has-text("Next")').first
        if cont_btn.is_visible():
            cont_btn.click()
            page.wait_for_timeout(2000)
            return True
    except (Error, TimeoutError) as exc:
        logger.warning("Model testing verification error: %s", exc)
    return False
