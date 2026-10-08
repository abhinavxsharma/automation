import sys
sys.path.insert(0, ".")
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = next((t for t in ctx.pages if "/task/" in t.url), ctx.pages[0])
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    
    for idx in [7, 11, 14, 15, 16, 18, 19, 20, 21, 22]:
        txt = edit_btns[idx].evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        print(f"\n================ STEP {idx} ================")
        print(txt.strip()[:350])
