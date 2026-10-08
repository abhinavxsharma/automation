import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Pick Block 1 - Response 1 radio
    res = pg.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
            if (node.nodeValue && node.nodeValue.trim() === 'Block 1 - Response 1') {
                const el = node.parentElement;
                if (el) {
                    el.click();
                    return true;
                }
            }
        }
        return false;
    }""")
    print("Clicked Block 1 - Response 1?", res)
    time.sleep(1)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_failure_selection.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_failure_selection.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
