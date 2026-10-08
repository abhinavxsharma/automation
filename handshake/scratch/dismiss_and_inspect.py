import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=500):
            box = st.bounding_box()
            if box:
                print("Clicking Start timer to dismiss...")
                page.mouse.click(
                    box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                )
                time.sleep(1.0)
    except Exception:
        pass


with sync_playwright() as p:
    browser, page = get_task_page(p)
    dismiss_timer(page)

    page.screenshot(path="handshake/scratch/live_view_after_timer_dismiss.png")
    print("Saved live_view_after_timer_dismiss.png")

    # Check if Step 7 is visible or open
    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())
    if ta.is_visible():
        print("Textarea text:\n", ta.input_value()[:100])
