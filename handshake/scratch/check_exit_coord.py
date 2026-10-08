import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    info = pg.evaluate("""() => {
        const el = document.elementFromPoint(1220, 30);
        if (!el) return null;
        return {
            tagName: el.tagName,
            innerText: el.innerText,
            outerHTML: el.outerHTML,
            parentHTML: el.parentElement ? el.parentElement.outerHTML : null
        };
    }""")
    print("Element at (1220, 30):", info)
