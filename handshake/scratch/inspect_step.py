from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pg = next(t for t in b.contexts[0].pages if "/task/" in t.url)
    
    for i, btn in enumerate(pg.locator("button[aria-label='Edit this step']").all()):
        print(f"Edit button {i}: visible={btn.is_visible()}, box={btn.bounding_box()}")
