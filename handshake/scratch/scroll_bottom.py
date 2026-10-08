import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    # Scroll down to bottom
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)

    pg.screenshot(path="scratch/live_bottom_state.png")
    print("Saved scratch/live_bottom_state.png")

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBottom 25 lines:")
    for ln in lines[-25:]:
        try:
            print(" ", ln)
        except Exception:
            pass
