import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    # Find the active block
    active = pg.locator("div[data-block-id]").last
    print("Active block HTML:")
    print(active.evaluate("el => el.outerHTML"))
