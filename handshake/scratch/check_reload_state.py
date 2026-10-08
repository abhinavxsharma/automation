import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    print("Reloading page...")
    pg.reload()
    time.sleep(5)
    
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=2000):
        start_btn.click()
        time.sleep(1)
        
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    print(f"Text length after reload: {len(text)}")
    if "Block 1 Responses:" in text:
        idx = text.find("Block 1 Responses:")
        print(text[idx:idx+500].encode('ascii', 'replace').decode('ascii'))
