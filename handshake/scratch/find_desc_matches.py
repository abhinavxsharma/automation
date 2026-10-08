import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    res = page.evaluate("""() => {
        const matches = [];
        for (const el of document.querySelectorAll('*')) {
            if (el.innerText && el.innerText.includes('Write a detailed description')) {
                matches.push({
                    tag: el.tagName,
                    childrenCount: el.children.length,
                    text: el.innerText.substring(0, 100),
                    rect: el.getBoundingClientRect()
                });
            }
        }
        return matches;
    }""")
    print(f"Found {len(res)} matches:")
    for m in res:
        print(" ", m)
