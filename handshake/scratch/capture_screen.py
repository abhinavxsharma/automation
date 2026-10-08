from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    pg = next(t for t in b.contexts[0].pages if "/task/" in t.url)
    pg.screenshot(path="scratch/current_screen.png")
    print("Screenshot saved to scratch/current_screen.png")
