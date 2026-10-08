import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    pg.screenshot(path="scratch/current_golden_screen.png")
    
    # Check all elements that can receive text
    info = pg.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('textarea, input, [contenteditable="true"], [role="textbox"]'));
        return els.map(e => ({
            tag: e.tagName,
            type: e.type,
            contentEditable: e.getAttribute('contenteditable'),
            role: e.getAttribute('role'),
            className: e.className,
            placeholder: e.placeholder,
            value: e.value,
            innerText: e.innerText ? e.innerText.slice(0, 100) : '',
            visible: e.offsetParent !== null
        }));
    }""")
    print("Found inputs:", info)
    
    # Also dump last 30 lines of text
    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    for ln in body.splitlines()[-30:]:
        print("  ", ln.encode('ascii', 'replace').decode('ascii'))
