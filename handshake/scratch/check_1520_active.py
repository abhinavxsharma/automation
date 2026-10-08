import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    print("Connected. Current URL:", page.url)
    if "1520c7f4" not in page.url:
        page.goto("https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
    
    # Check if timer modal is up
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        print("Timer modal visible, clicking Start timer...")
        box = st.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/live_1520_active.png")
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/live_1520_body.txt").write_text(txt, encoding="utf-8")
    print("Page URL:", page.url)
    print("Body length:", len(txt))
    print("Screenshot saved to scratch/live_1520_active.png")
