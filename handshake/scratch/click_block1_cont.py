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

    card = pg.locator("div[data-block-id]").last
    cont = card.locator('button:has-text("Continue")').first
    if cont.is_visible():
        print("Clicking Continue on Block 1 card...")
        cont.click(force=True)
        time.sleep(5)

    dismiss_timer(pg)
    pg.screenshot(path="scratch/step5_after_block1_continue.png")
    print("Saved scratch/step5_after_block1_continue.png")

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        try:
            print(" ", ln)
        except Exception:
            pass
