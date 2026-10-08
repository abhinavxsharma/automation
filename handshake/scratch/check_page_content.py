import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_timeout(1000)

    # Dismiss modal if open
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0:
        box = modal_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    info = page.evaluate("""() => {
        return {
            textLength: document.body.innerText.length,
            title: document.title,
            url: window.location.href,
            snippet: document.body.innerText.slice(0, 500)
        };
    }""")
    print("Page info:", info)
