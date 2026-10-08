import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    for b in pg.locator("button").all():
        txt = b.inner_text().strip()
        if "Start" in txt:
            print("Start btn:", repr(txt), "Visible:", b.is_visible())
            print("  HTML:", b.evaluate("el => el.outerHTML"))
