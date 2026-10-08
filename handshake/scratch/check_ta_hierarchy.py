import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    if ta.is_visible():
        info = ta.evaluate("""el => {
            let res = [];
            // Check parent and its children
            let curr = el;
            for (let depth = 0; depth < 5; depth++) {
                if (!curr) break;
                const btns = Array.from(curr.querySelectorAll('button'));
                res.push({
                    depth: depth,
                    tag: curr.tagName,
                    className: curr.className,
                    buttonCount: btns.length,
                    buttons: btns.map(b => ({
                        text: b.innerText,
                        aria: b.getAttribute('aria-label'),
                        type: b.getAttribute('type'),
                        outerHTML: b.outerHTML
                    }))
                });
                curr = curr.parentElement;
            }
            return res;
        }""")
        for item in info:
            print(f"Depth {item['depth']} ({item['tag']}, class='{item['className'][:30]}'): {item['buttonCount']} buttons")
            for b in item['buttons']:
                print(f"  Button text='{b['text']}' aria='{b['aria']}' outerHTML={b['outerHTML'][:120]}")
