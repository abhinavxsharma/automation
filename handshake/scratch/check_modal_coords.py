import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(1000)
    
    info = pg.evaluate("""() => {
        const points = [
            [500, 665],
            [500, 610],
            [500, 320]
        ];
        return points.map(([x, y]) => {
            const el = document.elementFromPoint(x, y);
            return el ? {
                x, y,
                tag: el.tagName,
                text: el.innerText ? el.innerText.trim() : '',
                outerHTML: el.outerHTML.slice(0, 200)
            } : {x, y, el: null};
        });
    }""")
    for item in info:
        print(item)
