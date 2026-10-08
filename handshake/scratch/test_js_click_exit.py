import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(2000)
    clicked = pg.evaluate("""() => {
        const spans = Array.from(document.querySelectorAll('span'));
        const exitSpan = spans.find(s => s.innerText && s.innerText.trim() === 'Exit');
        if (exitSpan) {
            const btn = exitSpan.closest('button');
            if (btn) {
                btn.click();
                return 'Clicked Exit button';
            }
            exitSpan.click();
            return 'Clicked Exit span';
        }
        return 'Exit not found';
    }""")
    print("JS Click result:", clicked)
    pg.wait_for_timeout(2000)
    pg.screenshot(path="scratch/after_js_click_exit.png")
    txt = pg.evaluate("() => document.body ? document.body.innerText : ''")
    print("After click text preview:")
    print(txt[:600])
