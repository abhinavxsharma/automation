import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    inp = pg.locator("textarea, input[type='text']").first
    print("Found input under References. Filling 'N/A'...")
    inp.fill("N/A", force=True)
    time.sleep(0.5)
    
    pg.evaluate("""() => {
        const el = document.querySelector("textarea, input[placeholder*='typing']");
        if (el) {
            el.value = "N/A";
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    time.sleep(0.5)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_references_continue.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_references.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
