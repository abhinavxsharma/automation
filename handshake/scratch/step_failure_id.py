import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Check both checkboxes
    res = pg.evaluate("""() => {
        const labels = Array.from(document.querySelectorAll('label, div[role="checkbox"], input[type="checkbox"]'));
        const clicked = [];
        labels.forEach(el => {
            const txt = el.innerText || '';
            if (txt.includes('Block 1 - Response 1') || txt.includes('Block 2 - Response 1')) {
                el.click();
                clicked.push(txt.trim());
            } else if (el.tagName === 'INPUT' && el.type === 'checkbox') {
                if (!el.checked) {
                    el.click();
                    clicked.push('input-cb');
                }
            }
        });
        return clicked;
    }""")
    print("Clicked checkboxes:", res)
    time.sleep(1)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    if cont_btn.is_visible():
        print("Clicking Continue...")
        cont_btn.click(force=True)
        time.sleep(3)
        
    pg.screenshot(path="scratch/after_failure_id_continue.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_failure_id.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
