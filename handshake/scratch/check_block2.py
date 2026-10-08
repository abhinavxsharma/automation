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
    is_gen = "Generating response" in body or "The next response is now being generated" in body
    print("Is Block 2 still generating?", is_gen)

    # Check for checkboxes or Block 2 responses
    idx2 = body.find("Block 2 Responses:")
    if idx2 != -1:
        print("Block 2 text snippet:\n", body[idx2:idx2 + 300])

    pg.screenshot(path="scratch/block2_status_now.png")
    print("Saved scratch/block2_status_now.png")
