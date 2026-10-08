import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    cont = pg.locator("button:has-text('Continue')").first
    print("Continue visible?", cont.is_visible())
    cont.click(force=True)
    time.sleep(3)
    pg.screenshot(path="scratch/after_golden_click_continue.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_golden_click.txt", "w", encoding="utf-8") as f:
        f.write(text)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines ---")
    for ln in lines[-30:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
