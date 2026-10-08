import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Scroll down to reveal Step 7
    page.evaluate("window.scrollBy(0, 1000)")
    time.sleep(1)

    page.screenshot(path="handshake/scratch/scrolled_to_step7.png")
    print("Saved scrolled_to_step7.png")

    # Inspect all edit buttons currently visible in viewport
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button[aria-label="Edit this step"]')).map((b, idx) => {
            const r = b.getBoundingClientRect();
            return {
                idx,
                x: r.x,
                y: r.y,
                visible: r.width > 0 && r.height > 0 && r.top >= 0 && r.bottom <= window.innerHeight
            };
        });
    }""")
    print("Edit buttons:", btns)
