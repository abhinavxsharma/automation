import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/current_live_screen.png")
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/current_live_text.txt").write_text(txt, encoding="utf-8")
    print("Screenshot saved to scratch/current_live_screen.png")
    print("Text length:", len(txt))
