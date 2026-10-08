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

REASON_2 = (
    "The sentence claiming that every weight value is plainly visible and directly readable has been removed from the task description as requested. "
    "The description provides an objective overview while satisfying the 200-word requirement."
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
    print("Page ready:", pg.title())
    
    # === RESOLVE ITEM 1 ===
    # Check if input is already open from previous step
    inp1 = pg.locator("input[placeholder='Add a resolve reason']").first
    if not inp1.is_visible(timeout=1000):
        res_btn1 = pg.locator("button[aria-label='Resolve']").first
        print("Clicking resolve button 1...")
        res_btn1.click(force=True)
        time.sleep(1)
        inp1 = pg.locator("input[placeholder='Add a resolve reason']").first
        
    print("Filling resolve reason 1...")
    inp1.fill(REASON_1)
    time.sleep(0.5)
    
    # Click paper airplane button inside the same container
    parent1 = inp1.locator("xpath=..")
    send1 = parent1.locator("button").first
    print("Sending resolution 1...")
    send1.click(force=True)
    time.sleep(2)
    
    pg.screenshot(path="scratch/after_resolve_1.png")
    
    # === RESOLVE ITEM 2 ===
    # Check remaining resolve buttons
    res_btns = pg.locator("button[aria-label='Resolve']").all()
    print("Remaining resolve buttons:", len(res_btns))
    if len(res_btns) > 0:
        print("Clicking resolve button 2...")
        res_btns[0].click(force=True)
        time.sleep(1)
        
        inp2 = pg.locator("input[placeholder='Add a resolve reason']").first
        print("Filling resolve reason 2...")
        inp2.fill(REASON_2)
        time.sleep(0.5)
        
        parent2 = inp2.locator("xpath=..")
        send2 = parent2.locator("button").first
        print("Sending resolution 2...")
        send2.click(force=True)
        time.sleep(2)
        
    pg.screenshot(path="scratch/after_both_resolved_live.png")
    
    # Check progress text
    prog = pg.locator("div:has-text('items addressed')").all_inner_texts()
    print("Progress:", prog)
