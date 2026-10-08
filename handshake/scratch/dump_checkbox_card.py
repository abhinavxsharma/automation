import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    card = pg.locator("div:has-text('These statements must all be true')").last
    print("Card HTML:")
    print(card.evaluate("el => el.outerHTML"))
