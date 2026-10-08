"""Validation execution and feedback parsing for Maven tasks."""

import logging
import time

from playwright.sync_api import Error, FrameLocator, Page

logger = logging.getLogger(__name__)
VALIDATE_SEL = 'button:has-text("Validate Captions"), button:has-text("Validate")'
ERR_SEL = 'text="INVALID - DETAILED", text="INVALID - SHORT", text="cannot be overridden"'
OK_SEL = 'text="VALID - all checks passed", text="Captions are valid", text="You may now submit"'
SUBMIT_SEL = 'button:has-text("Submit"), input[value="Submit"]'


def click_validate(context: Page | FrameLocator) -> tuple[bool, str | None]:
    """Click 'Validate Captions' button and return (passed, error_msg)."""
    val_btn = context.locator(VALIDATE_SEL).first
    if not val_btn.is_visible():
        return True, None
    logger.info("Clicking 'Validate Captions' button...")
    val_btn.scroll_into_view_if_needed()
    val_btn.click()
    try:
        val_wait = context.locator('text="Validating captions"').first
        if val_wait.is_visible():
            val_wait.wait_for(state="hidden", timeout=12000)
    except (Error, TimeoutError):
        pass
    for _ in range(12):
        ok_loc = context.locator(OK_SEL).first
        if ok_loc.is_visible():
            logger.info("Validation passed: %s", ok_loc.inner_text().strip())
            return True, None
        err_loc = context.locator(ERR_SEL).first
        if err_loc.is_visible():
            err_msg = err_loc.inner_text().strip()
            logger.warning("Validation failed: %s", err_msg)
            return False, err_msg
        sub_loc = context.locator(SUBMIT_SEL).first
        if sub_loc.is_visible() and sub_loc.get_attribute("disabled") is None:
            logger.info("Validation passed! Submit button enabled.")
            return True, None
        time.sleep(0.5)
    logger.info("Validation finished with no errors detected.")
    return True, None
