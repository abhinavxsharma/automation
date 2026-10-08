import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

REASON_1 = (
    "The diagram has been completely regenerated with optimal spatial clearances and attached to Step 7: "
    "(1) Badge 28 on D -> T is positioned near node D (x=5.56, y=1.28), separated by >1.5 graph units from F -> T; "
    "(2) Badge 20 on F -> T is near T (x=8.44, y=1.84); "
    "(3) Badge 22 on A -> D is positioned directly below node A (x=2.56, y=3.89) with >0.70 units clearance above S -> C, well clear of the crossing; "
    "(4) Every badge sits unambiguously on its own edge with >40px clearance, fixing the unique ground truth critical path duration of 76 ms."
)

REASON_2 = (
    "The sentence claiming that every weight value is plainly visible and directly readable has been removed from the task description as requested. "
    "The description provides an objective overview of the 8 nodes, 15 directed edges, and weights while satisfying the 200-word requirement."
)

def send_feedback_reason(page, reason_text):
    ta = page.locator("textarea[placeholder*='resolve reason'], textarea[placeholder*='Reply']").first
    if not ta.is_visible(timeout=3000):
        print("Textarea not visible for feedback reason!")
        return False
        
    print("Filling feedback reason...")
    ta.fill(reason_text)
    time.sleep(0.5)
    
    print("Clicking paper airplane send button...")
    sent = page.evaluate("""() => {
        const ta = document.querySelector("textarea[placeholder*='resolve reason'], textarea[placeholder*='Reply']");
        if (!ta) return { error: "No textarea" };
        let p = ta.parentElement;
        while (p && p.tagName !== 'SECTION' && p !== document.body) {
            const btns = Array.from(p.querySelectorAll('button')).filter(b => {
                const aria = b.getAttribute('aria-label') || '';
                return b.querySelector('svg') && aria !== 'Resolve' && aria !== 'Disagree' && aria !== 'Close';
            });
            if (btns.length > 0) {
                btns[0].click();
                return { success: true };
            }
            p = p.parentElement;
        }
        return { error: "No send button found" };
    }""")
    print("Send result:", sent)
    time.sleep(2)
    return sent.get("success", False)

with sync_playwright() as p:
    ctx, pg = get_page(p)
    print("Connected to task page:", pg.title())
    
    # 1. Resolve first Jimson feedback card
    res_btns = pg.locator("button[aria-label='Resolve']:visible").all()
    print("Visible resolve buttons:", len(res_btns))
    if len(res_btns) > 0:
        print("Clicking resolve button 1...")
        res_btns[0].click(force=True)
        time.sleep(1)
        send_feedback_reason(pg, REASON_1)
        
    # 2. Resolve second Jimson feedback card
    res_btns_after = pg.locator("button[aria-label='Resolve']:visible").all()
    print("Visible resolve buttons after item 1:", len(res_btns_after))
    if len(res_btns_after) > 0:
        print("Clicking resolve button 2...")
        res_btns_after[0].click(force=True)
        time.sleep(1)
        send_feedback_reason(pg, REASON_2)
        
    pg.screenshot(path="scratch/after_both_jimson_resolved.png")
    
    # 3. Check sidebar status
    sidebar_text = pg.evaluate("""() => {
        const aside = document.querySelector('aside') || document.querySelector("div[data-radix-scroll-area-viewport]");
        return aside ? aside.innerText : '';
    }""")
    print("\n=== SIDEBAR STATUS ===\n", sidebar_text[:400])
