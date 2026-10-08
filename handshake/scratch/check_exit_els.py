import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(1000)
    
    els = pg.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        return all
            .filter(e => e.innerText && e.innerText.includes('Exit task'))
            .map(e => ({
                tag: e.tagName,
                text: e.innerText.slice(0, 50),
                className: e.className
            }));
    }""")
    print(f"Elements containing 'Exit task': {len(els)}")
    for e in els:
        print(" ", e['tag'], e['className'], repr(e['text']))
