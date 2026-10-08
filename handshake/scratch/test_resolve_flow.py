import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"

REASON_1 = (
    "The diagram has been completely redrawn with optimal spatial clearances and attached to Step 7: "
    "(1) Badge 28 on D -> T is positioned near node D (x=5.56, y=1.28), separated by >1.5 graph units from F -> T; "
    "(2) Badge 20 on F -> T is near T (x=8.44, y=1.84); "
    "(3) Badge 22 on A -> D is positioned directly below node A (x=2.56, y=3.89) with >0.70 units clearance above S -> C, well clear of the crossing; "
    "(4) Every badge sits unambiguously on its own edge with >40px clearance, fixing the unique ground truth critical path duration of 76 ms."
)

def get_page(playwright):
    ctx = create_browser_context(playwright)
    pg = next((t for t in ctx.pages if "/task/" in t.url), None)
    if not pg:
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(TASK_URL)
        pg.wait_for_load_state("networkidle")
        time.sleep(2)
        
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=2000):
        start_btn.click(force=True)
        time.sleep(1)
        
    return ctx, pg

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Click Resolve button 0
    res_btns = pg.locator("button[aria-label='Resolve']").all()
    print("Clicking resolve button 0...")
    res_btns[0].click(force=True)
    time.sleep(1.5)
    
    # 2. Find newly appeared input via evaluate
    res_input = pg.evaluate('''(val) => {
        const inp = Array.from(document.querySelectorAll('input')).find(i => {
            const ph = i.getAttribute('placeholder') || '';
            return ph.includes('resolve') || ph.includes('reason');
        });
        if (!inp) return { error: "No resolve input found" };
        
        inp.focus();
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(inp, val);
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        inp.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Find send button next to inp
        const parent = inp.parentElement;
        const sendBtn = parent.querySelector('button');
        if (!sendBtn) return { error: "No send button found in parent" };
        sendBtn.click();
        return { success: true };
    }''', REASON_1)
    print("Result of resolve 1 submission:", res_input)
    time.sleep(2)
    
    pg.screenshot(path="scratch/after_single_resolve_test.png")
    
    # Check remaining resolve buttons
    rem_btns = pg.locator("button[aria-label='Resolve']").all()
    print("Remaining resolve buttons:", len(rem_btns))
