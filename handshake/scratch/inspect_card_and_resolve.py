import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    card_info = page.evaluate("""() => {
        const inputs = Array.from(document.querySelectorAll('input, textarea')).map(i => {
            const rect = i.getBoundingClientRect();
            return {
                tag: i.tagName,
                placeholder: i.placeholder,
                value: i.value,
                rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) }
            };
        }).filter(i => i.rect.w > 0 && i.rect.h > 0);

        const btns = Array.from(document.querySelectorAll('button')).map(b => {
            const rect = b.getBoundingClientRect();
            return {
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
                disabled: b.disabled
            };
        }).filter(b => b.rect.w > 0 && b.rect.h > 0 && b.rect.x > 700);

        return {
            inputs,
            btns
        };
    }""")

    print("Inputs:")
    for inp in card_info.get("inputs", []):
        print(f"  {inp['tag']} placeholder='{inp['placeholder']}' rect={inp['rect']}")
    print("\nButtons on right:")
    for b in card_info.get("btns", []):
        print(f"  aria='{b['aria']}' text='{b['text']}' rect={b['rect']}")
