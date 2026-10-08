import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    info = pg.evaluate('''() => {
        const editBtns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        function getText(btn) {
            if (!btn) return 'None';
            let el = btn;
            for (let i = 0; i < 6; i++) {
                if (!el) break;
                if (el.innerText && el.innerText.length > 50) return el.innerText;
                el = el.parentElement;
            }
            return btn.parentElement ? btn.parentElement.innerText : 'None';
        }
        return {
            s11: getText(editBtns[11]),
            s14: getText(editBtns[14]),
            s15: getText(editBtns[15]),
            s16: getText(editBtns[16]),
            d1: getText(editBtns[18]),
            d2: getText(editBtns[19]),
            d3: getText(editBtns[20]),
            d4: getText(editBtns[21]),
            d5: getText(editBtns[22])
        };
    }''')
    for k, v in info.items():
        print(f"=== {k} ===")
        print(v[:250].encode('ascii', 'replace').decode('ascii'))
