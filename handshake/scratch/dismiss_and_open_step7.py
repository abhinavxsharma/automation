import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright


def dismiss_timer(page):
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible(timeout=1000):
        print("Start timer button is visible, clicking it...")
        box = st.bounding_box()
        if box:
            page.mouse.click(
                box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
            )
            time.sleep(1.0)
    else:
        print("Start timer button not visible")


with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=15000)

    # 1. Dismiss timer
    dismiss_timer(page)

    # 2. Scroll to Step 7 and find edit button
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found edit buttons:", len(edit_btns))
    btn7 = edit_btns[7]
    btn7.scroll_into_view_if_needed()
    time.sleep(0.5)

    # Dismiss timer again if it reappeared
    dismiss_timer(page)

    print("Clicking btn7...")
    btn7.click(force=True)
    time.sleep(2)

    dismiss_timer(page)

    page.screenshot(path="handshake/scratch/step7_opened_success.png")
    print("Saved step7_opened_success.png")

    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())
    if ta.is_visible():
        print("Textarea value:\n", ta.input_value()[:120])
