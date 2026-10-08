import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

REASON = (
    "The Science Judge flag is an automated parser false positive. "
    "The quote cited ('The prompt can only be solved with the information in the image') is the platform checklist label, not the prompt. "
    "The prompt explicitly specifies: 'determine the critical path duration (maximum latency from S to T)'. "
    "Standard CPM topological dynamic programming yields a unique, unambiguous ground truth answer of 76 ms."
)

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Click Disagree button to open textarea
    disagree_btn = pg.locator("button[aria-label='Disagree']:visible").first
    if disagree_btn.is_visible():
        print("Clicking Disagree button to reveal textarea...")
        disagree_btn.click()
        time.sleep(1.5)
        
    # 2. Locate textarea
    ta = pg.locator("textarea[placeholder='Reason for disagreeing']").first
    print("Found textarea:", ta.is_visible())
    if ta.is_visible():
        ta.fill(REASON)
        time.sleep(0.5)
        
        # 3. Find and click submit arrow button
        sent = pg.evaluate("""() => {
            const ta = document.querySelector("textarea[placeholder='Reason for disagreeing']");
            if (!ta) return { error: "No textarea" };
            let p = ta.parentElement;
            while (p && p.tagName !== 'SECTION' && p !== document.body) {
                const btns = Array.from(p.querySelectorAll('button')).filter(b => {
                    const aria = b.getAttribute('aria-label') || '';
                    return aria !== 'Close' && aria !== 'Disagree' && aria !== 'Resolve';
                });
                if (btns.length > 0) {
                    btns[0].click();
                    return { success: true, aria: btns[0].getAttribute('aria-label') };
                }
                p = p.parentElement;
            }
            return { error: "No button found" };
        }""")
        print("Submit result:", sent)
        time.sleep(3)
        
    pg.screenshot(path="scratch/after_disagree_sub_final.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_sub_final.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines ---")
    for ln in lines[-30:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
