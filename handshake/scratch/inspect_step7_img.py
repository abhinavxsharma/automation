import sys
sys.stdout.reconfigure(encoding="utf-8")
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
    
    # Check if step 7 editor is open
    ta = pg.locator("textarea").first
    if not ta.is_visible():
        edit_btns = pg.locator("button[aria-label='Edit this step']").all()
        edit_btns[7].scroll_into_view_if_needed()
        time.sleep(0.5)
        edit_btns[7].click(force=True)
        time.sleep(1.5)
        
    # Inspect thumbnail container
    img_info = pg.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img')).map(img => {
            const p = img.parentElement;
            return {
                src: img.src.slice(0, 100),
                parentTag: p.tagName,
                parentClass: p.className,
                buttonsInParent: Array.from(p.querySelectorAll('button')).map(b => ({
                    aria: b.getAttribute('aria-label'),
                    text: b.innerText,
                    class: b.className
                }))
            };
        });
        const fileInputs = Array.from(document.querySelectorAll('input[type="file"]')).map(inp => ({
            name: inp.name,
            id: inp.id,
            accept: inp.accept
        }));
        return { imgs, fileInputs };
    }""")
    print("Image info:", img_info)
