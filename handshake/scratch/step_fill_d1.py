import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    ta = pg.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    print("Filling Distractor #1 with '85'...")
    ta.fill("85", force=True)
    time.sleep(0.5)
    
    pg.evaluate("""() => {
        const el = document.querySelector("textarea[placeholder='Plausible-but-wrong answer text']");
        if (el) {
            el.value = "85";
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    time.sleep(0.5)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_d1.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
