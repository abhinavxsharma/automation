import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    info = pg.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]'));
        return els.map(e => ({
            tag: e.tagName,
            type: e.type,
            placeholder: e.placeholder,
            value: e.value ? e.value.slice(0, 50) : '',
            innerText: e.innerText ? e.innerText.slice(0, 50) : '',
            visible: e.offsetParent !== null
        }));
    }""")
    for item in info:
        print(item)
