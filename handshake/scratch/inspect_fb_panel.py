import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    # Dismiss timer if visible
    st = pg.locator('button:has-text("Start timer")').first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            pg.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(0.5)

    fb_panel = pg.locator("aside, [data-testid*='feedback' i], div:has-text('Needs attention')").last
    print("Feedback buttons:")
    for b in fb_panel.locator("button").all():
        if b.is_visible():
            print("  Btn:", repr(b.inner_text()), "aria-label:", repr(b.get_attribute("aria-label")))
