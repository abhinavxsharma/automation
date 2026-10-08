import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    # Check all edit buttons (pencil icons) on the page
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total 'Edit this step' buttons: {len(edit_btns)}")
    for i, btn in enumerate(edit_btns):
        box = btn.bounding_box()
        # Find closest preceding text or container
        info = btn.evaluate("""el => {
            const container = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
            return container ? container.innerText.slice(0, 100).replace(/\\n/g, ' ') : '';
        }""")
        print(f"  [{i}] box={box} near: {info}")
