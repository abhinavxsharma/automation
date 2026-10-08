import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    # Dismiss timer modal
    st = pg.locator('button:has-text("Start timer")').first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            print("Dismissing Start timer modal...")
            pg.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(1)

    pg.screenshot(path="scratch/live_state_now.png")
    print("Saved scratch/live_state_now.png")

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
