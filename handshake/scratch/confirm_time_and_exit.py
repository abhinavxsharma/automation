import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    conf_btn = pg.locator("button:has-text('Confirm time')").first
    print("Confirm time visible?", conf_btn.is_visible())
    if conf_btn.is_visible():
        print("Clicking Confirm time...")
        conf_btn.click()
        time.sleep(3)
        
    pg.screenshot(path="scratch/after_confirm_time.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_confirm_time.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 20 lines ---")
    for ln in lines[-20:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
