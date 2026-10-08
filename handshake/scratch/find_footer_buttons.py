import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    btns = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, idx) => ({
            idx,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            box: b.getBoundingClientRect()
        })).filter(b => b.box.height > 0);
    }""")
    print(f"Total visible buttons: {len(btns)}")
    for b in btns:
        if b['text'] or 'Submit' in b['aria'] or 'Next' in b['aria'] or b['box']['y'] > 600:
            print(b)
