import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    print("Clicking Disagree button at (1174, 199)...")
    pg.mouse.click(1174, 199)
    time.sleep(2)
    
    pg.screenshot(path="scratch/after_mouse_disagree.png")
    
    # Check text around the sidebar
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines ---")
    for ln in lines[-30:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
