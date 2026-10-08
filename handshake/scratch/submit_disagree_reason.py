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
    inp = pg.locator("input[placeholder*='Reason for disagreeing'], textarea[placeholder*='Reason for disagreeing']").first
    print("Found disagree input:", inp.is_visible())
    inp.fill(REASON)
    time.sleep(0.5)
    
    # Click the send arrow button next to the input
    sent = pg.evaluate("""() => {
        const inp = document.querySelector("input[placeholder*='Reason for disagreeing'], textarea[placeholder*='Reason for disagreeing']");
        if (!inp) return { error: "No input" };
        const p = inp.parentElement;
        const btn = p.querySelector("button");
        if (btn) {
            btn.click();
            return { success: true, btnAria: btn.getAttribute('aria-label') };
        }
        return { error: "No button in parent" };
    }""")
    print("Submit disagree result:", sent)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_submit_disagree.png")
    
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_disagree_sub.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines ---")
    for ln in lines[-30:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
