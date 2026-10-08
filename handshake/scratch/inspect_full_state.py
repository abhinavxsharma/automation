import json
import sys
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    print(f"Contexts count: {len(browser.contexts)}")
    for c_idx, ctx in enumerate(browser.contexts):
        print(f"Context {c_idx} pages count: {len(ctx.pages)}")
        for p_idx, pg in enumerate(ctx.pages):
            print(f"  Page {p_idx}: URL={pg.url} Title={pg.title()}")
            
    # Look for task page or any handshake page
    target_page = None
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if "1520c7f4" in pg.url or "task" in pg.url:
                target_page = pg
                break
        if target_page:
            break
            
    if not target_page and browser.contexts and browser.contexts[0].pages:
        target_page = browser.contexts[0].pages[0]
        
    if target_page:
        print(f"\nTargeting Page: {target_page.url}")
        target_page.bring_to_front()
        time.sleep(2)
        target_page.screenshot(path="scratch/target_page_snap.png")
        print("Screenshot saved to scratch/target_page_snap.png")
        
        info = target_page.evaluate('''() => {
            const startTimerBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
            const banners = Array.from(document.querySelectorAll('[role="alert"], [class*="alert"], [class*="banner"]')).map(el => el.innerText.trim()).filter(Boolean);
            const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                disabled: b.disabled,
                ariaDisabled: b.getAttribute('aria-disabled'),
                classes: b.className
            })).filter(b => b.text.length > 0);
            
            return {
                url: window.location.href,
                title: document.title,
                hasStartTimerModal: !!startTimerBtn,
                banners,
                buttons,
                bodySnippet: document.body.innerText.slice(0, 3000)
            };
        }''')
        print("URL:", info["url"])
        print("Title:", info["title"])
        print("Has Start Timer Modal:", info["hasStartTimerModal"])
        print("Banners:", info["banners"])
        print("Buttons count:", len(info["buttons"]))
        for b in info["buttons"]:
            print(f"  Btn: '{b['text']}' (disabled={b['disabled']}, aria={b['ariaDisabled']})")
        print("\nBody snippet:")
        print(info["bodySnippet"][:1500])
