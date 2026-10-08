import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    pages = browser.contexts[0].pages
    print(f"Total pages: {len(pages)}")
    for i, pg in enumerate(pages):
        print(f"  Page {i}: url={pg.url} title={pg.title()}")

    # Find the task page
    target_page = None
    for pg in pages:
        if "ai.joinhandshake.com" in pg.url:
            target_page = pg
            break

    if not target_page:
        target_page = pages[0]

    # Wait for body text
    for _ in range(10):
        t = target_page.evaluate("() => document.body ? document.body.innerText : ''")
        if len(t) > 100:
            break
        time.sleep(0.5)

    print(f"Target page text length: {len(t)}")
    with open("scratch/task_page_text.txt", "w", encoding="utf-8") as f:
        f.write(t)

    # Let's search for key phrases in the text
    phrases = [
        "task-dependency", "critical path", "Model responses",
        "Block 1", "Block 2", "Generating", "Failed", "Final Answer",
        "Enter your prompt", "Submit", "Continue"
    ]
    for ph in phrases:
        print(f"  Contains '{ph}': {ph.lower() in t.lower()}")

    target_page.screenshot(path="scratch/target_page_full.png", full_page=True)
    print("Saved scratch/target_page_full.png")
