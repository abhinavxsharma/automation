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
    
    # Click edit on step 7
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    edit_btns[7].scroll_into_view_if_needed()
    time.sleep(0.5)
    edit_btns[7].click(force=True)
    time.sleep(1.5)
    
    # Inspect all elements at the bottom of the editor
    details = pg.evaluate("""() => {
        const ta = document.querySelector('textarea');
        if (!ta) return 'No textarea';
        const form = ta.closest('form') || ta.parentElement.parentElement;
        const allElements = Array.from(form.querySelectorAll('*')).map(el => ({
            tag: el.tagName,
            aria: el.getAttribute('aria-label'),
            text: el.innerText ? el.innerText.trim() : '',
            className: el.className
        }));
        return allElements.filter(e => e.aria || e.text || e.tag === 'IMG' || e.tag === 'INPUT');
    }""")
    print("Found form elements:")
    for d in details:
        print(d)
