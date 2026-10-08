import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright


def dismiss_timer(page):
    st = page.locator('button:has-text("Start timer")').first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(0.5)


with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)
    dismiss_timer(pg)

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/block1_finished_body.txt", "w", encoding="utf-8") as f:
        f.write(body)
    print("Wrote scratch/block1_finished_body.txt")

    pg.screenshot(path="scratch/block1_finished.png")
    print("Saved scratch/block1_finished.png")

    # Find timer
    for ln in body.splitlines():
        if "/ 04:00:00" in ln or "Stage:" in ln or "Block 1" in ln or "Block 2" in ln or "Continue" in ln:
            print("Status line:", repr(ln.strip()))
