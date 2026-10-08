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
            print("Dismissing Start timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(0.5)


with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)
    dismiss_timer(pg)

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    for ln in body.splitlines():
        if "/ 04:00:00" in ln or "remaining" in ln or "Block 2" in ln:
            print("Line:", repr(ln.strip()))
