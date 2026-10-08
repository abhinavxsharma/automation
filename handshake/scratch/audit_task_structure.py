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
        
    return ctx, pg

with sync_playwright() as p:
    ctx, pg = get_page(p)
    print("Page ready:", pg.title(), pg.url)
    
    # 1. Edit buttons
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Edit buttons:", len(edit_btns))
    
    # If aria-label isn't 'Edit this step', find all buttons with pencil SVG
    if len(edit_btns) == 0:
        pencil_btns = pg.locator("button:has(svg path[d*='M13.586'])").all()
        print("Pencil SVG buttons:", len(pencil_btns))
    
    # Check Step 7 (prompt & image)
    # Check Step 11 (image description)
    # Print headings or labels of steps
    steps = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('div.flex-col, div[data-block-id], section')).map(el => {
            const h = el.querySelector('h1, h2, h3, h4, p, label');
            const btn = el.querySelector('button');
            const hasImg = !!el.querySelector('img');
            return {
                text: el.innerText.slice(0, 100).replace(/\\n/g, ' '),
                hasImg,
                btnCount: el.querySelectorAll('button').length
            };
        }).filter(s => s.text.length > 5);
    }""")
    print(f"Total steps found: {len(steps)}")
    for i, s in enumerate(steps[:15]):
        print(f"Step {i}: [img={s['hasImg']}, btns={s['btnCount']}] {s['text']}")
