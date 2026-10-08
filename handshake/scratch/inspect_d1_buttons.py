import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Find the editor card around textarea
    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    if ta.count() > 0 and ta.is_visible():
        btns = ta.evaluate("""el => {
            let card = el.closest('div.border') || el.parentElement.parentElement;
            return Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.innerText,
                aria: b.getAttribute('aria-label'),
                className: b.className,
                html: b.outerHTML
            }));
        }""")
        print("Buttons in editor card:")
        for b in btns:
            print("Button:", b)
    else:
        print("Textarea not visible right now")
