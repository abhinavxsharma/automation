import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"

with sync_playwright() as p:
    ctx = create_browser_context(p)
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
        
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Found edit buttons:", len(edit_btns))
    for i, b in enumerate(edit_btns):
        txt = b.evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        first_line = lines[0] if lines else "EMPTY"
        second_line = lines[1] if len(lines) > 1 else ""
        print(f"Index {i:2d}: {first_line[:50]} | {second_line[:50]}")
