import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    next_btn = pg.locator("button:has-text('Next')").first
    print("Next button visible?", next_btn.is_visible())
    print("Next button enabled?", next_btn.is_enabled())
    
    if next_btn.is_visible() and next_btn.is_enabled():
        print("Clicking Next button...")
        next_btn.click()
        time.sleep(3)
        
    pg.screenshot(path="scratch/after_next_click.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_next.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
