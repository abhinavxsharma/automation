import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = next((t for t in ctx.pages if "/task/" in t.url), ctx.pages[0])
    
    # 1. Inspect edit buttons
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Total edit buttons found:", len(edit_btns))
    
    # Let's inspect step 7, 11, 18
    # Step 7
    if len(edit_btns) > 7:
        s7_text = edit_btns[7].evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        print("\n=== STEP 7 TEXT SNIPPET ===")
        print(s7_text[:300])
        
    # Step 11
    if len(edit_btns) > 11:
        s11_text = edit_btns[11].evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        print("\n=== STEP 11 TEXT SNIPPET ===")
        print(s11_text[-300:])
        
    # Distractors
    for i in range(18, min(23, len(edit_btns))):
        st = edit_btns[i].evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        print(f"Step {i}: {st.replace(chr(10), ' ')[:80]}")
        
    # Feedback items
    fb_cards = pg.locator("div.border.rounded-lg, div:has(> button:has-text('Reply'))").all()
    print("\n=== FEEDBACK CARDS ===", len(fb_cards))
    for i, c in enumerate(fb_cards):
        print(f"Card {i}: {c.inner_text().replace(chr(10), ' ')[:150]}")
