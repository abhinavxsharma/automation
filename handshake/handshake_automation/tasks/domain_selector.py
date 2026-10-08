"""Subdomain and image license selector for Handshake Project Lumière."""

import logging

from playwright.sync_api import Error, Page

logger = logging.getLogger(__name__)


def select_subdomain(page: Page, supertype: str = "Computer Science", subtype: str = "Algorithms and Complexity") -> bool:
    """Select engineering supertype and subtype, then advance."""
    try:
        for val in [supertype, subtype]:
            elem = page.locator(f'button:has-text("{val}"), [role="button"]:has-text("{val}"), text="{val}"').first
            if elem.is_visible():
                elem.click()
                page.wait_for_timeout(500)
        cont_btn = page.locator('button:has-text("Continue"), button:has-text("Next")').first
        if cont_btn.is_visible():
            cont_btn.click()
            page.wait_for_timeout(2000)
            logger.info("Selected subdomain: %s -> %s", supertype, subtype)
            return True
    except (Error, TimeoutError) as exc:
        logger.warning("Could not select subdomain: %s", exc)
    return False


def set_source_and_license(page: Page, is_original: bool = True, source_url: str = "N/A", license_type: str = "N/A") -> bool:
    """Configure image source (Original or External) and license."""
    try:
        sel = 'label:has-text("Original"), text="Original"' if is_original else 'label:has-text("External"), text="External"'
        source_opt = page.locator(sel).first
        if source_opt.is_visible():
            source_opt.click()
            page.wait_for_timeout(500)

        for in_sel, val in [('input[placeholder*="DOI" i], input[placeholder*="URL" i]', source_url), ('input[placeholder*="License" i]', license_type)]:
            inp = page.locator(in_sel).first
            if inp.is_visible():
                inp.fill(val)

        cont_btn = page.locator('button:has-text("Continue"), button:has-text("Next")').first
        if cont_btn.is_visible():
            cont_btn.click()
            page.wait_for_timeout(2000)
            logger.info("Configured source (Original: %s)", is_original)
            return True
    except (Error, TimeoutError) as exc:
        logger.warning("Could not set source/license: %s", exc)
    return False
