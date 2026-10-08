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

    # Find timer
    for line in body.splitlines():
        if "/ 04:00:00" in line:
            print("Timer status:", line.strip())

    # Check for Generating
    is_gen = "Generating response" in body
    print("Is 'Generating response' present?", is_gen)

    # Check for Block 1 responses
    if "Block 1 Responses:" in body:
        idx = body.find("Block 1 Responses:")
        print("Block 1 text sample:\n", body[idx:idx + 400])

    pg.screenshot(path="scratch/model_gen_status.png")
    print("Saved scratch/model_gen_status.png")
