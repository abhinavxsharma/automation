import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    disagree_btn = pg.locator("button[aria-label='Disagree']").first
    print("Disagree button visible?", disagree_btn.is_visible())
    if disagree_btn.is_visible():
        disagree_btn.click(force=True)
        time.sleep(2)
        
    pg.screenshot(path="scratch/after_disagree_click.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_disagree.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
