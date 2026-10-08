"""Snapshot and image extraction for Maven captioning tasks."""

import base64
import logging

from playwright.sync_api import FrameLocator, Locator, Page

logger = logging.getLogger(__name__)

IMG_SEL = (
    'img:not([src*="logo" i]):not([alt*="logo" i]), canvas, '
    '[data-testid*="image"], figure img, div[role="img"], [class*="image" i] img'
)


def get_task_context(page: Page) -> Page | FrameLocator:
    """Find and return active task frame or main page."""
    if page.locator(IMG_SEL).first.is_visible(timeout=1000):
        return page
    for frame in page.frames:
        if (
            frame != page.main_frame
            and any(k in frame.url.lower() for k in ("task", "annotate", "unit"))
            and (name := frame.url.split("/")[-1].split("?")[0])
        ):
            return page.frame_locator(f'iframe[src*="{name}"]')
    if (iframes := page.locator("iframe")).count() > 0:
        for idx in range(iframes.count()):
            candidate = page.frame_locator(f"iframe >> nth={idx}")
            if candidate.locator(IMG_SEL).first.is_visible(timeout=500):
                return candidate
    return page


def capture_task_image(context: Page | FrameLocator) -> tuple[str, str]:
    """Capture snapshot of task image as base64 string or extract direct URL."""
    img_loc: Locator = context.locator(IMG_SEL).locator("visible=true").first
    img_loc.wait_for(state="visible", timeout=25000)
    img_loc.scroll_into_view_if_needed()
    src = img_loc.get_attribute("src") or ""
    if src.startswith("http") and not src.startswith("blob:"):
        logger.info("Extracted direct image URL.")
        return ("url", src)
    logger.info("Taking cropped snapshot of image element...")
    screenshot_bytes = img_loc.screenshot(type="jpeg", quality=85)
    b64_str = base64.b64encode(screenshot_bytes).decode("utf-8")
    return ("base64", f"data:image/jpeg;base64,{b64_str}")
