import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    info = pg.evaluate("""() => {
        const inps = Array.from(document.querySelectorAll('input[type="text"], textarea'));
        return inps.map(i => ({
            tag: i.tagName,
            type: i.type,
            placeholder: i.placeholder,
            value: i.value,
            visible: i.offsetParent !== null
        }));
    }""")
    for item in info:
        print(item)
