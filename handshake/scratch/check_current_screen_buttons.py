import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    pg.screenshot(path="scratch/check_screen_right_now.png")
    
    btns = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, i) => ({
            i,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            box: b.getBoundingClientRect()
        })).filter(b => b.box.height > 0);
    }""")
    print("Visible buttons count:", len(btns))
    for b in btns:
        if b['text'] or b['aria']:
            print(f"[{b['i']:2d}] text='{b['text']}' aria='{b['aria']}'")
