import sys
sys.path.insert(0, "scratch")
from chrome_helper import ensure_chrome, PORT
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    pg = browser.contexts[0].pages[0]
    print("URL:", pg.url)
    print("Title:", pg.title())
    
    js = """() => {
        const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => h.innerText.trim()).filter(Boolean);
        return {
            url: window.location.href,
            buttons: btns,
            headings: headings,
            bodyText: document.body.innerText
        };
    }"""
    res = pg.evaluate(js)
    print("Headings:", res["headings"])
    print("Buttons:", res["buttons"][:20])
    lines = [line.strip() for line in res["bodyText"].splitlines() if line.strip()]
    print(f"Total lines: {len(lines)}")
    print("Top 15 lines:")
    for l in lines[:15]:
        print("  ", l)
    print("Bottom 15 lines:")
    for l in lines[-15:]:
        print("  ", l)
