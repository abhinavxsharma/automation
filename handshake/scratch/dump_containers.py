import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    res = pg.evaluate('''() => {
        const editBtns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        function getContainerText(btn) {
            let el = btn;
            while (el && el.tagName !== 'FORM' && el !== document.body) {
                if (el.className && (el.className.includes('Card') || el.className.includes('card') || el.className.includes('step') || el.className.includes('container') || el.className.includes('group'))) {
                    return el.innerText;
                }
                el = el.parentElement;
            }
            return btn.closest('div[class*="relative"], div[class*="flex"], div[class*="border"]')?.innerText || '';
        }
        
        return {
            s7: getContainerText(editBtns[7]),
            s11: getContainerText(editBtns[11]),
            s14: getContainerText(editBtns[14]),
            s15: getContainerText(editBtns[15]),
            s16: getContainerText(editBtns[16]),
            s18: getContainerText(editBtns[18])
        };
    }''')
    
    for k, v in res.items():
        with open(f"scratch/{k}.txt", "w", encoding="utf-8") as f:
            f.write(v)
        print(f"{k} length: {len(v)}")
