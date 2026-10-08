import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"

def get_page(playwright):
    ctx = create_browser_context(playwright)
    pg = next((t for t in ctx.pages if "/task/" in t.url), None)
    if not pg:
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        print("Navigating to task URL...")
        pg.goto(TASK_URL)
        pg.wait_for_load_state("networkidle")
        time.sleep(2)
        
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=2000):
        print("Dismissing start timer modal...")
        start_btn.click(force=True)
        time.sleep(1)
        
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible(timeout=1000):
        print("Canceling open editor...")
        cancel_btn.click(force=True)
        time.sleep(1)
        
    return ctx, pg

with sync_playwright() as p:
    ctx, pg = get_page(p)
    print("Page ready:", pg.title())
    
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Total edit buttons:", len(edit_btns))
    
    with open("scratch/all_steps_dump.txt", "w", encoding="utf-8") as out:
        for idx in range(len(edit_btns)):
            txt = edit_btns[idx].evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
            out.write(f"\n{'='*30} STEP {idx} {'='*30}\n")
            out.write(txt.strip() + "\n")
            
    print("Dump written to scratch/all_steps_dump.txt")
