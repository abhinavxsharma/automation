import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    card = pg.locator("div[data-block-id]").last
    print("Card HTML:\n", card.evaluate("el => el.outerHTML")[:2000])

    cont = card.locator('button:has-text("Continue")').first
    print("Continue button visible?", cont.is_visible(), "Enabled?", cont.is_enabled())
