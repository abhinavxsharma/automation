from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pg = next(t for t in b.contexts[0].pages if "/task/" in t.url)
    
    # Click the edit button for prompt
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    # The prompt edit button was at y ~ 549
    target_btn = None
    for btn in edit_btns:
        box = btn.bounding_box()
        if box and 400 < box["y"] < 800:
            target_btn = btn
            break
            
    if target_btn:
        print("Clicking prompt edit button...")
        target_btn.click(force=True)
        pg.wait_for_timeout(2000)
        pg.screenshot(path="scratch/after_edit_click.png")
        print("Screenshot saved to scratch/after_edit_click.png")
    else:
        print("Target edit button not found")
