import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    tas = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('textarea')).map(t => ({
            placeholder: t.placeholder,
            value: t.value,
            visible: t.offsetParent !== null,
            className: t.className
        }));
    }""")
    for t in tas:
        print(t)
