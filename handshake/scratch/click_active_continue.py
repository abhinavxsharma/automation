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

    active_block = pg.locator("div[data-block-id]").last
    btn = active_block.locator('button[aria-label="Continue"], button:has-text("Continue")').first
    print("Clicking active block Continue button...")
    btn.click(force=True)
    time.sleep(4)

    dismiss_timer(pg)

    print("\n--- Checkboxes / Labels ---")
    for cb in pg.locator('input[type="checkbox"], [role="checkbox"], label').all():
        if cb.is_visible():
            t = cb.inner_text().strip()
            if t:
                print("  CB:", repr(t[:120]))

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
    pg.screenshot(path="scratch/after_active_continue.png")
    print("Saved scratch/after_active_continue.png")
