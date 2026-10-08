import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    btn = pg.locator('button[aria-label="Continue"], button:has-text("Continue")').last
    print("Enabled:", btn.is_enabled())
    print("Visible:", btn.is_visible())
    print("HTML:", btn.evaluate("el => el.outerHTML"))
