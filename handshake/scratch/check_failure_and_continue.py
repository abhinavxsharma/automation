import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    cb0 = pg.locator("#checkbox-11120011-0000-4000-a000-000000000011-0")
    cb1 = pg.locator("#checkbox-11120011-0000-4000-a000-000000000011-1")
    
    print("Checking cb0...")
    cb0.check(force=True)
    time.sleep(0.5)
    print("Checking cb1...")
    cb1.check(force=True)
    time.sleep(0.5)
    
    print("cb0 checked?", cb0.is_checked())
    print("cb1 checked?", cb1.is_checked())
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_cbs_checked.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_cbs.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
