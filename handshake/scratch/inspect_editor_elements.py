import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = next((t for t in ctx.pages if "/task/" in t.url), ctx.pages[0])
    
    # Check buttons inside or near textarea
    ta = pg.locator("textarea").first
    parent = ta.locator("xpath=./ancestor::div[contains(@class, 'border') or contains(@class, 'rounded')]").first
    print("Editor HTML snippet:")
    btns = parent.locator("button").all()
    print("Buttons inside editor container:", len(btns))
    for i, b in enumerate(btns):
        print(f"Btn {i}: aria='{b.get_attribute('aria-label')}' text='{b.inner_text()}' class='{b.get_attribute('class')}'")
        
    imgs = parent.locator("img").all()
    print("Imgs inside editor container:", len(imgs))
    for i, img in enumerate(imgs):
        print(f"Img {i}: src='{img.get_attribute('src')[:80]}'")
