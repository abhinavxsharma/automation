from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    print(f"Browser contexts: {len(browser.contexts)}")
    for ci, ctx in enumerate(browser.contexts):
        print(f"Context {ci}: {len(ctx.pages)} pages")
        for pi, pg in enumerate(ctx.pages):
            has_fa = pg.evaluate("() => document.body ? document.body.innerText.includes('Final Answer') : false")
            print(f"  Page {pi}: url={pg.url[:60]} has_Final_Answer={has_fa}")
            for fi, fr in enumerate(pg.frames):
                has_fa_fr = fr.evaluate("() => document.body ? document.body.innerText.includes('Final Answer') : false")
                print(f"    Frame {fi}: url={fr.url[:60]} has_Final_Answer={has_fa_fr}")
