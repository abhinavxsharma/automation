import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Let's inspect the editor area around the textarea
    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']")
    if ta.count() > 0:
        print("Found textarea. Enclosing form/container buttons:")
        container = ta.evaluate("el => el.closest('div.border, section, [data-block-id], form')")
        # Find buttons inside or adjacent
        btns = page.evaluate("""() => {
            const ta = document.querySelector("textarea[placeholder='Plausible-but-wrong answer text']");
            if (!ta) return [];
            let card = ta.closest('div.border') || ta.parentElement;
            return Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.innerText,
                aria: b.getAttribute('aria-label'),
                classes: b.className
            }));
        }""")
        print("Buttons in card:", btns)
    else:
        print("Textarea not found")
